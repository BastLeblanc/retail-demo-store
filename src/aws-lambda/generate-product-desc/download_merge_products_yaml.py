import boto3
import yaml


s3 = boto3.resource('s3')


def write_yaml(bucket, outputfile, products):
    with open("products_new.yaml", 'w') as stream:
        try:
            yaml.safe_dump(products, stream, sort_keys=False)
        except yaml.YAMLError as exc:
            print(exc)
    #upload to s3
    s3.Bucket(bucket).upload_file("products_new.yaml", outputfile)

bucket='retaildemostore-output.bastil.appdev.us-east-1'

#copy all products* files from bucket 
bucket_objects = s3.Bucket(bucket).objects.filter(Prefix='generate/input/products')
products = []
for obj in bucket_objects:
    print(obj.key)
    #download products file from s3
    s3.Bucket(bucket).download_file(obj.key, "/tmp/products.yaml")
    with open("/tmp/products.yaml", 'r') as stream:
        try:
            products_new = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    #merge products_new with products
    products.extend(products_new)


print(len(products))

write_yaml('retaildemostore.bastil.appdev.us-east-1', 'generate/output/products.yaml', products)
