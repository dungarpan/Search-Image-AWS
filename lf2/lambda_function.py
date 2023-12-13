import json
import boto3
import random
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
import requests

def generate_session_id(length=10):
    # Generate a random session ID using letters and digits
    characters = string.ascii_letters + string.digits
    session_id = ''.join(random.choice(characters) for _ in range(length))
    return session_id
    

def get_opensearch_auth():
    session = boto3.Session()
    credentials = session.get_credentials()
    awsauth = AWS4Auth(
        credentials.access_key,
        #AKIA3OC4XIIWFQSQ73VK,
        credentials.secret_key,
        #ccUQZcuaDTErotWN5TmsYXJsWHkQfa6CyhuS4V3q,
        session.region_name,
        'es',
        session_token=credentials.token,
    )
    return awsauth

def search_photos_lex(query):
    # Call Amazon Lex for disambiguation
    
        lex_runtime = boto3.client('lexv2-runtime')
        random_session_id = generate_session_id()
        print("random id")
        print(random_session_id)
        lex_params = {
            'botId': 'RMKAROGAQ2',  # Replace with your Lex V2 bot ID
            'botAliasId': 'TSTALIASID',  # Replace with your Lex V2 bot alias ID
            'localeId': 'en_US',  # Replace with your bot's locale if needed
            'sessionId': 'ARP123',  # Create a unique session ID
            'text': query
        }

        lex_response = lex_runtime.recognize_text(**lex_params)

        #lex_message = lex_response.get('message', 'Lex bot did not respond.')
        lex_message = lex_response['messages'][0]['content']
        print(lex_response)
        print(lex_message)
    return response['slots'].values()

def search_opensearch(index_name, query, awsauth):
    awsauth = get_opensearch_auth()

    # Create an OpenSearch connection
    opensearch = OpenSearch(
        hosts=[https://search-photos-jsgbl4vz7jyakpja4uzrue2mbi.us-east-1.es.amazonaws.com],
        http_auth=awsauth,
        scheme="https",
        port=443,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    # Perform the search
    body = {
        "query": {
            "match": {
                "labels": " ".join(query)
            }
        }
    }

    response = opensearch.search(index=index_name, body=body)

    # Extract and return search results
    return [hit['_source'] for hit in response['hits']['hits']]

def lambda_handler(event, context):
    try:
        # Extract search query from Lex disambiguation
        query = search_photos_lex(event['queryStringParameters']['q'])

        # If keywords are found, search OpenSearch
        if query:
            index_name = 'photos'
            awsauth = get_opensearch_auth()  # Ensure to implement get_opensearch_auth() function
            results = search_opensearch(index_name, query, awsauth)
            return {
                'statusCode': 200,
                'body': json.dumps(results)
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps([])
            }
    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
