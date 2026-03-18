"""
Esta clase va a generar hilos que tomen un simbolo del generador y busquen
el valor correspondiente de la acción en yeahoo finance
"""

### Librerias
import requests
from lxml import html
import time
import threading
from User_agent import get_random_user_agent

class YahooFinancePriceWorker(threading.Thread):
    def __init__(self,simbolo):
        super().__init__()
        self._base_url='https://finance.yahoo.com/quote/'
        self.xpath_cierre='//*[@id="main-content-wrapper"]/section[1]/div[2]/div[1]/section/div/section[1]/div[1]/span[1]'
        self.simbolo=simbolo
        self.start()

    def run(self):
        try:
            url=self._base_url+self.simbolo
            headers={'User-Agent':get_random_user_agent()}
            time.sleep(0.1)
            response=requests.get(url,headers=headers)
            if response.status_code!=200:
                print('Error de conexion. codigo: ', response.status_code)
                return
            contenido=html.fromstring(response.text)
            precio=contenido.xpath(self.xpath_cierre)[0].text.strip()
            print(f'{self.simbolo}: {precio}')
        except Exception as e:
            print(f'Simbolo: {self.simbolo}, error: {e}')



        
