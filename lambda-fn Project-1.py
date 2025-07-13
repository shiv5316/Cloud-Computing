import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get all stopped EC2 instances
    response = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
    )

    instances_to_terminate = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state_transition_reason = instance.get('StateTransitionReason', '')

            # Format: 'User initiated (2025-07-11 05:10:45 GMT)'
            if 'User initiated' in state_transition_reason:
                try:
                    timestamp_str = state_transition_reason.split('(')[-1].strip(')')
                    stopped_time = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S %Z').replace(tzinfo=timezone.utc)
                    current_time = datetime.now(timezone.utc)

                    if current_time - stopped_time > timedelta(minutes=3):
                        instances_to_terminate.append(instance_id)
                except Exception as e:
                    print(f"Error parsing time for instance {instance_id}: {e}")

    if instances_to_terminate:
        print(f"Terminating instances: {instances_to_terminate}")
        ec2.terminate_instances(InstanceIds=instances_to_terminate)
    else:
        print("No stopped instances older than 5 minutes.")
