#results_archive.py
#archiving results files to glacier
#http://boto3.readthedocs.io/en/latest/reference/services/glacier.html


import boto3
import os
import json
import time
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

def archive_job(result_file_key=None):
    #find job in the dynamodb by job id
    #https://stackoverflow.com/questions/41833565/s3-buckets-to-glacier-on-demand-is-it-possible-from-boto3-api
    glacier_client = boto3.client('glacier', region_name=parser.get('configuration_variables', 'AWS_REGION_NAME'))
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(parser.get('configuration_variables', 'AWS_S3_RESULTS_BUCKET'))

    for obj in bucket.objects.filter(Prefix=result_file_key):
        response = glacier_client.upload_archive(vaultName=parser.get('configuration_variables', 'AWS_GLACIER_VAULT'),body=obj.get()['Body'].read())
        results_file_archive_id = response.get('archiveId')
        return results_file_archive_id

if __name__ == '__main__':
    #connect to SQS and get the message queue
    sqs = boto3.resource('sqs', region_name=parser.get('configuration_variables', 'AWS_REGION_NAME'))
    queue = sqs.get_queue_by_name(QueueName=parser.get('configuration_variables', 'AWS_SNS_JOB_ARCHIVE_QUEUE'))

    while True:
        messages = queue.receive_messages(WaitTimeSeconds=20)
        if(messages):
            for message in messages:
                #read message body
                body = json.loads(message.body)
                data = json.loads(body['Message'])
                job_id = data['job_id_archive']
                result_file_key = data['result_file_key']
                completion_time = data['completion_time']

                current_time = int(time.time())
                time_elapsed = current_time - completion_time
                print("elapsed time for job " + job_id + ": " + str(time_elapsed) + " seconds")
                if time_elapsed > parser.getint('configuration_variables', 'GLACIER_ARCHIVE_DELAY_IN_SECONDS'):
                    #check if user is still free (not upgraded during wait time)
                    dynamodb = boto3.resource('dynamodb', region_name=parser.get('configuration_variables', 'AWS_REGION_NAME'))
                    ann_table = dynamodb.Table(parser.get('configuration_variables', 'AWS_DYNAMODB_ANNOTATIONS_TABLE'))
                    try:
                        response = ann_table.get_item(Key={'job_id': job_id})
                    except Exception:
                        print('Error: failed to retrieve job information from database')
                    data = response.get('Item')
                    #if user is already premium, delete message and do nothing
                    if(data['user_role'] == 'premium_user'):
                        print('user is premium, deleting archive job request')
                        message.delete()
                    #if user is still free, go on with glacier archiving
                    else:
                        #archive file and get archived id
                        results_file_archive_id = archive_job(result_file_key=result_file_key)

                        #delete original file from S3
                        s3 = boto3.client('s3')
                        s3.delete_object(
                            Bucket=parser.get('configuration_variables', 'AWS_S3_RESULTS_BUCKET'),
                            Key=result_file_key,
                        )

                        #record archived ID in dynamodb
                        dynamodb = boto3.resource('dynamodb', region_name=parser.get('configuration_variables', 'AWS_REGION_NAME'))
                        ann_table = dynamodb.Table(parser.get('configuration_variables', 'AWS_DYNAMODB_ANNOTATIONS_TABLE'))
                        try:
                            ann_table.update_item(
                                Key = {'job_id': job_id},
                                UpdateExpression='SET results_file_archive_id = :val1, archived = :val2',
                                ExpressionAttributeValues={
                                    ':val1': results_file_archive_id,
                                    ':val2': 'true'
                                }
                            )
                        except Exception:
                            print('Error: failed to update database')

                        print("job " + job_id + " archived to Glacier")

                        #delete the message
                        message.delete()

        else:
            print("No notifications found")
