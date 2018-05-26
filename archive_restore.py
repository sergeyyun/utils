#archive_restore.py
#restoring results files from glacier

import boto3
import os
import json
import time

AWS_S3_RESULTS_BUCKET = "gas-results"
AWS_SNS_JOB_RETRIEVE_QUEUE = 'syun0_retrieval'
AWS_GLACIER_VAULT = "ucmpcs"
AWS_REGION_NAME = os.environ['AWS_REGION_NAME'] if ('AWS_REGION_NAME' in  os.environ) else "us-east-1"
AWS_DYNAMODB_ANNOTATIONS_TABLE = "syun0_annotations"

if __name__ == '__main__':
    #connect to SQS and get the message queue
    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName=AWS_SNS_JOB_RETRIEVE_QUEUE)

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
                glacier_client = boto3.client('glacier', region_name=AWS_REGION_NAME)
                response = glacier_client.get_job_output(
                    vaultName=AWS_GLACIER_VAULT,
                    jobId=retrieval_job_id
                )
                result_file = response['body']

                #upload response to s3
                s3 = boto3.client('s3', region_name=AWS_REGION_NAME)
                bucket_name = AWS_S3_RESULTS_BUCKET
                s3.upload_fileobj(result_file, bucket_name, result_file_key)

                #edit database entry
                #extract job_id from results file key
                split_key = result_file_key.split("/")
                job_id = split_key[2]

                #record restored ID in dynamodb
                try:
                    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION_NAME)
                    ann_table = dynamodb.Table(AWS_DYNAMODB_ANNOTATIONS_TABLE)
                except Exception:
                    print("Failed to retrieve connect to database")

                ann_table.update_item(
                    Key = {'job_id': job_id},
                    UpdateExpression='SET results_file_archive_id = :val1, archived = :val2',
                    ExpressionAttributeValues={
                        ':val1': None,
                        ':val2': 'false'
                    }
                )

                print("job " + job_id + " restored from Glacier")

                message.delete()
        else:
            print("No notifications found")
