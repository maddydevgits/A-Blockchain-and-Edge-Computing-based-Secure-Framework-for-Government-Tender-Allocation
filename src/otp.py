import boto3
from botocore.exceptions import ClientError
import random

accessKey='' # ask admin to share accessKey
secretAccessKey='' # ask admin to share secret
region='us-east-1'

def verifyIdentity(a):
    client=boto3.client('ses',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    response = client.verify_email_identity(EmailAddress = a)
    print(response)

def sendotp(otp,sub,r):
    client=boto3.client('ses',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    SENDER = "otp.service@makeskilled.com"
    RECIPIENT = r
    SUBJECT = sub
    BODY_HTML = """<html>
        <head></head>
        <body>
        <h1>"""+SUBJECT+"""</h1>
        <p> Otp requested is """+str(otp)+""" .<br> <br>
        Thanks, <br>
        Make Skilled Dev Team <br>
        </p>
        </body>
        </html>
    """
    # The character encoding for the email.
    CHARSET = "UTF-8"
    try:
        #Provide the contents of the email.
        response = client.send_email(Destination={'ToAddresses': [RECIPIENT,],},
        Message={'Body': {'Html': {'Charset': CHARSET,'Data': BODY_HTML,},
        'Text': {'Charset': CHARSET,'Data': ""},},
        'Subject': {'Charset': CHARSET,'Data': SUBJECT,},},
        Source=SENDER)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        return True

def sendotp1(sub,r):
    client=boto3.client('ses',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)
    SENDER = "otp.service@makeskilled.com"
    RECIPIENT = r
    SUBJECT = sub
    BODY_HTML = """<html>
        <head></head>
        <body>
        <h1>"""+SUBJECT+"""</h1>
        <p> Your bid finalized, arrange meeeting for MoU """""" .<br> <br>
        Thanks, <br>
        Make Skilled Dev Team <br>
        </p>
        </body>
        </html>
    """
    # The character encoding for the email.
    CHARSET = "UTF-8"
    try:
        #Provide the contents of the email.
        response = client.send_email(Destination={'ToAddresses': [RECIPIENT,],},
        Message={'Body': {'Html': {'Charset': CHARSET,'Data': BODY_HTML,},
        'Text': {'Charset': CHARSET,'Data': ""},},
        'Subject': {'Charset': CHARSET,'Data': SUBJECT,},},
        Source=SENDER)
    except ClientError as e:
        print(e.response['Error']['Message'])
        return False
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        return True