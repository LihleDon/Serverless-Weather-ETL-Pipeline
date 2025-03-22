import boto3
import pandas as pd
from decimal import Decimal
import io

dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['key']

    # Download the CSV file from S3
    response = s3_client.get_object(Bucket=bucket, Key=key)
    csv_content = response['Body'].read().decode('utf-8')

    # Parse CSV content with pandas using io.StringIO
    df = pd.read_csv(io.StringIO(csv_content))

    # Get DynamoDB table
    table = dynamodb.Table('WeatherRecords')

    # Write each row to DynamoDB, converting floats to Decimal
    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = {
                'city': row['city'],
                'date': row['date'],
                'temperature': Decimal(str(row['temperature'])),
                'humidity': Decimal(str(row['humidity']))
            }
            batch.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': f'Successfully loaded {len(df)} records into DynamoDB'
    }