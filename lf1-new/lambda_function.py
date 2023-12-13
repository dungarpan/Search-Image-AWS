import json
import boto3
import requests

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')
elasticsearch = boto3.client('es')


# Function to detect labels using Rekognition
def detect_labels(bucket, object_key):
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': object_key
            }
        }
    )
    print("rekognition")
    print(response)
    return [label['Name'] for label in response['Labels']]
    
# Function to get S3 metadata
def get_s3_metadata(bucket, object_key):
    response = s3.head_object(Bucket=bucket, Key=object_key)
    print("s3 bucket")
    print(response)
    return response

# Function to store JSON object in Elasticsearch
def store_in_opensearch(json_object):
    opensearch_url = 'https://search-photos-jsgbl4vz7jyakpja4uzrue2mbi.us-east-1.es.amazonaws.com' 
    index_name = 'photos'
    doc_type = '_doc'

    headers = {'Content-Type': 'application/json'}

    url = f'{opensearch_url}/{index_name}/{doc_type}'
    #url = f'{opensearch_url}/{index_name}'
    response = requests.post(url, headers=headers, data=json.dumps(json_object))

    print("OpenSearch indexed")
    print("Opensearch response")
    print(response)
    print(response.text)
    print("***")

def lambda_handler(event, context):
    try:
        s3_record = event['Records'][0]['s3']
        print("s3 record", s3_record)
        object_key = s3_record['object']['key']
        print("object_key", object_key)
        bucket = s3_record['bucket']['name']
        print("bucket", bucket)

        # Step 1: Detect labels using Rekognition
        labels = detect_labels(bucket, object_key)

        # Step 2: Retrieve S3 metadata
        metadata = get_s3_metadata(bucket, object_key)

        # Step 3: Create the JSON object
        json_object = {
            'objectKey': object_key,
            'bucket': bucket,
            #'createdTimestamp': metadata['Metadata']['createdTimestamp'],
            'labels': labels
        }

        # Step 4: Store JSON object in Elasticsearch
        store_in_opensearch(json_object)

        return {'statusCode': 200, 'body': 'Success'}
    except Exception as e:
        print(f'Error: {e}')
        return {'statusCode': 500, 'body': 'Error'}




