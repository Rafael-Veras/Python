import boto3
import collections
from datetime import datetime


ablb = boto3.client('elbv2')
lb = boto3.client('elb')
sns_client = boto3.client('sns')


def lambda_handler(event, context):

  email_body = "## Lista de possíveis balanceadores sem uso na região (us-east-1) \n\n\n"
  validar_email = 0
  sns_arn = 'arn:aws:sns:us-east-1:xxxxx:xxx'
  #print(response)
  responseAlb = ablb.describe_load_balancers() 
  for v in responseAlb['LoadBalancers']:
    if v['State']['Code'] != 'active':
      v['LoadBalancerArn']
      print('ALB-ARN:' , v['LoadBalancerArn'])
      v['LoadBalancerName']
      print('ALB-Nome:' , v['LoadBalancerName'])
      print('ALB-State:' , v['State']['Code'])
      email_body = email_body + "ALB-LoadBalancerName =>  "+ v['LoadBalancerName'] + "\n" 
      validar_email = 1
      

  responseLb = lb.describe_load_balancers()  
  for v in responseLb['LoadBalancerDescriptions']:
    if len(v['Instances']) == 0: 
     v['LoadBalancerName']
     print('LB-Nome:' , v['LoadBalancerName'])
     v['Instances']
     print('LB-Instances:' ,v['Instances'])
     email_body = email_body + "LB-LoadBalancerName =>  " + v['LoadBalancerName'] + "\n" 
     validar_email = 1
  if validar_email == 1:
      sns_client.publish(
            TopicArn = sns_arn,
            Subject = '[FinOps] Possível LB sem uso US',
            Message = email_body
        ) 
    
       

   #for v in response['LoadBalancers']:
   # if v['State']['Code'] != 'active':
    #print('State:' , v['State']['Code'])
   #print('Type:' , v['Type'])

if __name__ == '__main__':
    main()


