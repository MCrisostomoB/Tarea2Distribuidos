#!/usr/bin/env python
import pika
import sys
import json
import datetime

def callback(ch, method, properties, body):
    global response
    global result
    global logged
    global ownid
    global iteraciones
    global iter
    global resulog
    if method.routing_key == ownid:
        try:
            respuesta = json.loads(body)
            if 'largo' in respuesta:
                iteraciones = int(respuesta['largo'])
                response = "found"
            else:
                iter += 1
                print("[" + respuesta['fecha']+ "]"+ " ID mensaje: " + respuesta['id'] + " De: " + respuesta['from']+ " Para: " + respuesta['to']+"\n Mensaje: "+ respuesta['mensaje'])
        except:
            decoded = body.decode("utf-8")
            if decoded == "Success":
                print("Se envio el mensaje")
                response = "found"
            elif decoded == "Error":
                print("Hubo un error al intentar enviar el mensaje")
                response = "found"
            else:
                iter += 1
                if iteraciones!= 0:
                    print(decoded)
    else:
        decoded = body.decode("utf-8")
        if int(result) == 1:
            print(decoded)
            if decoded == "Error":
                response = "Error"
            else:
                print("Aqui")
                logged = True
                response = str(body.decode('utf-8'))
        elif int(result) == 2:
            if decoded == "Error":
                response = "Falto rellenar algun campo o la ID ya existe"
            else:
                response = "La cuenta fue creada con exito"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='ec-s', exchange_type='direct')

chl=channel.queue_declare(queue='', exclusive=True)
name = chl.method.queue
channel.basic_consume(queue=name, on_message_callback=callback,auto_ack=True)

logged = False
response= None
ownid=""
iteraciones = 0
iter = 0
while True:
    print("Que desea hacer ?\n")
    print("1- Logearse\n2- Crearse una cuenta\n3- Salir")
    result = input("Ingrese numero de la opcion:")
    if int(result) == 1:
        while True:
            usuario = input("Ingrese Usuario:")
            contrasena = input("Ingrese password:")
            jsonform= { "usuario": usuario,
                        "password": contrasena}
            channel.basic_publish(exchange='ec-s', routing_key="login",properties=pika.BasicProperties(reply_to=name), body=json.dumps(jsonform))
            print(response)
            while response is None:
                connection.process_data_events() 
            if response == "Error":
                respuesta = input("El usuario o contraseña estan malos, si quiere intentar logearse denuevo presione 1, si no presione 2: ")
                if int(respuesta) == 2:
                    break
                else:
                    response = None
            else:
                break       
    elif int(result) == 2:
        ide = input("Ingrese un nombre distinctivo con el que los otros usuarios lo veran: ")
        usuario = input("Ingrese Usuario:")
        contrasena = input("Ingrese password:")
        jsonform= {"id": ide,
                    "usuario": usuario,
                    "password": contrasena}

        channel.basic_publish(exchange='ec-s', routing_key="registro",properties=pika.BasicProperties(reply_to=name), body=json.dumps(jsonform))
        while response is None:
            connection.process_data_events()
        print(response)
        response = None
    elif int(result) == 3:
        exit(1)
    print(logged)
    if logged:
        ownid=response
        response = None
        channel.queue_bind(exchange='ec-s', queue=name, routing_key=ownid)
        print("Se logeo satsifactoriamente!\n")
        while True:
            resulog = input("Que desea hacer ? \n 1- Ver Listado de Usuarios\n 2- Ver Mensajes Enviados\n 3- Ver Mensajes Recibidos\n 4- Enviar un mensaje a un usuario\n 5- Salir\n" )
            if int(resulog) == 1:
                iter = 0
                iteraciones = 0
                channel.basic_publish(exchange='ec-s', routing_key="usuarios",body =ownid)
                while response is None:
                    connection.process_data_events()
                while iter < iteraciones:
                    connection.process_data_events()
                response = None
            elif int(resulog)==2:
                iter = 0
                iteraciones = 0
                channel.basic_publish(exchange='ec-s', routing_key="mensajes",body =ownid)
                while response is None:
                    connection.process_data_events()
                while iter < iteraciones:
                    connection.process_data_events()
                response = None
            elif int(resulog)==3:
                iter = 0
                iteraciones = 0
                channel.basic_publish(exchange='ec-s', routing_key="mensajes2",body =ownid)
                while response is None:
                    connection.process_data_events()
                while iter < iteraciones:
                    connection.process_data_events()
                response = None
            elif int(resulog) == 4:
                to = input("Ingrese el nombre a la persona que le quiere enviar el mensaje (El que aparece en la lista de Usuarios):")
                msg = input("Ingrese el mensaje que le desea enviar a este usuario: ")
                sendto = {'from':ownid,
                      'to':to,
                      'mensaje':msg,
                      'fecha':str(datetime.datetime.now())}
                channel.basic_publish(exchange='ec-s', routing_key="enviar",body =json.dumps(sendto))
                while response is None:
                    connection.process_data_events()
            elif int(resulog) == 5:
                exit(1)
