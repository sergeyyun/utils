import boto3
import os
import json
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

def send_email_ses(recipients=None,
  sender=None, subject=None, body=None):

  ses = boto3.client('ses', region_name=parser.get('configuration_variables', 'AWS_REGION_NAME'))

  response = ses.send_email(
    Destination = {'ToAddresses': recipients},
    Message={
      'Body': {'Text': {'Charset': "UTF-8", 'Data': body}},
      'Subject': {'Charset': "UTF-8", 'Data': subject},
    },
    Source=sender)
  return response['ResponseMetadata']['HTTPStatusCode']

if __name__ == '__main__':
    #connect to SQS and get the message queue
    sqs = boto3.resource('sqs', region_name='us-east-1')
    queue = sqs.get_queue_by_name(QueueName=parser.get('configuration_variables', 'AWS_SNS_JOB_NOTIFICATION_QUEUE'))

    while True:
        messages = queue.receive_messages(WaitTimeSeconds=20)
        if(messages):
            for message in messages:
                #read message body
                body = json.loads(message.body)
                data = json.loads(body['Message'])
                job_id = data['job_id_complete']
                user_email = data['user_email'],

                #construct the email subject and body
                link = "https://syun0.ucmpcs.org:4433/annotations/" + job_id
                subject = "GAS notification: job complete"
                body = "Annotation job " + job_id + " is complete" + "\n" + "To view annotation job, click on the following link: " + link

                #send the email
                send_email_ses (recipients=user_email, sender=parser.get('configuration_variables', 'MAIL_DEFAULT_SENDER'), subject=subject, body=body)
                print("Email notification sent")

                #delete the message
                message.delete()

        else:
            print("No notifications found")
