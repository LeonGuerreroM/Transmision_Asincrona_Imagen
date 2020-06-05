from PIL import Image
import io
import time
import random

binarios = []
binPuros = []
mensaje = []
mensaje_a_enviar=[]
mal_transmitidos = [] #almacena el indice en el arreglo mensaje_a_enviar de aquellos bytes que hayan sido mal transmitidos
mensaje_recuperado = []
discrepancia = 0
corte = 9
indiceTrama = 0
indiceBinarios = 0
cont = 0

img  = Image.open("./Lib.jpg")
with open("./Lib.jpg", "rb") as imagen:
    datos = imagen.read()
  
for i in datos:
    binarios.append(bin(i)[2:])
    
print(binarios[100])
print("__________________________________________________________________")

for i in datos:
    binPuros.append(bin(i)[2:])

for i in binarios:
    inicial = i.zfill(8)
    indiceTrama = 0
    for j in inicial:
        isWrong = random.randint(1,1000) #simula una probabilidad de error
        if isWrong == 4: #si se cumplió
            if j == '1': #intercambia el valor de ese bit en el indice correspondiente en inicial
                lista = list(inicial)
                lista[indiceTrama] = '0'
                inicial = "".join(lista)
            elif j == '0':
                lista = list(inicial)
                lista[indiceTrama] = '1'
                inicial = "".join(lista)
        indiceTrama += 1
    binarios[indiceBinarios] = inicial
    cont += 1    
    indiceBinarios += 1

print(binarios[100])