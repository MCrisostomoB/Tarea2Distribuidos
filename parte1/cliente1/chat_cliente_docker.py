from __future__ import print_function

import random
import logging

import grpc
import datetime

import chat_pb2
import chat_pb2_grpc


def inicio():
    channel = grpc.insecure_channel('servidor:50051')
    file = open("cliente.txt","r")
    comandos = file.readlines()
    file.close()
    usertouse = comandos[0].split("=")[1].strip()
    passtouse=comandos[1].split("=")[1].strip()
    stub = chat_pb2_grpc.ChatStub(channel)
    for comm in range(2,len(comandos)):
        print("Que desea hacer ?\n")
        print("1- Logearse\n2- Crearse una cuenta\n3- Salir")
        print("Ingrese numero de la opcion:")   
        result = comandos[comm]
        print(result)
        logeado = False
        if int(result) == 1:
            while True:
                print("Ingrese Usuario:")
                usuario = usertouse
                print(usuario)
                print("Ingrese password:")
                contrasena = passtouse
                print(contrasena)
                log = stub.Login(chat_pb2.RCliente(usuario=usuario,pas=contrasena))
                logsplit=log.Msg.split("#")
                if(logsplit[1] == "Success"):
                    logeado = True
                    personalid = logsplit[0]
                    break
                else:
                    print("El usuario o contraseña son incorrectos")
                    op = input("Si desea volver a intentar logearse ingrese 1 , si quiere volver al menu principal ingrese 2: ")
                    if int(op) == 2:
                        break
        elif int(result) == 2:
            print("Ingrese Usuario:")
            usuario = usertouse
            print(usuario)
            print("Ingrese password:")
            contrasena = passtouse
            print(contrasena)
            reg = stub.Registro(chat_pb2.RCliente(usuario=usuario,pas=contrasena))
            if(reg.Msg == "Success"):
                print("Se creo el usuario satisfactoriamente")
            else:
                print("Falto llenar alguno de los campos")
        elif int(result) == 3:
            exit(1)
        if logeado:
            print("Se logeo satsifactoriamente!\n")
            for comm2 in range(comm,len(comandos)):
                print("Que desea hacer ? \n 1- Ver Listado de Usuarios\n 2- Ver Mensajes Enviados\n 3- Ver Mensajes Recibidos\n 4- Enviar un m ensaje a un usuario\n 5- Salir\n" )
                spliting = comandos[comm2].split("#")
                resulog = spliting[0].strip()
                print(resulog)
                if int(resulog) == 1:
                    listado = stub.ListadoClientes(chat_pb2.Cliente(id = int(personalid),Nombre=usuario))
                    print("Los usuarios son:")
                    for user in listado:
                        print(str(user.id) +"-"+ user.Nombre)
                elif int(resulog) == 2:
                    mensajes = stub.ListadoMensajes(chat_pb2.Cliente(id = int(personalid),Nombre= usuario))
                    for i in mensajes:
                        print("["+i.fecha+"]")
                        print("Mensaje: "+ i.mensaje)
                elif int(resulog) == 3:
                    mensajes = stub.ListadoMensajes2(chat_pb2.Cliente(id = int(personalid),Nombre= usuario))
                    for i in mensajes:
                        print("["+i.fecha+"] De la id: "+ str(i.de))
                        print("Mensaje: "+ i.mensaje)
                elif int(resulog) ==4:
                    while True:

                        print("Ingrese la id de la persona a la cual se le quiere enviar (el numero que aparece en el listado de usuarios) ")
                        sendto = spliting[1].strip()
                        print(sendto)
                        print("Ingrese el mensaje que le quiere enviar al usuario: ")
                        msgsend= spliting[2]
                        print(msgsend)
                        resultadoenv = stub.Send(chat_pb2.Mensajes(id=0,de= personalid,to=sendto,mensaje= msgsend,fecha= str(datetime.datetime.now())))
                        if resultadoenv.Msg == "Success":
                            print("Su mensaje ha sido enviado exitosamente")
                        else:
                            print("Ocurrio un problema, el usuario al cual le desea enviar el mensaje no existe")
                        print("Si desea enviar otro mensaje ingrese 1, de otra manera ingrese 2: ")
                        salir = spliting[3].strip()
                        print(salir)
                        if int(salir) == 2:
                            break
                elif int(resulog) == 5:
                    exit(1)

            
            

if __name__ == '__main__':
    inicio()
