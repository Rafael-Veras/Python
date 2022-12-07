# import cloudwatch

from os import name
import threading
from datetime import datetime,timedelta

import boto3

import collections

from datetime import datetime

import os


ablb = boto3.client('elbv2')

lb = boto3.client('elb')

sns_client = boto3.client('sns')

ec2_client = boto3.client("ec2", region_name="us-east-1")



#Função para pegar o json dos valores de cloudwatch, o quanto a máquina usa de cpu e de internet.
def pegarValores(instanceId,metrica):
    client = boto3.client('cloudwatch', region_name="us-east-1")
    paginator = client.get_metric_statistics(
            Period=3600*6,
            StartTime=datetime.utcnow() - timedelta(hours=6),
            EndTime=datetime.utcnow(),
            MetricName=metrica,
            Namespace='AWS/EC2',
            Statistics=['Average'],
            Dimensions=[{'Name':'InstanceId', 'Value':str(instanceId)}]
            )

    return paginator

#aqui pega o nome da instancia, o id, e o valor
def codigo(nome,id,a):
    contador = -1
    vetorNome = []
    vetorQuantidade = []
    email_body = ""
    arquivo_escrito = ""

    for b in a:
        contador = contador + 1
        if b == "Nulo":

            if vetorNome.__contains__(nome[contador]):
                print("tem")
            else:
                vetorNome.append(nome[contador])
                vetorQuantidade.append(1)
    print(vetorQuantidade)
    print(vetorNome)
    i = -1
    for nome in vetorNome:
        i = i + 1
        validarAlteracao = 0

       
        texto_escrever = ""
        validar_enviar_email = 0


        bucket_name = 'xxxxxx-finops'
        file_name = "VerificaAmbiente/networkingUS.txt"
        

        s3 = boto3.resource("s3")
        obj = s3.Object(bucket_name,file_name)
        #body = obj.get()['Body'].read().decode()
    
        
        for linha in obj.get()['Body']._raw_stream:
            linha_texto = ""
            contador = 0
            numero = ""
            for linha_parte in linha:
                if contador == 1 :
                    numero = numero + chr(linha_parte)
                if contador == 0:
                    linha_texto = linha_texto + chr(linha_parte)
                if chr(linha_parte) == ",":
                    contador = 1




            if str(linha_texto) == str(nome) + ",":
                numero = int(numero) + 1
                linha_email = linha_texto
                linha_texto = linha_texto + str(numero)
                texto_escrever = texto_escrever + linha_texto
                print(linha_texto)
                if str(nome) != "Nulo":
                    arquivo_escrito = arquivo_escrito + str(linha_texto) + "\n"
                if numero > 4:
                    if str(nome) != "Nulo":
                        email_body = email_body + "EC2-Instância =>  " + str(linha_email) + "\n"
                        validar_enviar_email = 1
                        print(email_body)
                if str(nome) != "Nulo":
                    validarAlteracao = 1

            else:
                linha_texto = linha_texto + str(numero)

                texto_escrever = texto_escrever + linha_texto


        if validarAlteracao == 0:
            arquivo_escrito = arquivo_escrito + str(nome) + ","+ str(1) + "\n"
           
            print(arquivo_escrito)

        

    encoded_string = arquivo_escrito.encode("utf-8")
    s3.Bucket(bucket_name).put_object(Key=file_name, Body=encoded_string)
    return email_body,validar_enviar_email

   




def lambda_handler(event, context):
    
    email_body = "## Lista de possíveis ambientes que estão ociosos na região (us-east-1) \n\n\n"
    sns_arn = 'arn:aws:sns:us-east-1:xxxxx:xxx'

    
 
    
    reservations = ec2_client.describe_instances()
    nomesInstances = []
    idInstances = []
    valorInstances = []

    for v in reservations['Reservations']:

        idInstances.append(v['Instances'][0]['InstanceId'])
        # v[Instances]['Tags']['Value']
        # print(v['Tags']['Value'])

        verificandoNome = 0
        for a in v['Instances'][0]['Tags']:

            if str(a['Key']) == "Name":
                nomesInstances.append(a['Value'])
                verificandoNome = 1
                print(a['Value'])

        if verificandoNome == 0:
            nomesInstances.append("Nulo")

    print(nomesInstances)
    print(idInstances)
    print(len(nomesInstances))
    print(len(idInstances))

    metricas = ["NetworkIn", "NetworkOut", "CPUUtilization"]

    for instances in idInstances:
        dados = pegarValores(instances, "NetworkIn")
        # contador = 0
        try:
            print(str(dados["Datapoints"][0]['Average']) != "")
            valorInstances.append(dados["Datapoints"][0]['Average'])
        except:

            valorInstances.append("Nulo")
    
    '''
        for b in dados["Datapoints"]:
            valorInstances.append(b["Average"])
            print(b["Average"])
            contador = contador + 1

    '''
    
    print(valorInstances)
    print(len(valorInstances))
    body,validar_enviar_email=codigo(nomesInstances,idInstances,valorInstances)
    email_body = email_body + body

    print(email_body)
    if validar_enviar_email == 1:
        sns_client.publish(
            TopicArn=sns_arn,
            Subject='[FinOps] Possível Instância sem uso US',
            Message=email_body
        )

    

    

    # for reservation in reservations:
    # for instance in reservation[]:
    #   print(instance[Tags])

    #    instance_id = instance["InstanceId"]
    #    instance_type = instance["InstanceType"]
    #    print(f"{instance_id}, {instance_type}")
    #    for instance in reservation["Groups"]:
    #        GroupName = instance["GroupName"]
    #        print(f"{GroupName}")


