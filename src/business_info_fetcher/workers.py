from typing import Literal

from .krajowy_rejestr_sadowy.krs_api import KRSApi


def worker_scrape_krs_api(
        type_of_report: Literal["odpis_aktualny",
                                "odpis_pelny",
                                "wszystkie"],
        krs: int,
        rejestr: Literal["S", "P"]) -> dict:
    krs_api = KRSApi()
    if type_of_report == "wszystkie":
        {"odpis_aktualny":krs_api.get_odpis_aktualny(krs, rejestr),
         "odpis_pelny":krs_api.get_odpis_pelny(krs, rejestr)}
    elif type_of_report  == "odpis_aktualny":
        return {"odpis_aktualny":krs_api.get_odpis_aktualny(krs, rejestr)}
    elif type_of_report == "odpis_pelny":
        return {"odpis_pelny":krs_api.get_odpis_pelny(krs, rejestr)}
    else:
        raise ValueError("Niepoprawny typ raportu")


def worker_scrape_krs_dokumenty_finansowe(krs, rejestr):
    pass