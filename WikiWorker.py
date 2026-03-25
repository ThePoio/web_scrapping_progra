"""
Este programa tiene como finalidad extraer los simbolos de las compañias
del S&P 500 de Wikipedia, a través de un request.
"""
from urllib import response

import requests
from bs4 import BeautifulSoup
import time
import random

class WikiWorker():
    def __init__(self):
        # URL del S&P 500
        self._url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    @staticmethod
    def extraccion_de_simbolos(paginahtml): #Página html es la página de referencia
        soup=BeautifulSoup(paginahtml,'lxml') # Parser con lxml
        tabla=soup.find(id='constituents')
        if not tabla:
            print('No se encontró la tabla')
            return []
        filas=tabla.find_all('tr')
        for fila in filas[1:]: #Todas las filas excepto la primera (encabezado)
            simbolo=fila.find('td').text.strip('\n')
            yield simbolo

    def obtencion_de_html_SP500(self, macx_reintentos=5):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'} #Metadatos para informar al servidor
        for intento in range(macx_reintentos):
            try:
                response=requests.get(self._url,headers=headers,timeout=10) #(pagina,headers)
                response.raise_for_status()
                yield from self.extraccion_de_simbolos(response.text)
                return
            except requests.RequestException as error:
                if intento == macx_reintentos - 1:
                    print(f'Fallo tras {macx_reintentos} intentos: {error}')
                    return []

                # Backoff exponencial con jitter para espaciar los reintentos.
                espera=(2**intento)+random.uniform(0,1)
                print(f'Intento {intento + 1} fallido: {error}. Reintentando en {espera:.2f}s...')
                time.sleep(espera)
        #Vamos a llamar a extracción de simbolos
        
# wiki=WikiWorker()
# for simbolo in wiki.obtencion_de_html_SP500():
#     time.sleep(0.2)
#     print(simbolo)