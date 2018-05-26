#results_archive.py
#archiving results files to glacier


import boto3
import os
from ast import literal_eval
import json
import time

AWS_S3_RESULTS_BUCKET = "gas-results"
AWS_SNS_JOB_ARCHIVE_QUEUE = 'syun0_archive_jobs'
GLACIER_ARCHIVE_DELAY_IN_SECONDS = 10
AWS_GLACIER_VAULT = "ucmpcs"
AWS_S3_RESULTS_BUCKET = "gas-results"
AWS_REGION_NAME = os.environ['AWS_REGION_NAME'] if ('AWS_REGION_NAME' in  os.environ) else "us-east-1"
AWS_DYNAMODB_ANNOTATIONS_TABLE = "syun0_annotations"


def archive_job(result_file_key=None):
    #find job in the dynamodb by job id
    #https://stackoverflow.com/questions/41833565/s3-buckets-to-glacier-on-demand-is-it-possible-from-boto3-api
    glacier_client = boto3.client('glacier', region_name=AWS_REGION_NAME)
    s3 = boto3.resource('s3')

    bucket = s3.Bucket(AWS_S3_RESULTS_BUCKET)

    for obj in bucket.objects.filter(Prefix=result_file_key):
        response = glacier_client.upload_archive(vaultName=AWS_GLACIER_VAULT,body=obj.get()['Body'].read())
        results_file_archive_id = response.get('archiveId')
        return results_file_archive_id

if __name__ == '__main__':
    #connect to SQS and get the message queue
    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName=AWS_SNS_JOB_ARCHIVE_QUEUE)

    while True:
        messages = queue.receive_messages(WaitTimeSeconds=20)
        if(messages):
            for message in messages:
                #read message body
                body = literal_eval(message.body)
                data = literal_eval(body.get('Message'))
                job_id = data.get('job_id_archive')
                result_file_key = data.get('result_file_key')
                completion_time = data.get('completion_time')

                current_time = int(time.time())
                time_elapsed = current_time - completion_time
                if time_elapsed > GLACIER_ARCHIVE_DELAY_IN_SECONDS:
                    #archive file and get archived id
                    results_file_archive_id = archive_job(result_file_key=result_file_key)

                    #delete original file from S3
                    s3 = boto3.client('s3')
                    s3.delete_object(
                        Bucket=AWS_S3_RESULTS_BUCKET,
                        Key=result_file_key,
                    )

                    #record archived ID in dynamodb
                    try:
                        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
                        ann_table = dynamodb.Table(AWS_DYNAMODB_ANNOTATIONS_TABLE)
                    except Exception:
                        print("Failed to retrieve connect to database")

                    ann_table.update_item(
                        Key = {'job_id': job_id},
                        UpdateExpression='SET results_file_archive_id = :val1, archived = :val2',
                        ExpressionAttributeValues={
                            ':val1': results_file_archive_id,
                            ':val2': True
                        }
                    )

                    print("job " + job_id + " archived to Glacier")

                    #delete the message
                    message.delete()

        else:
            print("No notifications found")
