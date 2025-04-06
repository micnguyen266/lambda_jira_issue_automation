### Jira Issue Automation with Lambda and CloudWatch

1. Create a CloudWatch Rule that looks up the events like in the cloudwatch_event_pattern.json file.
2. Create a Lambda function and add environment variables as necessary like `JIRA_PROJECT` and `JIRA_ISSUETYPE_ID`. 
Generate an API token in your JIRA service account and convert `username:api_key | base64` and insert in the headers.
3. Make sure to add the CloudWatch event as a trigger to the Lambda function.
4. Use the lambda_test_event.json file to make a test ticket. Please note in the event you would need to put an actual Instance ID as 
the ec2nametag function will look up the instance tags.
5. If things are not working make sure to setup the appropriate IAM roles.

### Instructions for Jira Issue EC2 Stop Start Automation (Not yet tested!)
1. Set Up AWS Health Integration with Amazon EventBridge

AWS Health provides notifications about scheduled events, such as EC2 instance retirements. To capture these events: ￼
	•	Create an EventBridge Rule:
	•	Navigate to the Amazon EventBridge console. ￼
	•	Create a new rule with a predefined pattern for AWS Health events. ￼
	•	Configure the event pattern to match EC2 retirement events.
	•	Set the target as an AWS Lambda function (which you’ll create in the next step).

This setup ensures that when AWS Health detects a scheduled EC2 retirement, it triggers the specified Lambda function.  

2. Develop the AWS Lambda Function

The Lambda function will handle the following tasks: ￼
	•	Parse the Event:
	•	Extract relevant details from the AWS Health event, such as the instance ID and retirement schedule. ￼
	•	Create a Jira Ticket:
	•	Use Jira’s REST API to create a new issue.
	•	Include details like the instance ID, retirement date, and any other pertinent information.
	•	Stop and Start the EC2 Instance:
	•	Utilize the AWS SDK (e.g., Boto3 for Python) to stop the affected EC2 instance.
	•	After confirming the stop operation, start the instance to migrate it to new hardware. ￼
	•	Update and Close the Jira Ticket:
	•	Once the instance is successfully restarted, update the Jira ticket with the outcome.
	•	Transition the ticket to a closed or resolved status.

3. Configure IAM Roles and Permissions

Ensure that the Lambda function has the necessary permissions: ￼
	•	EC2 Permissions:
	•	ec2:StopInstances ￼
	•	ec2:StartInstances ￼
	•	ec2:DescribeInstances
	•	CloudWatch Logs Permissions:
	•	logs:CreateLogGroup ￼
	•	logs:CreateLogStream ￼
	•	logs:PutLogEvents ￼

Attach these permissions to the Lambda function’s execution role to allow it to perform the required actions.

4. Securely Store Jira Credentials

To authenticate with Jira’s API:
	•	Use AWS Systems Manager Parameter Store:
	•	Store the Jira API token securely as an encrypted parameter.
	•	Grant the Lambda function permission to access this parameter.

This approach ensures that sensitive credentials are not hardcoded and are securely managed.

5. Testing and Validation

After setting up the components: ￼
	•	Simulate an EC2 Retirement Event:
	•	Manually trigger the Lambda function with a test event mimicking an AWS Health notification.
	•	Verify Jira Ticket Creation:
	•	Check Jira to confirm that the ticket is created with the correct details.
	•	Confirm EC2 Instance Operations:
	•	Ensure the specified EC2 instance is stopped and started as expected.
	•	Check Jira Ticket Updates:
	•	Verify that the ticket is updated and closed upon successful instance restart. ￼

By implementing this automation, you can efficiently manage EC2 retirement events, ensuring minimal manual intervention and maintaining accurate tracking through Jira.

To create a test event for AWS Health notifications, such as an EC2 instance retirement, you can simulate the event in your Lambda function without waiting for an actual retirement event. Here’s how to do it step-by-step:

Step 1: Sample AWS Health Event Payload
Use the following mock payload to simulate an EC2 retirement event:

You can replace i-0123456789abcdef0 with a real EC2 instance ID in your account if you’re testing for real behavior.

Step 2: Use the Lambda Test Console
	1.	Go to the AWS Lambda Console.
	2.	Choose your function (the one that processes EC2 retirement).
	3.	Click the “Test” button at the top.
	4.	Create a new test event:
	•	Name it something like EC2RetirementTest.
	•	Paste the mock event JSON from above.
	5.	Click “Save”, then click “Test” again to run it.

Your Lambda should now:
	•	Parse the fake event.
	•	Trigger the logic (e.g., create a Jira ticket, stop/start EC2 instance).
	•	Log actions to CloudWatch.

Step 3: Check Results
	•	Jira: Look for the new ticket and its updates.
	•	EC2 Console: Check if the specified instance was stopped and restarted.
	•	CloudWatch Logs: Verify the Lambda logs for output, errors, or flow confirmation.

### Author

Michael Nguyen https://github.com/micnguyen266