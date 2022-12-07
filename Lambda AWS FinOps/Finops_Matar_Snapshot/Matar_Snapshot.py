import json
import boto3
import requests
import math
from datetime import datetime, timezone, timedelta

#from dolar import ValorDolar

class ValorDolar():

    def __init__(self):
        self.valor = -1

    def consulta(self):
        url = "https://economia.awesomeapi.com.br/json/all/USD-BRL"
        retorno = requests.get(url)
        if (retorno.status_code==200):
            jsonparsed = retorno.json()
            #print(jsonparsed)
            self.valor = jsonparsed['USD']['high']
        else:
            self.valor = -1

def lambda_handler(event, context):
    email_body = "## Lista de snapshot em (us-east-1) excluidos ## \n\n\n"

    dolar = ValorDolar
    dolar.consulta(self=ValorDolar)
    dolar = (dolar.valor)
    validar_email = 0
    
    #Period é a quantidade de dias para usar como filtro e selecionar apenas a AMI ou Snap que deseja
    periodo_por_dias = 30
    
    ec2 = boto3.resource('ec2')
    c = boto3.client('ec2')
    sns_client = boto3.client('sns')
    snapshots = ec2.snapshots.filter(OwnerIds=['self'])
    sns_client = boto3.client('sns')
    total = 0
    
    print("## LISTA DE SNAP EXCLUIDOS ##\n")
    
    for snapshot in snapshots:
        start_time = snapshot.start_time
        delete_time = datetime.now(tz=timezone.utc) - timedelta(days = periodo_por_dias)
        
        response = c.describe_snapshots(
                SnapshotIds=[
                str(snapshot.snapshot_id),
            ],
            
        )
        if delete_time > start_time:
            
            try:
                snapshot.delete()
                print("Deletado: ")
            except:
                pass
            #print(start_time, delete_time)        
            
            #Aqui desassocio a AMI - Em ImageId - Informar a AMI depois de se assegurar que realmente pode apagar
            #response = c.deregister_image(DryRun=False, ImageId = 'ami-1a5b5a70')
        
             #snapshot.delete()
     
        

            for variavel in response['Snapshots']:
                total = (variavel['VolumeSize']) + total
                email_body = email_body + 'Tamanho do Volume : '  + str(variavel['VolumeSize']) +  ' e ' + "Volume ID: " + str(variavel['VolumeId']) + '\n'
                validar_email = 1
                print('Tamanho do Volume : ' , variavel['VolumeSize'], ' e ' + str("Volume ID: "), variavel['VolumeId'])
            
        
               
            
    print(total)
    email_body = email_body + "\nO tamanho do disco foi de: " + str(total) + "\n\n"
    custo = ((total * (0.095) * float(dolar) * (1.4)))
    custo = math.ceil(custo)
    
    
    print("A economia com os snapshots excluidos foram de R$ {:0.2f} por mes".format(custo))
    email_body = email_body + "A economia com os snapshots excluidos foram de R$ "+ str(custo) + " por mes"
     
    
    sns_arn = 'arn:aws:sns:us-east-1:xxxxx:xxxx'
    if validar_email == 1:
        sns_client.publish(
                TopicArn = sns_arn,
                Subject = '[FinOps] Snapshot excluidos em US - Economia de: ' + custo,
                Message = email_body)
        
    
    
    
    
    # TODO implement
    return {
        'statusCode': 200,
        
    }

