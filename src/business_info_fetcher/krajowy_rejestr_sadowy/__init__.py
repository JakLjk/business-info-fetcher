from typing import Literal

from .krs_api import KRSApi
from .krs_dokumenty_finansowe import KRSDokumentyFinansowe
from ..errors import NoEntityFoundError, InvalidTypeOfReportPassed

def scrape_krs_api(
        type_of_report: Literal["odpis_aktualny",
                                "odpis_pelny"],
        krs: str,
        rejestr: Literal["S", "P"]) -> dict:
    krs_api = KRSApi()
    if  type_of_report  == "odpis_aktualny":
        try:
            return {"data":krs_api.get_odpis_aktualny(krs, rejestr)}
        except NoEntityFoundError as nefe:
            return {"data":"error",
                    "error_type": type(nefe).__name__,
                    "error_message": str(nefe)}
        except Exception as e:
            return {"data":"error", 
                    "error_type": type(e).__name__,
                    "error_message": str(e)}
    elif type_of_report == "odpis_pelny":
        try:
            return {"data":krs_api.get_odpis_pelny(krs, rejestr)}
        except NoEntityFoundError as nefe:
            return {"data":"error",
                    "error_type": type(nefe).__name__,
                    "error_message": str(nefe)}
        except Exception as e:
            return {"data":"error", 
                    "error_type":type(e).__name__,
                    "error_message": str(e)}
    else:   
        return {"data": "error",
                "error_type": InvalidTypeOfReportPassed.__name__,
                "error_message": "Invalid type_of_report passed"}


def scrape_krs_dokumenty_finansowe(krs):
    krs_dokumenty_finansowe = KRSDokumentyFinansowe()
    krs_dokumenty_finansowe.initialize_driver()
    krs_dokumenty_finansowe.search_krs(krs)

