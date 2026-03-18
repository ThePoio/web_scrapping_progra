"""
Este programa tiene como finalidad extraer los simbolos de las compañias
del S&P 500 de Wikipedia, a través de un request.
"""
import requests
from bs4 import BeautifulSoup
import time

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

    def obtencion_de_html_SP500(self):
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'} #Metadatos para informar al servidor
        response=requests.get(self._url,headers=headers) #(pagina,headers)

        # Si el status code es inválido, que nos saque
        if response.status_code!=200:
            print('No se pudo acceder a la página')
            print(f'Código error:{response.status_code}')
            return []
        
        yield from self.extraccion_de_simbolos(response.text)
        #Vamos a llamar a extracción de simbolos
        
# wiki=WikiWorker()
# for simbolo in wiki.obtencion_de_html_SP500():
#     time.sleep(0.2)
#     print(simbolo)