import boto3
import yaml


s3 = boto3.resource('s3')


def write_yaml(bucket, outputfile, products):
    with open("/tmp/products_new.yaml", 'w') as stream:
        try:
            yaml.safe_dump(products, stream, sort_keys=False)
        except yaml.YAMLError as exc:
            print(exc)
    #upload to s3
    print("upload to s3://" + bucket + "/" + outputfile)
    s3.Bucket(bucket).upload_file("/tmp/products_new.yaml", outputfile)


def lambda_handler(event, context):
    print(event)
    if event['action'] == 'chunk':
        # chunk = you need to break products into chunks to prepare
        #download products file from s3
        s3.Bucket(event['bucket-source']).download_file(event['file-source'], "/tmp/products.yaml")
        with open("/tmp/products.yaml", 'r') as stream:
            try:
                products = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        

        print("products loaded = " + str(len(products)))
        # break products into chunks 
        chunk_size = event['chunk_size']
        chunks = [products[i:i+chunk_size] for i in range(0, len(products), chunk_size)]

        i=0

        # remove objects with a certain prefix in bucket
        bucket_objects = s3.Bucket(event['bucket-source']).objects.filter(Prefix=event['prefix'])
        for obj in bucket_objects:
            obj.delete()

        for chunk in chunks:
            write_yaml(event['bucket-source'], event['prefix'] + '/products{:02d}.yaml'.format(i), chunk)
            i+=1
    
    elif event['action'] == 'merge':
        #copy all products* files from bucket 
        bucket_objects = s3.Bucket(event['bucket-output']).objects.filter(Prefix=event['prefix'])
        products_new = []
        for obj in bucket_objects:
            print("reading " + event['bucket-output'] + "/" + obj.key)
            #download products file from s3
            s3.Bucket(event['bucket-output']).download_file(obj.key, "/tmp/products.yaml")
            with open("/tmp/products.yaml", 'r') as stream:
                try:
                    products = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)
            #merge products_new with products
            products_new.extend(products)

        print("products loaded = " + str(len(products_new)))
        #upload the merged products to s3
        write_yaml(event['bucket-output'], event['file-output'], products_new)

    else:
        print("Unknown action")
        return 1



## LOCAL TESTING
#event={}
#event['action'] = 'merge'
#event['bucket-source'] = 'retaildemostore.bastil.appdev.us-east-1'
#event['file-source'] = 'generate-products/main/products.yaml'
#event['bucket-output'] = 'retaildemostore-output.bastil.appdev.us-east-1'
#event['file-output'] = 'generate-products/main/products.yaml'
#event['chunk_size'] = 100
#
#lambda_handler(event, '')