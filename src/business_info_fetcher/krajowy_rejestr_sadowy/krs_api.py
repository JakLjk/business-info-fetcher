import requests
import json

from string import Template
from typing import Literal, Union

from .links import KRS_API
class KRSApi:
    """Klasa do pobierania danych z API Krajowego Rejestru Sądowego
       Zakres informacyjny udostępnianych danych odpowiada odpisom z KRS, zupełnemu i aktualnemu."""
    def __init__(self):
        pass

    def get_odpis_aktualny(self, krs: str, rejestr: Literal["S", "P"]) -> dict:
        """krs  - numer KRS danego przedsiębiorstwa
            rejestr - P (dla przedsiębiorstw), S (dla stowarzyszeń)
        """
        url = KRS_API.get("odpis_aktualny").format(krs=krs, rejestr=rejestr)
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Nie znaleziono danych")
        return response.json()
    
    def get_odpis_pelny(self, krs: Union[int, str], rejestr: Literal["S", "P"]) -> dict:
        """krs  - numer KRS danego przedsiębiorstwa
           rejestr - P (dla przedsiębiorstw), S (dla stowarzyszeń)
        """
        url = KRS_API.get("odpis_pelny").format(krs=krs, rejestr=rejestr)
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("Nie znaleziono danych")
        return response.json()
    
