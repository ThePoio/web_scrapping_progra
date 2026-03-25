"""
En este modulo se controla la creacion de hilos para cada simbolo del s&p500
"""

#Importacion de librerias
import time
from WikiWorker import WikiWorker
from YahooFinanceWorker import YahooFinancePriceWorker
import threading
import queue

try:

    wikiworker = WikiWorker()
    hilos = []

    
    semaforo = threading.Semaphore(5)
    for simbolo in wikiworker.obtencion_de_html_SP500():
        with semaforo:
            #time.sleep(0.2) #Usar el timesleep es la opcion logica para evitar el error 429
            hiloyahooworker = YahooFinancePriceWorker(simbolo)
            hilos.append(hiloyahooworker)

    for hilo in hilos:
        hilo.join()

    print()
except Exception as e:
    print("Hubo un error de tipo",e)

finally:
    print("Web scrapping finalizado :D ¬w¬")
