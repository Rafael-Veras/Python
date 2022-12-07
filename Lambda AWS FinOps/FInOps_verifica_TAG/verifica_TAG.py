import json
from datetime import datetime,timedelta
import boto3


from datetime import datetime

import os

ablb = boto3.client('elbv2')

lb = boto3.client('elb')

sns_client = boto3.client('sns')

ec2_client = boto3.client("ec2", region_name="us-east-1")

 
def lambda_handler(event, context):
    email_body = "## Lista de ambientes sem TAG na região (us-east-1) \n\n\n"
    sns_arn = 'arn:aws:sns:us-east-1:xxxx:xxxx'
    reservations = ec2_client.describe_instances()
    
    nomesInstances = []
    idInstances = []
    valorInstances = []
    email_nome = "*Instâncias que faltam a TAG Name* \n\n"
    email_ambiente = "*Instâncias que faltam a TAG Ambiente* \n\n"
    email_aplicacao = "*Instâncias que faltam a TAG Aplicacao* \n\n"
    email_area = "*Instâncias que faltam a TAG Area* \n\n"
    email_cliente = "*Instâncias que faltam a TAG Cliente* \n\n"
    email_produto = "*Instâncias que faltam a TAG Produto*\n\n"
    email_projeto = "*Instâncias que faltam a TAG Projeto* \n\n"
    email_tenant = "*Instâncias que faltam a TAG Tenant* \n\n"
    email_chamado = "*Instâncias que faltam a TAG Chamado* \n\n"
    nome_vetor = []
    ambiente_vetor = []
    aplicacao_vetor = []
    area_vetor = []
    cliente_vetor = []
    produto_vetor = []
    projeto_vetor = []
    tenant_vetor = []
    chamado_vetor = []

    for v in reservations['Reservations']:

        idInstances.append(v['Instances'][0]['InstanceId'])
         # v[Instances]['Tags']['Value']
        # print(v['Tags']['Value'])

        verificandoNome = 0
        verificandoAmbiente = 0
        verificandoAplicacao = 0
        verificandoArea = 0
        verificandoCliente = 0
        verificandoProduto = 0
        verificandoProjeto = 0
        verificandoTenant = 0
        verificandoChamado = 0
        nome_instancia_vai_no_email = ""



        contador = 0
        try:
            for a in v['Instances'][0]['Tags']:

                if str(a['Key']).lower() == "Name".lower():
                    nomesInstances.append(a['Value'])
                    nome_instancia_vai_no_email = a['Value']
                    verificandoNome = 1
                if str(a['Key']).lower() == "Ambiente".lower():
                    verificandoAmbiente = 1
                if str(a['Key']).lower() == "Aplicacao".lower():
                    verificandoAplicacao = 1
                if str(a['Key']).lower() == "Area".lower():
                    verificandoArea = 1
                if str(a['Key']).lower() == "Cliente".lower():
                    verificandoCliente = 1
                if str(a['Key']).lower() == "Produto".lower():
                    verificandoProduto = 1
                if str(a['Key']).lower() == "Projeto".lower():
                    verificandoProjeto = 1
                if str(a['Key']).lower() == "Tenant".lower():
                    verificandoTenant = 1
                if str(a['Key']).lower() == "Chamado".lower():
                    verificandoChamado = 1
        except:
            print("nothing")

        if verificandoNome == 0:
            nomesInstances.append("Nulo")
            email_nome = email_nome + "EC2-Instância de id  => " + str(v['Instances'][0]['InstanceId']) + "   \n"
        if verificandoAmbiente == 0:
            if nome_instancia_vai_no_email != "":
                if ambiente_vetor.__contains__(nome_instancia_vai_no_email):
                    continue
                else:
                    email_ambiente = email_ambiente + "EC2-Instância de Name   =>" + str(
                        nome_instancia_vai_no_email) + " \n"
                    ambiente_vetor.append(nome_instancia_vai_no_email)
            else:
                email_ambiente = email_ambiente + "EC2-Instância de id  => " + str(
                    v['Instances'][0]['InstanceId']) + "   \n"

        if verificandoAplicacao == 0:
            if nome_instancia_vai_no_email != "":
                if aplicacao_vetor.__contains__(nome_instancia_vai_no_email):
                    continue
                else:

                    email_aplicacao = email_aplicacao + "EC2-Instância de Name   =>" + str(
                        nome_instancia_vai_no_email) + " \n"
                    aplicacao_vetor.append(nome_instancia_vai_no_email)
            else:
                email_aplicacao = email_aplicacao + "EC2-Instância de id  => " + str(
                    v['Instances'][0]['InstanceId']) + "   \n"

        if verificandoArea == 0:
            if nome_instancia_vai_no_email != "":
                if area_vetor.__contains__(nome_instancia_vai_no_email):
                    continue
                else:
                    email_area = email_area + "EC2-Instância de Name   =>" + str(nome_instancia_vai_no_email) + " \n"
                    area_vetor.append(nome_instancia_vai_no_email)
            else:
                email_area = email_area + "EC2-Instância de id  => " + str(v['Instances'][0]['InstanceId']) + "   \n"

        if verificandoCliente == 0:
            if nome_instancia_vai_no_email != "":
                if cliente_vetor.__contains__(nome_instancia_vai_no_email):
                    continue
                else:
                    email_cliente = email_cliente + "EC2-Instância de Name   =>" + str(nome_instancia_vai_no_email) + " \n"
                    cliente_vetor.append(nome_instancia_vai_no_email)
            else:
                email_cliente = email_cliente + "EC2-Instância de id  => " + str(
                    v['Instances'][0]['InstanceId']) + "   \n"

        if verificandoProduto == 0:
            if nome_instancia_vai_no_email != "":
                if produto_vetor.__contains__(nome_instancia_vai_no_email):
                    continue
                else:
                    produto_vetor.append(nome_instancia_vai_no_email)
                    email_produto = email_produto + "EC2-Instância de Name   =>" + str(nome_instancia_vai_no_email) + " \n"
            else:
                email_produto = email_produto + "EC2-Instância de id  => " + str(
                    v['Instances'][0]['InstanceId']) + "   \n"

        if verificandoTenant == 0:
            if nome_instancia_vai_no_email != "":
                if tenant_vetor.__contains__(nome_instancia_vai_no_email):
                    continue
                else:
                    tenant_vetor.append(nome_instancia_vai_no_email)
                    email_tenant = email_tenant + "EC2-Instância de Name   =>" + str(nome_instancia_vai_no_email) + " \n"
            else:
                email_tenant = email_tenant + "EC2-Instância de id  => " + str(
                    v['Instances'][0]['InstanceId']) + "   \n"

        if verificandoChamado == 0:
            if nome_instancia_vai_no_email != "":
                if chamado_vetor.__contains__(nome_instancia_vai_no_email):
                    continue
                else:
                    chamado_vetor.append(nome_instancia_vai_no_email)
                    email_chamado = email_chamado + "EC2-Instância de Name   =>" + str(nome_instancia_vai_no_email) + " \n"
            else:
                email_chamado = email_chamado + "EC2-Instância de id  => " + str(
                    v['Instances'][0]['InstanceId']) + "   \n"

        contador = contador + 1
    email_body = email_body + email_nome
    email_body = email_body + "\n" + email_ambiente
    email_body = email_body + "\n" + email_aplicacao
    email_body = email_body + "\n" + email_area
    email_body = email_body + "\n" + email_cliente
    email_body = email_body + "\n" + email_produto

    email_body = email_body + "\n" + email_tenant
    email_body = email_body + "\n" + email_chamado
    validar_email = 0
    if nome_vetor != []:
        validar_email = 1

    if ambiente_vetor != []:
        validar_email = 1

    if aplicacao_vetor != []:
        validar_email = 1

    if area_vetor != []:
        validar_email = 1

    if cliente_vetor != []:
        validar_email = 1

    if produto_vetor != []:
        validar_email = 1

    if projeto_vetor != []:
        validar_email = 1

    if tenant_vetor != []:
        validar_email = 1

    if chamado_vetor != []:
        validar_email = 1


    if validar_email == 1:
        sns_client.publish(
                TopicArn=sns_arn,
                Subject='[FinOps] Instância sem TAG US',
                Message=email_body
            )
        

