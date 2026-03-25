"""
Esta clase va a generar hilos que tomen un simbolo del generador y busquen
el valor correspondiente de la acción en yeahoo finance
"""

### Librerias
import requests
from lxml import html
import time
import random
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
            max_reintentos=5

            for intento in range(max_reintentos):
                try:
                    time.sleep(0.1)
                    response=requests.get(url,headers=headers,timeout=10)
                    response.raise_for_status()
                    break
                except requests.RequestException as error:
                    if intento == max_reintentos - 1:
                        print(f'Simbolo: {self.simbolo}, fallo tras {max_reintentos} intentos: {error}')
                        return

                    # Backoff exponencial con jitter para espaciar reintentos.
                    espera=(2**intento)+random.uniform(0,1)
                    print(f'Simbolo: {self.simbolo}, intento {intento + 1} fallido. Reintentando en {espera:.2f}s...')
                    time.sleep(espera)

            contenido=html.fromstring(response.text)
            precio=contenido.xpath(self.xpath_cierre)[0].text.strip()
            print(f'{self.simbolo}: {precio}')
        except Exception as e:
            print(f'Simbolo: {self.simbolo}, error: {e}')



        
