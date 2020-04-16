from PIL import Image
import io
from array import array
import time

binarios = []
mensaje = []
mensaje_a_enviar=[]
mal_transmitidos = [] #almacena el indice en el arreglo mensaje_a_enviar de aquellos bytes que hayan sido mal transmitidos
mensaje_recuperado = []
discrepancia = 0
corte = 9

img  = Image.open("./Lib.jpg")
with open("./Lib.jpg", "rb") as imagen:
  datos = imagen.read()
  arreglo_bytes = bytearray(datos)

for i in arreglo_bytes:
    binarios.append(bin(i)[2:])

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

print(mensaje_a_enviar[35])

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
#time.sleep(2)
print(mensaje_a_enviar[35])
print("Comprobando bits de parada")
indice = 0
print("corte: ",corte)
for i in mensaje_a_enviar:
    iT = i.count("1") + i.count("0")
    if iT == l_esperado and i[corte:] == terminacion:
        mensaje_a_enviar[indice] = i[0:corte]
    else:
        mal_transmitidos.append(indice)
    indice += 1
#time.sleep(2)
print(mensaje_a_enviar[35])
print("Buscando errores con paridad ",paridadT)
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
print(mensaje_a_enviar[35])
#time.sleep(3)         
if len(mal_transmitidos) != 0:
    print("Es necesario retransmitir los bytes: ")
    #print(mal_transmitidos)
else: 
    indice = 0
    for i in mensaje_a_enviar:
        if mensaje_a_enviar[indice] != binarios[indice]:
            discrepancia += 1
            break
        #indice += 1
    if discrepancia == 0:
        print("Mostrando imagen")
        img.show()
        print("Transmision terminada")
    else:
        print("La imagen no fue bien recibida")

