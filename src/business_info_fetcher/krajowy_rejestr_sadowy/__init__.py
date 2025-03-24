from typing import Literal

from .krs_api import KRSApi


def scrape_krs_api(
        type_of_report: Literal["odpis_aktualny",
                                "odpis_pelny"],
        krs: str,
        rejestr: Literal["S", "P"]) -> dict:
    krs_api = KRSApi()
    if  type_of_report  == "odpis_aktualny":
        return {"data":krs_api.get_odpis_aktualny(krs, rejestr)}
    elif type_of_report == "odpis_pelny":
        return {"data":krs_api.get_odpis_pelny(krs, rejestr)}
    else:   
        return {"data": "Record not found"}

def scrape_krs_dokumenty_finansowe(krs, rejestr):
    pass