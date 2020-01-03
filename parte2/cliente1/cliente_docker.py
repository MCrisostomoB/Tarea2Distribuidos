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
            if decoded == "Error":
                response = "Error"
            else:
                logged = True
                response = str(body.decode('utf-8'))
        elif int(result) == 2:
            if decoded == "Error":
                response = "Falto rellenar algun campo o la ID ya existe"
            else:
                response = "La cuenta fue creada con exito"

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
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
file = open("cliente.txt","r")
comandos = file.readlines()
file.close()
idtouse= comandos[0].split("=")[1].strip()
usertouse = comandos[1].split("=")[1].strip()
passtouse=comandos[2].split("=")[1].strip()
for comm in range(3,len(comandos)):
    print("Que desea hacer ?\n")
    print("1- Logearse\n2- Crearse una cuenta\n3- Salir")
    print("Ingrese numero de la opcion:")   
    result = comandos[comm]
    print(result)
    if int(result) == 1:
        while True:
            print("Ingrese Usuario:")
            usuario = usertouse
            print(usuario)
            print("Ingrese password:")
            contrasena = passtouse
            print(contrasena)
            jsonform= { "usuario": usuario,
                        "password": contrasena}
            channel.basic_publish(exchange='ec-s', routing_key="login",properties=pika.BasicProperties(reply_to=name), body=json.dumps(jsonform))
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
        print("Ingrese un nombre distinctivo con el que los otros usuarios lo veran: ")
        ide = idtouse 
        print(ide)
        print("Ingrese Usuario:")
        usuario = usertouse
        print(usuario)
        print("Ingrese password:")
        contrasena = passtouse
        print(contrasena)
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
    if logged:
        ownid=response
        response = None
        channel.queue_bind(exchange='ec-s', queue=name, routing_key=ownid)
        print("Se logeo satsifactoriamente!\n")
        for comm2 in range(comm,len(comandos)):
            print("Que desea hacer ? \n 1- Ver Listado de Usuarios\n 2- Ver Mensajes Enviados\n 3- Ver Mensajes Recibidos\n 4- Enviar un mensaje a un usuario\n 5- Salir\n" )
            spliting = comandos[comm2].split("#")
            resulog =spliting[0].strip()
            print(resulog)
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
                print(ownid)
                channel.basic_publish(exchange='ec-s', routing_key="mensajes2",body =ownid)
                while response is None:
                    connection.process_data_events()
                while iter < iteraciones:
                    connection.process_data_events()
                response = None
            elif int(resulog) == 4:
                print("Ingrese el nombre a la persona que le quiere enviar el mensaje (El que aparece en la lista de Usuarios):")
                to = spliting[1].strip()
                print(to)
                print("Ingrese el mensaje que le desea enviar a este usuario: ")
                msg = spliting[2].strip()
                print(msg)
                sendto = {'from':ownid,
                      'to':to,
                      'mensaje':msg,
                      'fecha':str(datetime.datetime.now())}
                channel.basic_publish(exchange='ec-s', routing_key="enviar",body =json.dumps(sendto))
                while response is None:
                    connection.process_data_events()
            elif int(resulog) == 5:
                exit(1)
