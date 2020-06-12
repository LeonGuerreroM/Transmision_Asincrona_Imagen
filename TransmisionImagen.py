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
me_temp = []
bp_temp = []
numero_bits_diferentes = []
discrepancia = 0
corte = 9
indiceTrama = 0
indiceBinarios = 0
cont = 0

img  = Image.open("./Lib.jpg")
with open("./Lib.jpg", "rb") as imagen:
    datos = imagen.read()
    
BER = 0.001
P1 = (1-BER)**8
P2 = 1-P1


print("Las probabilidades de error calculadas numericamente son:\nPb=0.001\nProbabilidad errores en la trama={}".format(P2))
    
  
for i in datos:
    binarios.append(bin(i)[2:])
    
for i in datos:
    binPuros.append(bin(i)[2:])
    binPuros[cont] = binPuros[cont].zfill(8)
    cont += 1


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

#print(binarios[100])

print("_______________EMISOR________________")
print("Elija el numero de bits de parada (1 o 2)")
print("--------------------------------------")
bits_parada = input()
bits_parada = int(bits_parada)
if bits_parada == 1:
    terminacion = "1"
    l_esperado = 10
else:
    terminacion = "11"
    l_esperado = 11
print("--------------------------------------")
print("Escoja el tipo de paridad\n0. Sin paridad\n1. Paridad impar\n2.Paridad par")
print("--------------------------------------")
paridad = input()
paridad = int(paridad)
if paridad == 0:
    l_esperado -= 1
    corte -= 1
print("_____________________________________")

if paridad == 0:
    for i in binarios:
        mensaje_a_enviar.append(i.zfill(9)+terminacion)

if paridad == 1:
    for i in binarios:
        mensaje.append(i.zfill(9))
    for i in mensaje:
        mensajeC = str(i)
        num_unos = mensajeC.count("1")
        if num_unos%2 == 0:
            mensajeC=mensajeC+"1"+terminacion
            mensaje_a_enviar.append(mensajeC)
        if num_unos%2 != 0: 
            mensajeC=mensajeC+"0"+terminacion
            mensaje_a_enviar.append(mensajeC)

if paridad == 2:
    for i in binarios:
        mensaje.append(i.zfill(9))
    for i in mensaje:
        mensajeC = str(i)
        num_unos = mensajeC.count("1")
        if num_unos%2 == 0:
            mensajeC=mensajeC+"0"+terminacion
            mensaje_a_enviar.append(mensajeC)
        if num_unos%2 != 0: 
            mensajeC=mensajeC+"1"+terminacion
            mensaje_a_enviar.append(mensajeC)    

print("_______________RECEPTOR________________")
if paridad == 1:
    paridadT = "impar"
elif paridad == 2:
    paridadT = "par"
elif paridad == 0:
    paridadT = "nula"
print("Se ha escogido paridad {} con {} bit(s) de parada".format(paridadT, bits_parada))
print("Comprobando bits de inicio")
indice = 0
for i in mensaje_a_enviar:
    mensaje_a_enviar[indice] = i[1:]
    indice = indice + 1
time.sleep(2)
print("Comprobando bits de parada")
indice = 0
for i in mensaje_a_enviar:
    iT = i.count("1") + i.count("0")
    if iT == l_esperado and i[corte:] == terminacion:
        mensaje_a_enviar[indice] = i[0:corte]
    else:
        mal_transmitidos.append(indice)
    indice += 1
time.sleep(2)
print("Buscando errores con paridad",paridadT)
indice = 0
if paridad == 1:
    for i in mensaje_a_enviar:
        if i.count("1")%2 == 0:
            mal_transmitidos.append(indice)
        if i.count("1")%2 != 0:
            mensaje_a_enviar[indice] = i[:-1]
        indice += 1
if paridad == 2:
    for i in mensaje_a_enviar:
        if i.count("1")%2 != 0:
            mal_transmitidos.append(indice)
        if i.count("1")%2 == 0:
            mensaje_a_enviar[indice] = i[:-1]
        indice += 1
time.sleep(2)         
if len(mal_transmitidos) != 0:
    print("Es necesario retransmitir los bytes: ")
    print(mal_transmitidos)
else: 
    indice = 0
    for i in mensaje_a_enviar:
        if int(mensaje_a_enviar[indice], base=2) != int(binPuros[indice], base=2):
            mal_transmitidos.append(mensaje_a_enviar[indice])
            me_temp = list(mensaje_a_enviar[indice])
            bp_temp = list(binPuros[indice])
            diferencias = 0
            for i, j in zip(me_temp, bp_temp):
                if j != i:
                    diferencias += 1
            numero_bits_diferentes.append(diferencias)
            me_temp = []
            bp_temp = []
            print("Trama diferente")
            print("mensaje a enviar tiene {}".format(mensaje_a_enviar[indice]))
            print("bin puros tiene {}".format(binPuros[indice]))
            discrepancia += 1
        indice += 1
    if discrepancia == 0:
        print("Mostrando imagen")
        img.show()
        print("Transmision terminada")
    else:
        print("La imagen no fue bien recibida. Se muestran a continuacion las tramas con bits erroneos")
        print(mal_transmitidos)
        print("Y el numero de bits diferentes, respectivamente")
        print(numero_bits_diferentes)
        print("La probabilidad calculada es igual a {}".format(len(mal_transmitidos)/len(mensaje_a_enviar)))