from concurrent import futures
import time
import math
import logging
import os
import shutil



import grpc

import chat_pb2
import chat_pb2_grpc

class ChatServicer(chat_pb2_grpc.ChatServicer):
    def __init__(self):
        #shutil.rmtree('/registros')
        if not os.path.exists('logs'):
            os.mkdir('logs')
        if not os.path.exists('logs/log.txt'):
            f = open('logs/log.txt',"w+")
            f.close()
        if not os.path.exists('logs/cuentas.txt'):
            f = open('logs/cuentas.txt',"w+")
            f.close()
        self.clientes = []
        self.lastid = 0
        self.mensajes = []
        self.lastmid = 0
        file = open("./logs/log.txt","r+")
        filec = open("./logs/cuentas.txt","r+")
        clientesraw = filec.readlines()
        for i in clientesraw:
            value = i.split("#")
            self.clientes.append(chat_pb2.LCliente(id = int(value[0]),usuario=value[1],pas=value[2].strip()))
        if len(clientesraw)>0: 
            self.lastid = int(clientesraw[len(clientesraw)-1].split("#")[0])
        else:
            self.lastid=0
        msjs = file.readlines()
        for i in msjs:
            value2 = i.split("#")
            self.mensajes.append(chat_pb2.Mensajes(id=int(value2[0]),de=value2[1],to=value2[2],mensaje=value2[3],fecha=value2[4]))
        if len(msjs)>0:
            self.lastmid = int(msjs[len(self.mensajes)-1].split("#")[0])
        else:
            self.lastmid=0
        file.close()
        filec.close()
    
    def ListadoClientes(self, request, context):
        for cliente in self.clientes:
            print(cliente)
            yield chat_pb2.Cliente(id=cliente.id,Nombre=cliente.usuario)
    def ListadoMensajes(self, request, context):
        for mensaje in self.mensajes:
            print(mensaje)
            if(int(mensaje.de) == request.id):
                yield chat_pb2.LMensajes(de = mensaje.de,fecha = mensaje.fecha,mensaje= mensaje.mensaje)
    def ListadoMensajes2(self, request, context):
        for mensaje in self.mensajes:
            if(int(mensaje.to) == request.id):
                yield chat_pb2.LMensajes(de = mensaje.de,fecha = mensaje.fecha,mensaje= mensaje.mensaje)
    def Login(self,request,context):
        for i in self.clientes:
            print(i)
            if request.usuario == i.usuario and request.pas == i.pas:
                return  chat_pb2.Info(Msg =str(i.id)+"#Success")
        return chat_pb2.Info(Msg =str(0)+"#Fail")
    def Registro(self,request,context):
        if request.usuario != "" and request.pas != "":
            file = open("./logs/cuentas.txt","a+")
            self.lastid+=1
            file.write(str(self.lastid)+"#"+request.usuario+"#"+request.pas+"\n")
            self.clientes.append(chat_pb2.LCliente(id = self.lastid,usuario=request.usuario,pas=request.pas))
            file.close()
            return chat_pb2.Info(Msg="Success")
        else:
            return chat_pb2.Info(Msg="Fail")
    def Send(self,request,context):
        encontrado = False
        for i in self.clientes:
            if i.id == int(request.de):
                encontrado = True
                break
        if encontrado:
            request.id = self.lastmid+1
            self.lastmid+=1
            self.mensajes.append(request)
            file=open("./logs/log.txt","a")
            file.write(str(request.id)+"#"+request.de+"#"+request.to+"#"+request.mensaje+"#"+request.fecha+"\n")
            file.flush()
            file.close()
            return chat_pb2.Info(Msg="Success")
        else:
            return chat_pb2.Info(Msg="")
    def GetCliente(self,request,context):
        for i in self.clientes:
            if i.id == int(request.id):
                return chat_pb2.Cliente(id=i.id,Nombre = i.usuario)
        
             


def serve():
    file = open("server.txt","r")
    clients = file.readlines()
    file.close()
    n = clients[0]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=int(n.strip())))
    chat_pb2_grpc.add_ChatServicer_to_server(
    ChatServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
        serve()


