#archive_restore.py
#restoring results files from glacier
#http://boto3.readthedocs.io/en/latest/reference/services/glacier.html

import boto3
import os
import json
import time
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

if __name__ == '__main__':
    #connect to SQS and get the message queue
    sqs = boto3.resource('sqs', region_name=parser.get('configuration_variables', 'AWS_REGION_NAME'))
    queue = sqs.get_queue_by_name(QueueName=parser.get('configuration_variables', 'AWS_SNS_JOB_RETRIEVE_QUEUE'))

    while True:
        messages = queue.receive_messages(WaitTimeSeconds=20)
        if(messages):
            for message in messages:
                #read message body
                body = json.loads(message.body)
                data = json.loads(body['Message'])
                result_file_key = data['JobDescription']
                retrieval_job_id = data['JobId']

                #download job contents from glacier
                glacier_client = boto3.client('glacier', region_name=parser.get('configuration_variables', 'AWS_REGION_NAME'))
                try:
                    response = glacier_client.get_job_output(
                        vaultName=parser.get('configuration_variables', 'AWS_GLACIER_VAULT'),
                        jobId=retrieval_job_id
                    )
                except Exception:
                    print('Error: failed to retrieve job contents from Glacier')
                result_file = response['body']

                #upload response to s3
                s3 = boto3.client('s3', region_name=parser.get('configuration_variables', 'AWS_REGION_NAME'))
                bucket_name = parser.get('configuration_variables', 'AWS_S3_RESULTS_BUCKET')
                try:
                    s3.upload_fileobj(result_file, bucket_name, result_file_key)
                except Exception:
                    print('Error: failed to upload results file to S3 bucket')

                #edit database entry
                #extract job_id from results file key
                split_key = result_file_key.split("/")
                job_id = split_key[2]

                #record restored ID in dynamodb
                dynamodb = boto3.resource('dynamodb', region_name=parser.get('configuration_variables', 'AWS_REGION_NAME'))
                ann_table = dynamodb.Table(parser.get('configuration_variables', 'AWS_DYNAMODB_ANNOTATIONS_TABLE'))
                try:
                    ann_table.update_item(
                        Key = {'job_id': job_id},
                        UpdateExpression='SET results_file_archive_id = :val1, archived = :val2',
                        ExpressionAttributeValues={
                            ':val1': None,
                            ':val2': 'false'
                        }
                    )
                except Exception:
                    print('Error: failed to update annotations database')

                print("job " + job_id + " restored from Glacier")

                #delete the message
                message.delete()
        else:
            print("No notifications found")
