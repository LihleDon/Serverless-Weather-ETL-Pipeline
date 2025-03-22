# Serverless Weather ETL Pipeline

A serverless Extract, Transform, Load (ETL) pipeline built using AWS Serverless Application Model (SAM). It fetches daily weather data for Tokyo from the OpenWeatherMap API, stores it as a CSV in Amazon S3, and loads it into Amazon DynamoDB. The pipeline runs automatically every day via a CloudWatch Events rule.

## Architecture
- **AWS CloudWatch Events**: Triggers the pipeline daily using a scheduled rule (`rate(1 day)`).
- **AWS Step Functions**: Orchestrates the workflow with two states:
  - **FetchWeatherData**: A Lambda function that retrieves weather data (temperature and humidity) for Tokyo, saves it as a CSV in S3, and passes the file location to the next step.
  - **LoadToDynamoDB**: A Lambda function that reads the CSV from S3 and writes the data to DynamoDB.
- **Amazon S3**: Stores raw weather data as CSV files (e.g., `lihle-weather-data-bucket-2025/raw/YYYY-MM-DD/Tokyo_weather.csv`).
- **Amazon DynamoDB**: Stores processed weather records in a table named `WeatherRecords` with a composite key (`city` and `date`).

## Prerequisites
- **AWS Account**: Configured with AWS CLI (`aws configure`).
- **AWS SAM CLI**: Installed (see [AWS SAM CLI Installation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)).
- **OpenWeatherMap API Key**: Sign up at [OpenWeatherMap](https://openweathermap.org/), generate an API key, and add it to `FetchWeatherData/FetchWeatherData.py`.
- **Git**: Installed to clone the repository.

## Project Structure

├── FetchWeatherData/
│   ├── FetchWeatherData.py    # Lambda function to fetch weather data and save to S3
│   └── requirements.txt       # Dependencies: requests, pandas
├── LoadToDynamoDB/
│   ├── LoadToDynamoDB.py      # Lambda function to load CSV data into DynamoDB
│   └── requirements.txt       # Dependency: pandas
├── template.yaml              # SAM template defining all AWS resources
└── README.md                  # This documentation file


## Setup Instructions

1. **Clone the Repository**:
2. **Insert Your API Key**:
- Open the `FetchWeatherData.py` file:
  ```
  code FetchWeatherData/FetchWeatherData.py
  ```
- Find the line `api_key = "your_actual_api_key_here"`.
- Replace `"your_actual_api_key_here"` with your OpenWeatherMap API key (e.g., `api_key = "abc123def456ghi789"`).
- Save and close the file.
3. **Build the Application**:
- This command installs the dependencies listed in `requirements.txt` files and prepares the deployment package.
4. **Deploy to AWS**:
- Follow the interactive prompts:
  - **Stack Name**: Enter `WeatherETLPipeline`.
  - **Region**: Enter `af-south-1`.
  - **Confirm Changeset**: Type `y` to approve the changes.
  - **Capabilities**: Accept `CAPABILITY_IAM` for IAM role creation.
- Wait until you see “Successfully created/updated stack - WeatherETLPipeline in af-south-1”.

## Running the Pipeline

- **Manual Trigger**:
  - Open the AWS Console, navigate to Step Functions in the `af-south-1` region.
  - Find `WeatherETLStateMachine-2pV7SlFD7TSW`, click “Start Execution.”
  - In the input box, leave it as `{}` (default), and click “Start Execution.”
- **Automatic Trigger**: The pipeline runs daily at a fixed time, managed by the CloudWatch Events rule.
- **Verify Output**:
  - **S3**: Check the bucket `lihle-weather-data-bucket-2025` for a file like `raw/YYYY-MM-DD/Tokyo_weather.csv`.
  - **DynamoDB**: Open the `WeatherRecords` table and look for an entry (e.g., `city: Tokyo, date: YYYY-MM-DD, temperature: 15.0, humidity: 70`).

## Troubleshooting

- **View Logs**: Check CloudWatch Logs in the `af-south-1` region:
  - `/aws/lambda/WeatherETLPipeline-FetchWeatherDataFunction-<random>` for API fetch issues.
  - `/aws/lambda/WeatherETLPipeline-LoadToDynamoDBFunction-<random>` for DynamoDB load issues.
- **Common Problems**:
  - **Invalid API Key**: If the API call fails, update the key in `FetchWeatherData.py` and redeploy.
  - **Missing Dependencies**: Ensure `requirements.txt` files exist in both `FetchWeatherData/` and `LoadToDynamoDB/`.

## Cleanup

To remove all AWS resources and avoid charges:
aws cloudformation delete-stack --stack-name WeatherETLPipeline --region af-south-1
aws cloudformation wait stack-delete-complete --stack-name WeatherETLPipeline --region af-south-1


## Future Enhancements

- Parameterize the city name to fetch data for multiple locations.
- Include additional weather metrics like wind speed or pressure.
- Add error handling with Amazon SNS notifications for failures.