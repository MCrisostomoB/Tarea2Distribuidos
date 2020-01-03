# Tarea2Distribuidos
## Instrucciones:
* Para poder ejectuar tanto la parte 1 como la parte 2 de la Tarea es necesario ingresar a la carpeta parte 1 o parte 2 y dentro de ellas ejecutar docker-compose build y luego docker-compose up

* Tanto para la parte 1 como 2 de la tarea se tiene un txt llamado "cliente.txt" en la carpeta de cliente, en la cual estan todos los mensajes que se enviaran desde el cliente al servidor. Este txt siempre debe terminar con el numero "5"  que es el de salir,y debe iniciar con el usuario y contraseña para la parte 1 y para la parte 2 se incluye la id, a continuacion se dara un ejemplo:
	* user=xxx
	* pass=xxx
	* 2
	* 1
	* 1
	* 4#1#Hola este es un mensaje de prueba#2
	* 2
	* 5
	
* El primer 2 despues del usuario y contraseña, corresponde a registrarse, y el 1 que viene corresponde a logearse.
* Pasada esta etapa, son solamente comandos a realizar como por ejemplo :
	* 1-ver usuarios
	* 2- ver mensajes enviados
	* 3- ver mensajes recibidos
	* 4- enviar un mensaje
	* 5- Salir
*Un ejemplo de la parte 2 seria el siguiente:
	* id=xxx
	* user=xxx
	* pass=xxx
	* 2
	* 1
	* 4#xxx#Hola este es un mensaje de prueba
	* 2
	* 2
	* 3
	* 3
	* 5
*Para la parte 2  cuando se seleccione la opcion 4, debe ser de la siguiente manera 4#id a quien se mandara#mensaje
*Para la parte 1 cuando se selecciona la opcion 4, debe ser de la siguiente manera 4#id a quein se le mandara#mensaje#2
* Todas las instrucciones anteriores son para modificar el archivo cliente.txt que se encuentran en las carpetas cliente 1 y 2 para la parte 2, para poder customizar el mandado de mensajes automaticos.
* Dentro del container los logs creados por el servidor. llamados log.txt,clientes.txt seran guardados en /app/logs pero a su vez se pueden ver estos archivos localmente em la misma carpeta en la que se ejecuta el programa, es decir estos archivos se encontraran en CarpetaActualDondeSeEjecuta/parte1/resultados o CarpetaActualDondeSeEjecuta/parte2/resultados.
* Nota: Para la parte 2, el docker se demora un poco mas en reaccionar, por como funciona rabbitmq hay veces que se demora en partir y por eso se hacen varios retry de los clientes y servidores, soltando asi mucha informacion de una, se recomienda si es que no funciona a la primera correr el docker-compose up nuevamente.
## Integrantes
* Rigoberto Bravo 201673551-8
* Martín Crisóstomo 201673609-3
