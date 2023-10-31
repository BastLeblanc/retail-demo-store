import boto3
import yaml
import json
import time


bedrock = boto3.client(service_name='bedrock-runtime')
s3 = boto3.resource('s3')
products = []

def write_yaml(bucket, outputfile, products):
    with open("/tmp/products_new.yaml", 'w') as stream:
        try:
            yaml.safe_dump(products, stream, sort_keys=False)
        except yaml.YAMLError as exc:
            print(exc)
    #upload to s3
    s3.Bucket(bucket).upload_file("/tmp/products_new.yaml", outputfile)

def call_model(prompt):
    tic = time.perf_counter()
    body = json.dumps(
        {"prompt": prompt
        , "max_tokens_to_sample" : 300  ,
        "temperature": 1,
         "top_k": 150,
         "top_p": 0.6
         })
    modelId = 'anthropic.claude-v2'
    accept = 'application/json'
    contentType = 'application/json'
    response = bedrock.invoke_model(
        body=body, 
        modelId=modelId, 
        accept=accept,
        contentType=contentType)
    response_body = json.loads(response.get('body').read())

    toc = time.perf_counter()

    print(f"call_model in {toc - tic:0.4f} seconds")
    print(response_body['completion'])
    if(response_body['completion'].find(":")>0):
        output=response_body['completion'].split(":")
        final_output=''
        for i in range(len(output)) :
            if i>0: #we skip the first line which the start of the answer "Here is a[....]details:"
                final_output+=output[i].strip().replace('\\','').replace('\n','')
        return(final_output)
    else:
        # there's no ':' we return the whole answer
        return(response_body['completion'].strip().replace('\\','').replace('\n',''))
    

def generate_description(products,index):

    # get only required data from product

    product_for_prompt={}
    product_for_prompt['name']=products[index]['name']
    product_for_prompt['description']=products[index]['description']
    product_for_prompt['category']=products[index]['category']

    prompt = (f"Human: Given the following product details:\n"
        f"{product_for_prompt}"
        f"         "
        f"Please generate an enhanced product description that incorporates all the above elements while ensuring "
        f"high-quality language and factual coherence. Make the description rich in relevant details "
        f"and present it in a format that starts with a detailed description of the product as an opening sentence.\n"
        f""
        f"Assistant:"
    )

    products[index]['description']= call_model(prompt)


def generate_title(products,index):

    prompt = f"""Human: Consider this product information 
    {products[index]}

    create a more descriptive title for the product in less 10 words listed above. Make the title simple and original. It shouldn't be a sentence.
    Assistant:
    """

    products[index]['name'] =  call_model(prompt)

def lambda_handler(event, context):

    bucket='retaildemostore.bastil.appdev.us-east-1'
    bucket_output='retaildemostore-output.bastil.appdev.us-east-1'

    #read
    print("reading products from s3")
    s3.Bucket(bucket).download_file(event['Key'], "/tmp/products.yaml")
    with open("/tmp/products.yaml", 'r') as stream:
        try:
            products = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    print("loaded " + str(len(products)) +  "products")
    print("** generating new products info descriptions and title**")
    for i in range(len(products)):
        generate_description(products,i)
        generate_title(products,i)

    #Final Write
    write_yaml(bucket_output,event['Key'],products)




#event={}
#event['action']=  'GENERATE'
#event['inputbucket']=  'retaildemostore.bastil.appdev.us-east-1'
#event['outputbucket']=  'retaildemostore.bastil.appdev.us-east-1'
#event['Key']=  'generate/input/products01.yaml'
#event['file_output']=  'generate/output/products01.yaml'
#lambda_handler(event, {})