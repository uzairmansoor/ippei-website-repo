import boto3
import os
import json
import datetime

autoscaling = boto3.client('autoscaling')
ec2 = boto3.client('ec2')
ssm = boto3.client('ssm')


def lambda_handler(event, context):
    
    instanceIdParameterStore = os.environ.get("instanceIdsParamStore")
    instance_id = get_ssm_parameter(instanceIdParameterStore).split(',')[0]
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    ami_name = os.environ.get("project") + "-" + os.environ.get("env") + "-" + os.environ.get('AWS_REGION') + "-" + f"{formatted_datetime}"
    ami_id = create_ami(instance_id, ami_name, formatted_datetime)

    return {
        'statusCode': 200,
        'body': 'Successfully created AMI'
    }


def get_ssm_parameter(param_name):
    return ssm.get_parameter(
        Name = param_name
    )['Parameter']['Value']


def create_ami(instance_id, ami_name, date_time):
    return ec2.create_image(
        InstanceId = instance_id,
        Name = ami_name,
        TagSpecifications=[
            {
                'ResourceType': 'image',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': ami_name
                    },
                    {
                        'Key': 'created_at',
                        'Value': date_time
                    },
                    {
                        'Key': 'project',
                        'Value': os.environ.get("project")
                    },
                    {
                        'Key': 'env',
                        'Value': os.environ.get("env")
                    }
                ]
            }
        ]
    )['ImageId']