# -*- coding: utf-8 -*-
"""
Created on Mon May 22 10:21:55 2023

@author: JUAN
"""
import numpy as np
import random 
import copy
import time
start_time = time.time()

   

#definir las distancias
distancias = np.loadtxt('C:\\Users\\juand\OneDrive\\Documents\\Andes\\10. Semestre\\Tesis\\Código\\PRUEBA\\Distancias1.txt',
                   delimiter =",", skiprows=0)
#definir las demandas
demandas = np.loadtxt('C:\\Users\\juand\OneDrive\\Documents\\Andes\\10. Semestre\\Tesis\\Código\\PRUEBA\\Demandas1.txt',
                   delimiter =",", skiprows=0)

#Definir cosas varias.
#Definir capacidad"
with open('C:\\Users\\juand\\OneDrive\\Documents\\Andes\\10. Semestre\\Tesis\\Código\\PRUEBA\\I1.txt', 'r') as archivo:
    for linea in archivo:
        if 'CAPACITY: ' in linea:
            capacidad = int(linea.split()[-1])
            capacidadInicial =int(linea.split()[-1])
            break


#Definir EnergiaInicial"

with open('C:\\Users\\juand\\OneDrive\\Documents\\Andes\\10. Semestre\\Tesis\\Código\\PRUEBA\\I1.txt', 'r') as archivo:
    for linea in archivo:
        if 'ENERGY_CAPACITY: ' in linea:
            energiaInicial = int(linea.split()[-1])
            energiaActual =int(linea.split()[-1])
            break

#Definir Consumo
with open('C:\\Users\\juand\\OneDrive\\Documents\\Andes\\10. Semestre\\Tesis\\Código\\PRUEBA\\I1.txt', 'r') as archivo:
    for linea in archivo:
        if 'ENERGY_CONSUMPTION: ' in linea:
            consumo = float(linea.split()[-1])
            break



Soluciones ={}
numClientes = 0
nodosVisitados =[]
#Encontrar Numero de nodos en total
for demanda in demandas:
    if demanda >0:
        numClientes = numClientes+1
#encontrar cuantos nodos son estación de recarga
numRecarga =-1
for valor in demandas:
    if valor == 0:
        numRecarga = numRecarga +1

numRecarga
# encontrar en qué valor está la primera estación de recarga

for i in range(len(demandas)):
    if demandas[i] == 0 and i >1:
        PrimeraEstaciónDeRecarga =i-1
        break

#numEstacionesDeRecarga
numEstacionesRecarga = len(demandas)-PrimeraEstaciónDeRecarga

# Crear función que encuentra distancia euclidiana. 

def distancia_euclidiana(i,j):
    x1 = distancias[i,0]  
    x2 = distancias[j,0]
    y1 = distancias[i,1]
    y2 = distancias[j,1]
    xd = (x2 -x1)**2
    yd = (y2-y1)**2
    resp = np.sqrt(xd+yd)
    return resp

#Crear matriz de distancias

matDistancias = np.zeros((len(demandas), len(demandas)))

valorDistancias = 0
for i in range(len(demandas)):
    for j in range(len(demandas)):
        valorDistancias = distancia_euclidiana(i,j)
        matDistancias[i,j] = valorDistancias
   
def recargarVehiculo(NodoInicial):
    NodoIrRecarga = 0
    DistanciaRecargas=[]
    for i in range(numEstacionesRecarga):
        DistanciaRecargas.append(distancia_euclidiana(NodoInicial,PrimeraEstaciónDeRecarga+ i))
    
    minimo =1000 
    for i in range(numEstacionesRecarga):
        if minimo > DistanciaRecargas[i]:
            NodoIrRecarga = PrimeraEstaciónDeRecarga+ i
            minimo = DistanciaRecargas[i]
    return NodoIrRecarga
    

#matriz más cerca de recarga:

matRecargas = np.zeros((len(demandas), len(demandas)))

listaRecargas = [0]*len(demandas)

valorRecargas = 0

for i in range(len(demandas)):
    valorRecargas = recargarVehiculo(i)
    listaRecargas[i] = valorRecargas
    
    
#Iniciar Estructura
Respuestas =[]

for a in range(10):
    

    Fo =0
    
    Ruta = []
    
    capacidades=[]
    
    Ruta.append(0)
    
    nodoInicial = 0
    
    nodoFinal = random.randint(1,PrimeraEstaciónDeRecarga)
    
    Ruta.append(nodoFinal)

    energiaActual = energiaActual - matDistancias[nodoInicial,nodoFinal] *consumo
    
    capacidad = capacidad - demandas[nodoFinal]
    
    capacidades.append(capacidad)
    
    nodosVisitados.append(nodoInicial)
    
    nodosVisitados.append(nodoFinal)

    #print(Ruta)

    #print(capacidades)

    #print(energiaActual)


    #llenar el resto de cosas

    cambioNodos = True

    Factible = True

    contadorPasos = 0



    while len(nodosVisitados) < numClientes:
    
        contadorPasos = contadorPasos +1
    
        #print("factible? " + str(Factible))
    
        #print(contadorPasos)
    
        
        Factible = True
        
        #print("el cambio de nodos es "  + str(cambioNodos))
        
        if cambioNodos == True:
            
            nodoInicial = nodoFinal
    
        nodoFinal = random.randint(1,PrimeraEstaciónDeRecarga)
    
        #print(str(nodoInicial)+"  "+ str(nodoFinal) )
    
    
        #Revisar que puerda ir a cargar el vehículo
        
        Posible = False
    
        GastoPotencial =[]
    
        potencialEnergia =energiaActual - matDistancias[nodoInicial,nodoFinal] * consumo
    
        numEstacionesRecarga =len(demandas)-PrimeraEstaciónDeRecarga

        for i in range(numEstacionesRecarga):
        
            GastoPotencial.append(matDistancias[nodoFinal,PrimeraEstaciónDeRecarga+ i]* consumo)
    
        cont =0 
        
        GastoPotencial.append(matDistancias[nodoFinal,0]* consumo)
    
        for i in range(numEstacionesRecarga+1):
       
            if potencialEnergia > GastoPotencial[i]:
        
                Posible = True
            
        if Posible == False:
            
            Factible = False
    
        
    
    
    
    
    
        #Revisar que la energía aguante.
        if energiaActual - matDistancias[nodoInicial,nodoFinal]*consumo <0:
        
            Factible = False
    
        #revisar que la capacidad aguante:
        if capacidad - demandas[nodoFinal] <0:
        
            Factible = False
        
        #revisar que tenga capacidad:
        if capacidad < capacidadInicial*0.25:
        
            nodoFinal = 0
        
            energiaActual = energiaInicial
        
            capacidad = capacidadInicial
        
            capacidades.append(capacidad)
        
            Ruta.append(nodoFinal)
        
            continue
        
    
        # revisar si deben ir a recargar    
        if energiaActual < energiaInicial *0.25:
        
            nodoFinal = listaRecargas[nodoInicial]
        
            energiaActual = energiaActual - matDistancias[nodoInicial,nodoFinal]* consumo
        
            Ruta.append(nodoFinal)
        
            capacidades.append(capacidad)
        
            energiaActual = energiaInicial
        
            continue
    
    
        #revisar que no haya pasado por este nodo
        if nodoFinal in Ruta:
        
            Factible = False
    
        if nodoFinal in nodosVisitados:
        
            Factible = False
    
    
        #Meter nodo en la ruta:
    
        if Factible == True:
        
            energiaActual = energiaActual - matDistancias[nodoInicial,nodoFinal] *consumo
        
            capacidad = capacidad - demandas[nodoFinal]
        
            Ruta.append(nodoFinal)
        
            nodosVisitados.append(nodoFinal)
        
            #print("la ruta hasta el momento es: "+str(Ruta))
        
            cambioNodos = True
        
    
    
    
    

        
        
        
        # si no encuentra a donde ir, ir al nodo central.
        if contadorPasos > 100:
        
            nodoFinal = 0
        
            energiaActual = energiaInicial
        
            capacidad = capacidadInicial
        
            capacidades.append(capacidad)
        
            Ruta.append(nodoFinal)
        
            contadorPasos = 0
        
            cambioNodos = True
        
        
            continue
        
        if Factible == False:
        
            cambioNodos = False
    
    
    Ruta.append(0)
    #Función Objetivo
    fo=0
    for i in range(len(Ruta)-1):
        
        fo = round(fo+matDistancias[Ruta[i],Ruta[i+1]],2)
    
    FuncionObjetivo = fo
    Soluciones = {}
    Soluciones['ruta'] = Ruta
    Soluciones['Fo'] = FuncionObjetivo
    Soluciones['Capacidad'] = capacidad

    Respuestas.append(Soluciones)
    Ruta = []
    FuncionObjetivo = 0
    nodosVisitados = []
    
#print(Respuestas)    
min = 100000
indice =0
for i in range(len(Respuestas)):
    if Respuestas[i]['Fo'] < min:
        min = Respuestas[i]['Fo']
        indice = i

Ruta = Respuestas[indice]['ruta']
FoSol = Respuestas[indice]['Fo']
#print(Ruta)
#print(FoSol)



Ruta.pop(0)
a = []

rutas = []

fo = 0

cont = 0
conta = 0
for i in Ruta:  
    conta = conta + 1   
    
        
    a.append(i)
    
    
    if i == 0 and conta >1:
        
        dicc = {}
        
        a.insert(0,0)
        
        dicc['ruta'] = a
        
        dicc['fo'] = Fo
        
        dicc['Capacidad'] = capacidades[cont]
        
        rutas.append(dicc)
        
        a = []
        
        Fo = 0
        
        cont = cont+1
    
#agregar f.o
for i in range(len(rutas)):
    fo=0
    
    for j in range(len(rutas[i]['ruta'])-1):
        
        fo = round(fo+matDistancias[rutas[i]['ruta'][j],rutas[i]['ruta'][j+1]],2)
    
    rutas[i]['fo']= fo



    
#encontrar capacidades
for i in range(len(rutas)):
    
    capaci = capacidadInicial
    
    for j in range(len(rutas[i]['ruta'])-1):
        
        capaci = capaci- demandas[rutas[i]['ruta'][j]]
    rutas[i]["Capacidad"] = capaci
    
    

#Cambiar todos con todos y si mejora, me quedo con esa
foExp1 = 0
foTotalExp1 = 0
Posible = False
ener = 0
rutasBl =[]
rutasBl = copy.deepcopy(rutas)
for i in range(len(rutasBl)):
    foExp1 = 0
    negativo = False
    for j in range(len(rutasBl[i]['ruta'])):
        negativo = False
        for k in range(len(rutasBl[i]['ruta'])-1):
            negativo = False
            if rutasBl[i]['ruta'][j]!= 0 and rutasBl[i]['ruta'][k] != 0:
                
                rutasBl[i]['ruta'][j],rutasBl[i]['ruta'][k] = rutasBl[i]['ruta'][k],rutasBl[i]['ruta'][j]
                
                
                
                for l in range(len(rutasBl[i]['ruta'])-1):
                    foExp1 = round(foExp1+matDistancias[rutasBl[i]['ruta'][l],rutasBl[i]['ruta'][l+1]],2)
                    
                
                
                for n in range(len(rutasBl[i]['ruta'])-1):
                    
                    ener =  round(ener-matDistancias[rutasBl[i]['ruta'][n],rutasBl[i]['ruta'][n+1]],2)
                    if ener< 0:
                        negativo = True
                    
                    if rutasBl[i]['ruta'][n+1] > 21:
                        ener = energiaInicial
                        negativo = False
                
                

                if foExp1< rutasBl[i]['fo'] and negativo == False:
                    rutasBl[i]['fo'] = foExp1
                    
                #print (rutasBl[i]['ruta'])
                #print(foExp1)   
                    
                if foExp1 >  rutasBl[i]['fo'] or negativo == True:
                
                    rutasBl[i]['ruta'][j],rutasBl[i]['ruta'][k] = rutasBl[i]['ruta'][k],rutasBl[i]['ruta'][j]
                #print(negativo)

                
            foExp1 = 0
            

foTotalBl = 0
for i in range(len(rutasBl)):
    
    foTotalBl=0
    for j in range(len(rutasBl[i]['ruta'])-1):
        foTotalBl = round(foTotalBl+matDistancias[rutasBl[i]['ruta'][j],rutasBl[i]['ruta'][j+1]],2)
        rutasBl[i]['fo'] = foTotalBl

foTotalBl = 0
for i in range(len(rutasBl)):
    
    foTotalBl=0
    for j in range(len(rutasBl[i]['ruta'])-1):
        foTotalBl = round(foTotalBl+matDistancias[rutasBl[i]['ruta'][j],rutasBl[i]['ruta'][j+1]],2)
        rutasBl[i]['fo'] = foTotalBl

  
foTotalBl = 0
for i in range(len(rutasBl)):
    foTotalBl = round(foTotalBl+ rutasBl[i]['fo'],2)

#Función Objetivo Total:
foTotal = 0
for i in range(len(rutasBl)):
    foTotal = round(foTotal+ rutasBl[i]['fo'],2)

foTotal

#Cambio 2 con 2 
foVND = 0
rutaVNSFinal = []
rutasVNS2 = copy.deepcopy(rutasBl)
numRutaFactible = 0
indiceRutaFactible = 0
mejoraVNS2 =[]
foVNS2 =0
Mejoras2 =[]
solucionesVNS2 = []
foSolVNS2 = [] 

foVND = 0
foVND2 = 0
rutasVNS = copy.deepcopy(rutasBl)
#print(rutasVNS)
numRutaFactible = 0
indiceRutaFactible = 0
mejoraVNS =[]
Mejoras1 =[]
solucionesVNS = []
foSolVNS = [] 



for r in range (10):
    
    for i in range(len(rutasVNS2)-1):
    
        for j in range(len(rutasVNS2[i]["ruta"])-1):
        
            aa = rutasVNS2[i]["ruta"][j]
        
            b = rutasVNS2[i]["ruta"][j+1]
        
            if aa == 0:
                continue
        
            if b == 0:
                continue
        
            for k in range(len(rutasVNS2)-1):
            
                for l in range(len(rutasVNS2[k]["ruta"])-1):
                 
                    c = rutasVNS2[k]["ruta"][l]
                    if c == 0:
                        continue
        
                    d = rutasVNS2[k]["ruta"][l+1]
            
                    if d == 0:
                        continue          
                
                
                    rutasVNS2[k]["ruta"][l] = aa
                    rutasVNS2[k]["ruta"][l+1] = b
                    rutasVNS2[i]['ruta'][j] =c
                    rutasVNS2[i]['ruta'][j+1] =d

                
                
                #Calcular fo
                    for a in range(len(rutasVNS2[k]['ruta'])-1):
                        foVND = round(foVND+matDistancias[rutasVNS2[k]['ruta'][a],rutasVNS2[k]['ruta'][a+1]],2)
                    for a in range(len(rutasVNS2[i]['ruta'])-1):
                        foVND2 = round(foVND+matDistancias[rutasVNS2[i]['ruta'][a],rutasVNS2[i]['ruta'][a+1]],2)
                
                
                # calcular que la capacidad aguante.
                    capi = True
                    for z in range(len(rutasVNS2)):
                        capacidadVNS2 = capacidad
                    
                        for x in range(len(rutasVNS2[z]['ruta'])):
                            capacidadVNS2 = capacidad - demandas[rutasVNS2[z]['ruta'][x]]
                        if capacidadVNS2 < 0:
                            capi =False
                
                
                
                
                
                    #calcular que la energia aguante
                
                
                
                    negativo = False
                    for p in range(len(rutasVNS2)):
    
                        ener = energiaInicial
    
                        for u in range(len(rutasVNS2[p]['ruta'])-1):
            
                            ener =ener- matDistancias[rutasVNS2[p]['ruta'][u],rutasVNS2[p]['ruta'][u+1]] * consumo
                
                            if rutasVNS2[p]['ruta'][u+1] >21 or rutasVNS2[p]['ruta'][u+1] == 0:
                        
                                ener = energiaInicial
                            
                            if ener <0:
                            
                                negativo = True
                
                
                
                #calcular fo total nueva ruta:
                
                    foVNS2=0
                    for q in range(len(rutasVNS2)):
    
                        for w in range(len(rutasVNS2[q]['ruta'])-1):
        
                            foVNS2 = round(foVNS2+matDistancias[rutasVNS2[q]['ruta'][w],rutasVNS2[q]['ruta'][w+1]],2)
                            #print(str(rutas[i]['ruta'][j])+" "+ str(rutas[i]['ruta'][j+1]))
                        #print(foVNS)
                
                    foposible = True
                    if foVNS2 > foTotal:
                        foposible = False
                
                
                
                
                #print(str(k))        
                #print("la vieja ruta es " + str(rutas[k]['ruta']))
                #print("la vieja fo es " + str(rutas[k]['fo']))
                #print("la nueva ruta es " + str(rutasVNS[k]['ruta']))
                #print("la nueva fo es " + str(foVND))
                #print("la vieja ruta es " + str(rutas[i]['ruta']))
                #print("la vieja fo es " + str(rutas[i]['fo']))
                #print("la nueva ruta es " + str(rutasVNS[i]['ruta']))
                #print("la nueva fo es " + str(foVND2))
                
                
                    if foVND < rutasBl[k]['fo'] and foVND2 < rutasBl[i]['fo'] and negativo == False and capi == True and foposible == True and foVNS2<foTotalBl:
                    
                        #print(str(foVNS2)+" - "+ str(foTotal))
                        mejoraVNS2 = copy.deepcopy(rutasVNS2)
                        foTotalVNS2 = 0 
                        for y in range(len(rutasVNS2)):
                            foTotalVNS2=0
                            for t in range(len(rutasVNS2[y]['ruta'])-1):
                                foTotalVNS2 = round(foTotalVNS2+matDistancias[mejoraVNS2[y]['ruta'][t],mejoraVNS2[y]['ruta'][t+1]],2)
                                mejoraVNS2[y]['fo'] = foTotalVNS2
                        Mejoras2.append(mejoraVNS2)
                #guardar todos los posibles cambios:
                
                
                
                
                    rutasVNS2[k]["ruta"][l] = c
                    rutasVNS2[k]["ruta"][l+1] = d
                    rutasVNS2[i]['ruta'][j]  =aa
                    rutasVNS2[i]['ruta'][j+1] = b
                    foVND = 0
                    foVND2 =0
                    foVNS2 = 0
        

    tesisruta2 = 99999999
    for e in range(len(Mejoras2)):
        foSolVNS2 = 0
        for b in range(len(Mejoras2[e])):
            foSolVNS2 = round(foSolVNS2+ Mejoras2[e][b]['fo'],2)
        solucionesVNS2.append(foSolVNS2)
        if foSolVNS2 < tesisruta2:
            tesisruta2 = e
    if tesisruta2 < 50:
        rutasVNS2 = copy.deepcopy(Mejoras2[tesisruta2])


    
    
    #Cambio 1 con 1:





    for i in range(len(rutasVNS)-1):
    
        for j in range(len(rutasVNS[i]["ruta"])-1):
        
            aa = rutasVNS[i]["ruta"][j]
        
            #b = rutasVNS[i]["ruta"][j+1]
        
            if aa == 0:
                continue
        
            for k in range(len(rutasVNS)-1):
            
                for l in range(len(rutasVNS[k]["ruta"])-1):
                 
                    c = rutasVNS[k]["ruta"][l]
                    if c == 0:
                        continue
                
                        #d = rutasVNS[k]["ruta"][l+1]
            
          
                
                
                    rutasVNS[k]["ruta"][l] = aa
                    #rutasVNS[k]["ruta"][l+1] = b
                    rutasVNS[i]['ruta'][j] =c
                    #rutasVNS[i]['ruta'][j+1] =d

                
                
                    #Calcular fo
                    for a in range(len(rutasVNS[k]['ruta'])-1):
                        foVND = round(foVND+matDistancias[rutasVNS[k]['ruta'][a],rutasVNS[k]['ruta'][a+1]],2)
                    for a in range(len(rutasVNS[i]['ruta'])-1):
                        foVND2 = round(foVND+matDistancias[rutasVNS[i]['ruta'][a],rutasVNS[i]['ruta'][a+1]],2)
                
                
                    # calcular que la capacidad aguante.
                    capi = True
                    for z in range(len(rutas)):
                        capacidadVNS = capacidadInicial
                    
                        for x in range(len(rutasVNS[z]['ruta'])):
                            capacidadVNS = capacidad - demandas[rutasVNS[z]['ruta'][x]]
                        if capacidadVNS < 0:
                            capi = False
                
                
                
                
                
                    #calcular que la energia aguante
                
                
                
                    negativo = False
                    for p in range(len(rutasVNS)):
    
                        ener = energiaInicial
    
                        for u in range(len(rutasVNS[p]['ruta'])-1):
            
                            ener =ener- matDistancias[rutasVNS[p]['ruta'][u],rutasVNS[p]['ruta'][u+1]] * consumo
                
                            if rutasVNS[p]['ruta'][u+1] >21 or rutasVNS[p]['ruta'][u+1] == 0:
                        
                                ener = energiaInicial
                            
                            if ener <0:
                            
                                negativo = True
                
                
                
                    #calcular fo total nueva ruta:
                
                    foVNS=0
                    for q in range(len(rutas)):
    
                        for w in range(len(rutas[q]['ruta'])-1):
        
                            foVNS = round(foVNS+matDistancias[rutasVNS[q]['ruta'][w],rutasVNS[q]['ruta'][w+1]],2)
                        #print(str(rutas[i]['ruta'][j])+" "+ str(rutas[i]['ruta'][j+1]))
                    #print(foVNS)
                
                    foposible = True
                    if foVNS > foTotal:
                        foposible = False
                
                
                
                
                #print(str(k))        
                #print("la vieja ruta es " + str(rutas[k]['ruta']))
                #print("la vieja fo es " + str(rutas[k]['fo']))
                #print("la nueva ruta es " + str(rutasVNS[k]['ruta']))
                #print("la nueva fo es " + str(foVND))
                #print("la vieja ruta es " + str(rutas[i]['ruta']))
                #print("la vieja fo es " + str(rutas[i]['fo']))
                #print("la nueva ruta es " + str(rutasVNS[i]['ruta']))
                #print("la nueva fo es " + str(foVND2))
                
                
                    if foVND < rutasBl[k]['fo'] and foVND2 < rutasBl[i]['fo'] and negativo == False and capi == True and foposible == True and foVNS <foTotalBl:
     
                        #######print(str(foVNS)+" - "+ str(foTotal))
                        mejoraVNS = copy.deepcopy(rutasVNS)
                        foTotalVNS1 = 0
                        for y in range(len(rutasVNS)):
                            foTotalVNS1=0
                            for t in range(len(rutasVNS[y]['ruta'])-1):
                                foTotalVNS1 = round(foTotalVNS1+matDistancias[mejoraVNS[y]['ruta'][t],mejoraVNS[y]['ruta'][t+1]],2)
                                mejoraVNS[y]['fo'] = foTotalVNS1
                        Mejoras1.append(mejoraVNS)
                    
                #guardar todos los posibles cambios:
                
                
                
                #
                
                
                
                    rutasVNS[k]["ruta"][l] = c
                    #rutasVNS[k]["ruta"][l+1] = d
                    rutasVNS[i]['ruta'][j]  =aa
                    #rutasVNS[i]['ruta'][j+1] = b
                    foVND = 0
                    foVND2 =0
                    foVNS =0

                
                
    tesisruta = 99999999
    for e in range(len(Mejoras1)):
        foSolVNS = 0
        for b in range(len(Mejoras1[e])):
            foSolVNS = round(foSolVNS+ Mejoras1[e][b]['fo'],2)
        solucionesVNS.append(foSolVNS)
        if foSolVNS <= tesisruta:
            tesisruta = e
    if tesisruta <50:
        rutasVNS = copy.deepcopy(Mejoras1[tesisruta])
    
    

    #Función Objetivo Total 2 con 2:
    foTotal2v2 = 0
    for i in range(len(rutasVNS2)):
        foTotal2v2 = round(foTotal2v2+ rutasVNS2[i]['fo'],2)
               

    #Función Objetivo Total 1 con 1:
    foTotal1v1 = 0
    for i in range(len(rutasVNS)):
        foTotal1v1 = round(foTotal1v1+ rutasVNS[i]['fo'],2)

    # arreglar capacidades
    for i in range(len(rutasVNS2)):
    
        capaci = capacidadInicial
    
        for j in range(len(rutasVNS2[i]['ruta'])-1):
        
            capaci = capaci- demandas[rutasVNS2[i]['ruta'][j]]
    
        rutasVNS2[i]["Capacidad"] = capaci
    
    
    
    for i in range(len(rutasVNS)):
    
        capaci = capacidadInicial
    
        for j in range(len(rutasVNS[i]['ruta'])-1):
        
            capaci = capaci- demandas[rutasVNS[i]['ruta'][j]]
    
        rutasVNS[i]["Capacidad"] = capaci
    
    #escoger la que tenga capacidad positiva
    rutaFinalVNS2 = True
    
    for i in range(len(rutasVNS2)):
        if rutasVNS2[i]['Capacidad'] < 0:
            rutaFinalVNS2 = False
    
    
    rutaFinalVNS = True
    
    for i in range(len(rutasVNS)):
        if rutasVNS[i]['Capacidad'] < 0:
            rutaFinalVNS = False
    
    menorRutaVNS = 0
    #encontrar menor
    if foTotal1v1 < foTotal2v2 and rutaFinalVNS == True:
        menorRutaVNS = 1
    else:
        menorRutaVNS = 2
    
    if menorRutaVNS == 1 and rutaFinalVNS == True:
        rutasVNSFinal = copy.deepcopy(rutasVNS)
    elif menorRutaVNS == 2 and rutaFinalVNS2 == True:
        rutasVNSFinal = copy.deepcopy(rutasVNS2)  
    
    if menorRutaVNS == 1 and rutaFinalVNS == False:
        rutasVNSFinal = copy.deepcopy(rutasVNS2)
    elif menorRutaVNS == 2 and rutaFinalVNS2 == False:
        rutasVNSFinal = copy.deepcopy(rutasVNS)
    

for i in range(len(rutas)):
    
    capaci = capacidadInicial
    
    for j in range(len(rutas[i]['ruta'])-1):
        
        capaci = capaci- demandas[rutas[i]['ruta'][j]]
    rutas[i]["Capacidad"] = capaci

for i in range(len(rutasVNS2)):
    
    capaci = capacidadInicial
    
    for j in range(len(rutasVNS2[i]['ruta'])-1):
        
        capaci = capaci- demandas[rutasVNS2[i]['ruta'][j]]
    rutasVNS2[i]["Capacidad"] = capaci
    
    
for i in range(len(rutasVNS)):
    
    capaci = capacidadInicial
    
    for j in range(len(rutasVNS[i]['ruta'])-1):
        
        capaci = capaci- demandas[rutasVNS[i]['ruta'][j]]
    rutasVNS[i]["Capacidad"] = capaci
    
    
    
rutas
#Función Objetivo Total:
foTotal = 0
for i in range(len(rutas)):
    foTotal = round(foTotal+ rutas[i]['fo'],2)

print(foTotal)

rutasBl

#Función Objetivo Total:
foTotal = 0
for i in range(len(rutasBl)):
    foTotal = round(foTotal+ rutasBl[i]['fo'],2)

print(foTotal)

rutasVNSFinal

#Función Objetivo Total:
foTotal = 0
for i in range(len(rutasVNSFinal)):
    foTotal = round(foTotal+ rutasVNSFinal[i]['fo'],2)

print(foTotal)

# Crear gráficas


import matplotlib.pyplot as plt
for i in range(len(rutas)):
    ruta = rutas[i]['ruta']  # lista de nodos
    coordenadas = distancias  # lista de coordenadas

    # Obtener las coordenadas x e y de cada nodo
    x = [coordenadas[nodo-1][0] for nodo in ruta]
    y = [coordenadas[nodo-1][1] for nodo in ruta]

    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Graficar los nodos
    ax.scatter(x, y)

    # Unir los nodos con líneas
    ax.plot(x, y)


    for i, nodo in enumerate(ruta):
        ax.annotate(str(nodo), (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Mostrar el gráfico
    plt.show()
    

# Crear gráficas Búsqueda local


import matplotlib.pyplot as plt
for i in range(len(rutasBl)):
    ruta = rutasBl[i]['ruta']  # lista de nodos
    coordenadas = distancias  # lista de coordenadas

    # Obtener las coordenadas x e y de cada nodo
    x = [coordenadas[nodo-1][0] for nodo in ruta]
    y = [coordenadas[nodo-1][1] for nodo in ruta]

    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Graficar los nodos
    ax.scatter(x, y)

    # Unir los nodos con líneas
    ax.plot(x, y)


    for i, nodo in enumerate(ruta):
        ax.annotate(str(nodo), (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Mostrar el gráfico
    plt.show()
    
# Crear gráficas VNS 2 con 2 

# Crear gráficas Búsqueda local


import matplotlib.pyplot as plt
for i in range(len(rutasVNSFinal)):
    ruta = rutasVNSFinal[i]['ruta']  # lista de nodos
    coordenadas = distancias  # lista de coordenadas

    # Obtener las coordenadas x e y de cada nodo
    x = [coordenadas[nodo-1][0] for nodo in ruta]
    y = [coordenadas[nodo-1][1] for nodo in ruta]

    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # Graficar los nodos
    ax.scatter(x, y)

    # Unir los nodos con líneas
    ax.plot(x, y)


    for i, nodo in enumerate(ruta):
        ax.annotate(str(nodo), (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Mostrar el gráfico
    plt.show()
    

end_time = time.time()

computing_time = end_time - start_time

print("Tiempo de cómputo:", computing_time, "segundos")


