import boto3
import requests
import json
import os

# Initialize AWS and Jira clients
ec2 = boto3.client('ec2')
jira_url = os.environ['JIRA_URL']
jira_user = os.environ['JIRA_USER']
jira_api_token = os.environ['JIRA_API_TOKEN']
jira_project = os.environ['JIRA_PROJECT']
jira_issue_type = os.environ['JIRA_ISSUE_TYPE']


def lambda_handler(event, context):
    # Extract instance ID from the AWS Health event
    instance_id = event['detail']['affectedEntities'][0]['entityValue']

    # Create Jira ticket
    jira_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {jira_user}:{jira_api_token}'
    }
    jira_payload = {
        'fields': {
            'project': {'key': jira_project},
            'summary': f'EC2 Instance {instance_id} Scheduled for Retirement',
            'description': f'AWS has scheduled the EC2 instance {instance_id} for retirement.',
            'issuetype': {'name': jira_issue_type}
        }
    }
    response = requests.post(f'{jira_url}/rest/api/2/issue', headers=jira_headers, data=json.dumps(jira_payload))
    jira_issue_key = response.json().get('key')

    # Stop the EC2 instance
    ec2.stop_instances(InstanceIds=[instance_id])
    waiter = ec2.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])

    # Start the EC2 instance
    ec2.start_instances(InstanceIds=[instance_id])
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])

    # Update and close Jira ticket
    update_payload = {
        'fields': {
            'resolution': {'name': 'Done'}
        },
        'transition': {
            'id': '31'  # Transition ID for closing the issue; may vary based on your Jira workflow
        }
    }
    requests.post(f'{jira_url}/rest/api/2/issue/{jira_issue_key}/transitions', headers=jira_headers,
                  data=json.dumps(update_payload))