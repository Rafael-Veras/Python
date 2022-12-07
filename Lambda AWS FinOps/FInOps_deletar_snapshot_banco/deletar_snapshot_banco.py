
import json

from datetime import datetime, timezone, timedelta
import boto3
import math

import requests

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
    validar_email = 0
    
    dolar = ValorDolar
    dolar.consulta(self=ValorDolar)
    dolar = (dolar.valor)
    

    email_body = "## Lista de snapshot de banco em (us-east-1) excluidos ## \n\n\n"

    client = boto3.client('rds',region_name="us-east-1")
    #client = boto3.client('rds', region_name="sa-east-1")


    sns_client = boto3.client('sns',region_name="us-east-1")



    snapshotbanco = client.describe_db_snapshots()

    print(snapshotbanco)

    total = 0
    for snapshot in snapshotbanco['DBSnapshots']:
        start_time = snapshot['SnapshotCreateTime']

        periodo_por_dias = 93
        delete_time = datetime.now(tz=timezone.utc) - timedelta(days=periodo_por_dias)



        if delete_time > start_time:
            client.delete_db_snapshot(DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'])
            tamanho = snapshot['AllocatedStorage']
            total = float(tamanho) + total
            email_body = email_body + "Snapshot deletado: " + str(snapshot['DBSnapshotIdentifier']) + " tamanho : " + str(tamanho) +" GB + \n"
            validar_email = 1

    custo = ((total * (0.095) * float(dolar) * (1.4)))
    custo = round(custo, 2)

    print("A economia com os snapshots excluidos foram de R$ " + str(custo) + " por mes")

    if validar_email == 1:
        email_body = email_body + "\n\nA economia com os snapshots excluidos foram de R$ " + str(custo) + " por mes\ntotal: " + str(total) + " GB"
        
        sns_arn = 'arn:aws:sns:us-east-1:xxxxx:xxxx'
        sns_client.publish(
            TopicArn=sns_arn,
            Subject='[FinOps] Snapshot excluidos de banco em US - Economia de: ' + str(custo),
            Message=email_body)

    '''
    total = 5
    custo = ((total * (0.05) * float(dolar) + (0.4)))

    
    '''
