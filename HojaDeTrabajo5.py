#Juan Manuel Marroquin 19845
#Hoja de Trabajo 5
#Algoritmos y Estructuras de Datos
import simpy
import random

#Semilla para el random
RANDOM_SEED = 22
# Numero de procesos
Procesos = 25
#Capacidad de memoria del procesador
Memoria = 100
#Minima cantidad de instrucciones
Min_p = 1
#Maxima cantidad de instrucciones
Max_p = 100         

#Definicion de los procesos
def function(env, tProceso,codigo,RAM, memoriaNecesaria,cantInstrucciones,IPM):
    
    #Se imprime el tiempo de llegada
        yield env.timeout(tProceso)
        print('Tiempo: %f - %s solicita %d de memoria ram' % (env.now, codigo, memoriaNecesaria))
        tiempo_llegada = env.now
    
    #Se solicita un espacio de memoria de la RAM
        yield RAM.get(memoriaNecesaria)
        print('Tiempo: %f - %s (Solicitud de RAM)%d de RAM, aceptada' % (env.now, codigo, memoriaNecesaria))
    
    #Instrucciones completadas
        cantInstC = 0
        while cantInstC < cantInstrucciones:
        #conexion a la CPU (Estado Ready)
                with CPU.request() as req:
                        yield req
                        #Obtener el numero de instrucciones a realizar
                        if(cantInstrucciones-cantInstC)>=IPM:
                                #Mas de 3 instrucciones a realizar
                                instEfectuar = IPM

                        else:
                                #Menos de 3 instrucciones a realizar
                                instEfectuar=(cantInstrucciones-cantInstC)
            #Se imprime el tiempo que se tomara en realizar la instruccion
                        print('Tiempo necesario: %f - %s (ready) cpu %d ' % (env.now, codigo, instEfectuar))
             #Se toma la cantidad de recursos necesaria
                        yield env.timeout(instEfectuar/IPM)   #Error
            #Se actualiza cantidad de instrucciones realizadas
                        cantInstC += instEfectuar
             
        #Se genera un random para ver si se atiende el proceso o se pone en espera
                        validador = random.randint(1,2)
                        if validador == 1 and instEfectuar<IPM:
                                with Wait.request() as reqE:
                                        yield reqE
                #Espera el tiempo necesario para hacer otra solicitud
                                yield env.timeout(1)
    
    #Se retornan los recursos a la "memmoria"
        yield RAM.put(memoriaNecesaria)
        print('Fin proceso %f - %s, Utilizo %d de memoria' % (env.now, codigo, memoriaNecesaria))

    
#Inicio de la simulacion
print('Simulacion de procesos')
#Se crea siempre el mismo random, para poder comparar resultados despues
random.seed(RANDOM_SEED)
#Se crea el ambiente de simulacion
env = simpy.Environment()
#Se podra realizar solo un proceso a la vez
CPU = simpy.Resource(env, capacity = 2)
#Uso de container, tiene capacidad de 100, y comienza con toda la capacidad
RAM = simpy.Container(env,init=Memoria,capacity= 100)
#Capacidad de cola 
Wait= simpy.Resource(env, capacity = 1)
#Intrucciones por minuto CPU
instPM = 3.0           
constante = 1

#Creacion de procesos
for i in range(Procesos):
    #Memoria a solicitar
    tProceso = random.expovariate(1.0/constante)
    memoriaNecesaria= random.randint(Min_p,Max_p)
    #Intrucciones que necesitaran 
    cantInstrucciones= random.randint(Min_p,Max_p) 
    env.process(function(env, tProceso,'Proceso %d' % i,RAM, memoriaNecesaria,cantInstrucciones,instPM))

#Comienza el proceso de ejecucion
#Se corre la simulacion hasta que no existan mas eventos
env.run()                               