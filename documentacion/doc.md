# Introducción

El siguiente proyecto ha sido creado con el propósito de satisfacer
una necesidad que tienen los estudiantes del Instituto Tecnológico
de Costa Rica, el manejo de tiempo. La idea surge debido a la necesidad
de una herramienta sencilla de utilizar para llevar un control estandarizado
del tiempo dividido entre actividades académicas y extracurriculares,
no solo esto, sino que también ofrezca una manera sencilla de visualizar
y de mantener la concentración durante las actividades diarias.


# Análisis del problema

Se requiere un sistema que sea capaz de tomar fotografías y analizar el estado
de animo de una persona durante la extensión de distintas actividades, además
de esto se requiere qu este sistema almacene los diferentes estados de animo que
la persona para así llevar control de estos, además de detectar cuando se pierde
la concentración durante una actividad y notificar al usuario cuando este se desconcentre.


## Interfáz del programa

Este programa no requiere una interfáz sofisticada, sin embargo, la interfaz que
se cree para el debe mediar acciones del usuario hacia el backend del programa para
realizar acciones como activar y desactivar la captura de estado de animo, así como el
detector de concentración.


## Captura de imágenes

El programa deberá tener un sistema interno que permita capturar imágenes a través de
la cámara de la computadora, y estas deben ser almacenadas de alguna manera que sea eficiente
y no cree muchos archivos inútiles en el sistema del usuario.


## Almacenamiento de actividades

No es necesario poder crear actividades nuevas, sin embargo, se necesita poder almacenar
los datos de las emociones obtenidas en la duración de cada actividad.


## Almacenamiento de emociones

Se debe definir una manera efectiva de almacenar distintas instancias de las emociones
para poder acceder a estas luego y poder acceder a ellas durante cualquier momento a lo
largo del uso del programa.


# Solución del problema


## Captura de imágenes

Para esta se utilizó se capturan imágenes mediante la cámara en intérvalos y estas son
almacenadas de manera persistente en el disco, sin embargo, cada imágen sobreescribe la
anterior para no crear archivos basura en la computadora del usuario, puesto a que las
imágenes tienden a tener un tamaño considerable.


## Actividades

### Almacenamiento

Para almacenar las actividades se utilizó un archivo binario en el cual, mediante el uso
de la librería pickle se almacena una lista con las actividades, de esta manera es muy
sencillo obtener estas instancias almacenadas de manera persistente.


### Cola de actividades

Para cambiar de actividad y utilizar las actividades obtenidas se creó una cola de actividades
mediante la cuál se puede revisar el contenido de la actividad que sigue, eliminar actividades
y agregar actividades a la cola, esta estructura de datos permite el manejo y el cambio sencillo
de la actividad actual y futuras actividades.

# Emociones

## Almacenamiento

Las emociones son guardadas en un árbol binario cuya raíz vive en cada actividad existente,
el criterio para su ordenamiento se basa en la hora en la que se registró la actividad, esta
hora se almacena en formato de `UNIX Timestamp`, y es la entidad que decide la posición dentro
del árbol binario.


## Relaciónes con actividades

Para la relación con las actividades, se utiliza la actividad actual del programa para trabajar
sobre ella, en esta se almacenan todas las emociones que se capten durante su duración.


# Análisis de resultados

|Tarea/Requerimiento|Estado|Observaciones|
|:-:|:-:|:--|
|Reconocimiento de emociones|Completo|El sistema reconoce las emociones del usuario y las almacena|
|Control de concentración|Completo|El sistema reproduce una alarma cuando el usuario pierde la concentración|
|Reporte|Incompleto|Se completó el reporte de emociones predominantes en la mañana y en la tarde, pero no el semanal|
|Almacenamiento y recuperación de archivos|Completo|Los datos necesarios son almacenados y recuperados a necesidad|
