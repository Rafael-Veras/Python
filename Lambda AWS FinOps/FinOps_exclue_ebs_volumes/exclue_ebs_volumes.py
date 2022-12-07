import json
import boto3
from datetime import datetime, timedelta, timezone
 #import smtplib

def lambda_handler(event, context):
     
    ec2_client = boto3.client('ec2')
    sns_client = boto3.client('sns')

    volumes = ec2_client.describe_volumes()
    sns_arn = 'arn:aws:sns:sa-east-1:xxxxxx:xxxx'

    unsed_vols = []
    for volume in volumes['Volumes']:
        if len(volume['Attachments']) == 0:
            unsed_vols.append(volume['VolumeId'])
            print(volume)
            print("----"*5)

    email_body = "## Lista de volumes (us-east-1) em estado available que serao excluidos## \n\n\n"
    validar_email = 0
    for vol in unsed_vols:
        email_body = email_body + "VolumeId = {} \n".format(vol)
        ec2_client.delete_volume(VolumeId=vol)
        validar_email = 1

    # Envio de email
    if validar_email == 1:
        sns_client.publish(
            TopicArn = sns_arn,
            Subject = '[FinOps] Volumes nao usados - available BR',
            Message = email_body
        ) 
    #print(email_body)
    
    #Delete volumes
    #ec2_client.delete_volume(VolumeId="vol-0616d6346547b7809")


    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(email_body)
    }

