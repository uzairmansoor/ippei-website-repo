import boto3
import os
import json

ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')
ssm = boto3.client('ssm')


def lambda_handler(event, context):
    
    json.dumps(event)
    instance_id = event['detail']['EC2InstanceId']
    instanceIdParameterStore = os.environ.get("instanceIdsParamStore")
    put_ssm_parameter(instance_id,instanceIdParameterStore)
    
    return {
    'statusCode': 200,
    'body': 'Successfully modified instance id'
}


def put_ssm_parameter(instance_id,param_name):
    return ssm.put_parameter(
        Name= param_name,
        Value = instance_id,
        Type = 'StringList',
        Overwrite = True
    )