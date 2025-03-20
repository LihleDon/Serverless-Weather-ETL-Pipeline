import json
import requests
import boto3
import csv
import io
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # API key and city for weather data
    api_key = 'YOUR_API_KEY_HERE'  # Replace with your OpenWeatherMap API key
    city = 'Tokyo'  # Example city; can be parameterized later
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    # Fetch weather data
    response = requests.get(url)
    response.raise_for_status()  # Raise exception for bad responses
    weather_data = response.json()

    # Transform: Extract relevant fields
    date = datetime.utcnow().strftime('%Y-%m-%d')
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['date', 'city', 'temperature_celsius', 'humidity_percent', 'description'])
    writer.writerow([date, city, temp, humidity, description])
    csv_data = output.getvalue()
    output.close()

    # Upload to S3
    bucket_name = 'weather-data-bucket'
    file_key = f'raw/{date}/{city}_weather.csv'
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=csv_data)

    # Return for Step Functions
    return {
        'statusCode': 200,
        'body': json.dumps({
            'bucket': bucket_name,
            'key': file_key
        })
    }