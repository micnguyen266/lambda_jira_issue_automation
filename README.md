### Jira Issue Automation with Lambda and CloudWatch

1. Create a CloudWatch Rule that looks up the events like in the cloudwatch_event_pattern.json file.
2. Create a Lambda function. Generate an API token in your JIRA service account and convert `username:api_key | base64` 
and insert in the headers.
3. Make sure to add the CloudWatch event as a trigger to the Lambda function.
4. Use the lambda_test_event.json file to make a test ticket. Please note in the event you would need to put an actual Instance ID as 
the ec2nametag function will look up the instance tags.
5. If things are not working make sure to setup the appropriate IAM roles.