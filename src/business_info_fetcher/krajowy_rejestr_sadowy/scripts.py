


class KRSParser:
    def __init__(self):
        self.__url_odpis_aktualny = "https://api-krs.ms.gov.pl/api/krs/OdpisAktualny/{}?rejestr={}&format=json"
        self.__url_odpis_pelny = "https://api-krs.ms.gov.pl/api/krs/OdpisPelny/{}?rejestr={}&format=json"