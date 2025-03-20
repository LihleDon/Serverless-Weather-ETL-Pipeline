import json
import boto3
import csv
import io

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Get S3 details from the previous step (FetchWeatherData)
    body = json.loads(event['body'])
    bucket = body['bucket']
    key = body['key']

    # Read CSV from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    csv_data = response['Body'].read().decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_data))

    # Load into DynamoDB
    table = dynamodb.Table('WeatherRecords')
    for row in csv_reader:
        table.put_item(
            Item={
                'city': row['city'],
                'date': row['date'],
                'temperature_celsius': float(row['temperature_celsius']),
                'humidity_percent': int(row['humidity_percent']),
                'description': row['description']
            }
        )

    # Return success
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data loaded into DynamoDB'})
    }