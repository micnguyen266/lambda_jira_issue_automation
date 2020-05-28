"""
This lambda function will create and post JIRA issues to your JIRA space based on EC2 health events. It uses JIRA's REST API and AWS CloudWatch Events to accomplish this.
Right now the user and pass are encoded in base64 it uses the users api token in the headers. In the future it be best to use AWS Parameter stores or KMS to make this more secure.
"""

from __future__ import print_function

import os
import logging
import pprint
import base64
from base64 import b64decode
import boto3
from boto3 import client
import urllib.request
from pprint import pprint
import json

# Setup Logger
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def lambda_handler(event, context):
    """
    Main Lambda function for handling events of AWS instance health
    """
    logger.info('Event: ' + str(event))
    instance_ids = event['resources']
    instance_name = ec2nametag(event,context)
    region = event['region']
    account = event['account']
    startTime = event['detail']['startTime']
    event_description = event['detail']['eventDescription'][0]['latestDescription']
    event_type_code = event['detail']['eventTypeCode']
    if event_type_code == 'AWS_EC2_PERSISTENT_INSTANCE_RETIREMENT_SCHEDULED':
        event_type_code = 'Retirement'
    else:
        event_type_code = 'Maintenance'

    # Set Values for Ticket
    issue_data = {
     "fields": {
     "labels": ['Scheduled-' + event_type_code],
     "project": {"key": os.environ['JIRA_PROJECT']},
     "summary": 'Stop-Start EC2 Instance ' + instance_name + ' ' + '(' + ''.join(instance_ids) + ')' + ' for Scheduled ' + event_type_code + ' | Region: ' + region + ' | Account: ' + account,
     "description": 'Start Time: ' + startTime + '\n' + '\n' + event_description + '\n' + '\n' + 'Please follow the steps outlined in this runbook: https://yourJIRAsite.com/.',
     "issuetype": {"name": os.environ['JIRA_ISSUETYPE_ID']},
     }
    }
    
    # JIRA payload
    url = "https://yourJIRAsite.com/rest/api/2/issue"
    
    headers = {
        "Authorization": "Basic %s" % '<CONVERT JIRA username:password | base64>',
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    data = json.dumps(issue_data).encode("utf-8")
    pprint(data)
    
    try:
        req = urllib.request.Request(url, data, headers)
        with urllib.request.urlopen(req) as f:
            res = f.read()
        pprint(res.decode())
    except Exception as e:
        pprint(e)
        
"""
Function to grab the "Name" tag value from the event resource instance ID.
"""        
def ec2nametag(event, context):
    tags = boto3.client('ec2')
    # tags = boto3.client('ec2', region_name='us-east-1')

    # Get all the tags associated with our EC2 instance
    instance_id = event['resources']
    response = tags.describe_tags (
        Filters=[
                {
                    'Name':'resource-id',
                    'Values':[
                        ''.join(instance_id)
                    ]
                },
            ]
        )
    # Iterate through and add the tags into a dictionary
    for tag in response['Tags']:
        #   print(tag['Key']) 
        if tag['Key'] == 'Name':
            return(tag['Value'])
    print("Error: Please check if there is a 'Name' tag for this instance.")
            
## Test Function    
def main_function(event, context):
    instance_name = ec2nametag(event,context)
    print("Start-Stop EC2 Instance",instance_name)

# To Test JIRA API
# curl -v https://yourJIRAsite.com/rest/api/2/issue --user username:password
# echo -n username:password | base64
