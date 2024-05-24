import os
import boto3
import json


autoscaling = boto3.client('autoscaling')

def lambda_handler(event, context):
    action = event.get('action')
    asgName = os.environ.get("asgName")

    ec2StartStopState = ec2StartStop(action,asgName)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully triggered')
    }


def ec2StartStop(action,asgName):
    if ('stop' == action):  
        response = autoscaling.update_auto_scaling_group(AutoScalingGroupName=asgName,MinSize=0,DesiredCapacity=0,MaxSize=0)
        response = autoscaling.update_auto_scaling_group(AutoScalingGroupName=asgName,MinSize=0,DesiredCapacity=0,MaxSize=0)
    elif (action == 'start'):
        response = autoscaling.update_auto_scaling_group(AutoScalingGroupName=asgName,MinSize=1,DesiredCapacity=1,MaxSize=1)
        response = autoscaling.update_auto_scaling_group(AutoScalingGroupName=asgName,MinSize=1,DesiredCapacity=1,MaxSize=1)