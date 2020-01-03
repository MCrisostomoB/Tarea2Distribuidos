#!/usr/bin/env python
import pika
import sys
import json
import os

if not os.path.exists('logs'):
    os.mkdir('logs')
if not os.path.exists('logs/log.txt'):
    f = open('logs/log.txt',"w+")
    f.close()
if not os.path.exists('logs/cuentas.txt'):
    f = open('logs/cuentas.txt',"w+")
    f.close()
file = open("./logs/log.txt","r")
filec = open("./logs/cuentas.txt","r")
clientesraw = filec.readlines()
msjs = file.readlines()

clientes ={'id' : [] , 'usuario':[],'password':[]}
mensajes = {'id':[],'from':[],'to':[],'mensaje':[],'fecha':[]}
for i in clientesraw:
    spliteo = i.split("#")
    clientes['id'].append(spliteo[0])
    clientes['usuario'].append(spliteo[1])
    clientes['password'].append(spliteo[2])
for i in msjs:
    spliteo = i.split("#")
    mensajes['id'].append(spliteo[0])
    mensajes['from'].append(spliteo[1])
    mensajes['to'].append(spliteo[2])
    mensajes['mensaje'].append(spliteo[3])
    mensajes['fecha'].append(spliteo[4])

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='ec-s', exchange_type='direct')

result = channel.queue_declare(queue='registro/login')

channel.queue_bind(exchange='ec-s', queue='registro/login', routing_key="login")
channel.queue_bind(exchange='ec-s', queue='registro/login', routing_key="registro")
channel.queue_bind(exchange='ec-s', queue='registro/login', routing_key="mensajes")
channel.queue_bind(exchange='ec-s', queue='registro/login', routing_key="mensajes2")

channel.queue_bind(exchange='ec-s', queue='registro/login', routing_key="usuarios")
channel.queue_bind(exchange='ec-s', queue='registro/login', routing_key="enviar")



def callback(ch, method, properties, body):
    global clientes
    global mensajes
    found = False
    if str(method.routing_key) == "login":
        cuenta = json.loads(body)
        if len(clientes['usuario'])>0:
            for i in range(len(clientes['usuario'])):
                if clientes['usuario'][i] == cuenta['usuario'] and clientes['password'][i].strip() == cuenta['password'].strip():
                    found = True
                    ch.basic_publish(exchange='',routing_key=properties.reply_to,body=clientes['id'][i])
        if not found:
            ch.basic_publish(exchange='',routing_key=properties.reply_to,body="Error")
    elif str(method.routing_key) == "registro":
        cuenta = json.loads(body)
        if cuenta['usuario'] != "" and cuenta['password'] != "" and cuenta['id'] != "" and cuenta['id'] not in clientes['id']:
            clientes['id'].append(cuenta['id'])
            clientes['usuario'].append(cuenta['usuario'])
            clientes['password'].append(cuenta['password'])
            filec = open("./logs/cuentas.txt","a")
            filec.write(cuenta['id']+"#"+cuenta['usuario']+"#"+cuenta['password']+"\n")
            filec.close()
            ch.basic_publish(exchange='',routing_key=properties.reply_to,body="Success")
        else:
            ch.basic_publish(exchange='',routing_key=properties.reply_to,body="Error")
    elif str(method.routing_key) == "usuarios":
        user = body.decode("utf-8")
        sendto = {"largo": str(len(clientes['id']))}
        ch.basic_publish(exchange='ec-s',routing_key=user,body=json.dumps(sendto))
        if len(clientes['id']) != 0:
            for i in clientes['id']:
                ch.basic_publish(exchange='ec-s',routing_key=user,body=i)
        else:
            ch.basic_publish(exchange='ec-s',routing_key=user,body="")
    elif str(method.routing_key) == "mensajes":
        user = body.decode("utf-8")
        length = 0
        for i in mensajes['from']:
            if(i.strip() == user.strip()):
                length+=1
        sendto = {"largo": length}
        ch.basic_publish(exchange='ec-s',routing_key=user,body=json.dumps(sendto))

        if length != 0:
            for i in range(len(mensajes['id'])):
                if(mensajes['from'][i].strip() == user.strip()):
                    sendto = {'id': mensajes['id'][i],
                            'from':mensajes['from'][i],
                            'to':mensajes['to'][i],
                            'mensaje':mensajes['mensaje'][i],
                            'fecha':mensajes['fecha'][i]}
                    ch.basic_publish(exchange='ec-s',routing_key=user,body=json.dumps(sendto))
        else:
            ch.basic_publish(exchange='ec-s',routing_key=user,body="")
    elif str(method.routing_key) == "mensajes2":
        user = str(body.decode())
        length = 0
        for i in mensajes['to']:
            if(i.strip() == user.strip()):
                length+=1
        sendto = {"largo": length}
        ch.basic_publish(exchange='ec-s',routing_key=user,body=json.dumps(sendto))

        if length != 0:
            for i in range(len(mensajes['id'])):
                if(mensajes['to'][i].strip() == user.strip()):
                    sendto = {'id': mensajes['id'][i],
                            'from':mensajes['from'][i],
                            'to':mensajes['to'][i],
                            'mensaje':mensajes['mensaje'][i],
                            'fecha':mensajes['fecha'][i]}
                    ch.basic_publish(exchange='ec-s',routing_key=user,body=json.dumps(sendto))
        else:
            ch.basic_publish(exchange='ec-s',routing_key=user,body="")


    elif str(method.routing_key) == "enviar":
        exist = False
        mensajerec = json.loads(body)
        for i in clientes['id']:
            if i == mensajerec['to']:
                exist = True
                break
        if exist:
            if len(mensajes['id']) == 0:
                newid = 0
            else:
                newid = int(mensajes['id'][(len(mensajes['id'])-1)])+1
            mensajes['id'].append(str(newid))
            mensajes['from'].append(mensajerec['from'])
            mensajes['to'].append(mensajerec['to'])
            mensajes['mensaje'].append(mensajerec['mensaje'])
            mensajes['fecha'].append(mensajerec['fecha'])
            file = open("./logs/log.txt","a")
            file.write(str(newid)+"#"+ mensajerec['from']+"#"+mensajerec['to']+"#"+mensajerec['mensaje']+"#"+mensajerec['fecha']+"\n")
            file.close()
            ch.basic_publish(exchange='ec-s',routing_key=mensajerec['from'],body="Success")
        else:
            ch.basic_publish(exchange='ec-s',routing_key=mensajerec['from'],body="Error")





channel.basic_consume(queue='registro/login', on_message_callback=callback,auto_ack=True)

channel.start_consuming()
