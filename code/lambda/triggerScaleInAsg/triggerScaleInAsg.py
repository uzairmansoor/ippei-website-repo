import os
import boto3
import json

cloudwatch = boto3.client('cloudwatch')
autoscaling = boto3.client('autoscaling')


def lambda_handler(event, context):
    
    cloudwatch_alarms = get_cloudwatch_alarms()
    alarm_states = {}
    for alarm in cloudwatch_alarms['MetricAlarms']:
        alarm_name = alarm['AlarmName']
        state_value = alarm['StateValue']
        alarm_states[alarm_name] = state_value
        print(f"Alarm Name: {alarm_name}, StateValue: {state_value}")
    
    if all(state == 'ALARM' for state in alarm_states.values()) and 'INSUFFICIENT_DATA' not in alarm_states.values():
        print("Both alarms are in ALARM state. Triggering Auto Scaling group scale-in.")
        trigger_scale_in()
    else:
        print("At least one alarm is not in ALARM state. No action taken.")
   
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully triggered ScaleIn policy!')
    }


def get_cloudwatch_alarms():
    response = cloudwatch.describe_alarms(
        AlarmNames=['cloudweb-prod-cpuScaleInAlarm-us-east-1', 'cloudweb-prod-ec2FreeMemScaleInAlarm-us-east-1']
    )
    return response


def trigger_scale_in():
    autoscaling.execute_policy(
        AutoScalingGroupName=os.environ.get("asgName"),
        PolicyName=os.environ.get("scaleInPolicyName"),
        MetricValue=50,
        BreachThreshold=50
    )
