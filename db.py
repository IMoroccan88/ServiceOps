# Starting necessary service and connecting to the DB.


import psycopg
import boto3
import json

def get_db_connection():

    # Create a connection client for AWS Secrets Manager in us-east-2.

    secrets_client = boto3.client(
        "secretsmanager",
        region_name="us-east-2"
    )   


    # "Secrets Manager, give me the secret named ServiceOps/RDS/Credentials."
    secret_response = secrets_client.get_secret_value(
    SecretId="ServiceOps/RDS/Credentials"
    )

    # "Turn the secret text into something Python can read by key name."
    secret = json.loads(secret_response["SecretString"])



    # to connect to our RDS PostgreSQL database."
    connection = psycopg.connect(
    host=secret["host"],
    dbname=secret["dbname"],
    user=secret["username"],
    password=secret["password"],
    port=secret["port"]
    )

    # Return the database connection to whichever route requested it.
    return connection
