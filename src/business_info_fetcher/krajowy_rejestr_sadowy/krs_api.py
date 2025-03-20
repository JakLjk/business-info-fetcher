import requests
import json

from string import Template
from typing import Literal, Union

from links import KRS_API
class KRSApi:
    def __init__(self):
        pass

    def get_odpis_aktualny(self, krs: Union[int, str], rejestr: Literal["S", "P"]) -> dict:
        """krs  - numer KRS danego przedsiębiorstwa
           rejestr - P (dla przedsiębiorstw), S (dla stowarzyszeń)
        """
        url = KRS_API.get("odpis_aktualny").format(krs=krs, rejestr=rejestr)
        response = requests.get(url)
        return response.json()
    
    def get_odpis_pelny(self, krs: Union[int, str], rejestr: Literal["S", "P"]) -> dict:
        """krs  - numer KRS danego przedsiębiorstwa
           rejestr - P (dla przedsiębiorstw), S (dla stowarzyszeń)
        """
        url = KRS_API.get("odpis_pelny").format(krs=krs, rejestr=rejestr)
        response = requests.get(url)
        return response.json()
    
    def get_historia_zmian(self, dzien:str, godzinaOd:int, godzinaDo:int) -> dict:
        """dzien - późniejszy niż 2021-12-08
           godzinaOd - godzina początkowa biuletynu, w formacie 24-godzinnym (GG, od 00 do 23)
           godzinaDo - godzina końcowa biuletynu w formacie 24-godzinnym (GG, od 00 do 23)
        """
        url = KRS_API.get("historia_zmian").format(dzien=dzien, godzinaOd=godzinaOd, godzinaDo=godzinaDo)
        response = requests.get(url)
        return response.json()

    



krs_api = KRSApi() 
print(krs_api.get_odpis_aktualny("0000057814", "G"))