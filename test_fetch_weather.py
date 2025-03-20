import sys
sys.path.append(r"C:\Users\Lihle\Downloads\GithubProjects\Project5\FetchWeatherData\package")
import FetchWeatherData

event = {}
context = None
result = FetchWeatherData.lambda_handler(event, context)
print(result)