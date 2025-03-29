from typing import Literal

from .krs_api import KRSApi
from .krs_dokumenty_finansowe import KRSDokumentyFinansowe
from ..errors import (NoEntityFoundError,
                        InvalidTypeOfReportPassed, 
                        BusinessSiteNotLoaded,
                        WebpageThrottlingError,
                        NoDataToScrape)

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


def scrape_krs_dokumenty_finansowe_document_list(krs:str, job_id:str):
    krs_dokumenty_finansowe = KRSDokumentyFinansowe(job_id)
    try:
        krs_dokumenty_finansowe.initialize_driver()
        krs_dokumenty_finansowe.search_krs(krs)
        data = krs_dokumenty_finansowe.get_available_documents_list()
    except WebpageThrottlingError as wte:
        return {"data":"error",
                "error_type":type(wte).__name__,
                "error_message":str(wte)}
    except BusinessSiteNotLoaded as bsnl:
        return {"data":"error",
                "error_type":type(bsnl).__name__,
                "error_message":str(bsnl)}
    except NoDataToScrape as ndts:
        return {"data":"No records"}
    finally:
        krs_dokumenty_finansowe.driver.quit()
    return {"data":data}
    
def scrape_krs_dokumenty_finansowe_document_file(krs:str,
                                                 document_name:str,
                                                 date_from:str,
                                                 date_to:str,
                                                 job_id:str):
    krs_dokumenty_finansowe = KRSDokumentyFinansowe(job_id)
    try:
        krs_dokumenty_finansowe.initialize_driver()
        krs_dokumenty_finansowe.search_krs(krs)
        saved_to = krs_dokumenty_finansowe.get_document_by_name_and_date(
            document_name=document_name,
            date_from=date_from,
            date_to=date_to
        )
    except WebpageThrottlingError as wte:
        return {"data":"error",
                "error_type":type(wte).__name__,
                "error_message":str(wte)}
    except BusinessSiteNotLoaded as bsnl:
        return {"data":"error",
                "error_type":type(bsnl).__name__,
                "error_message":str(bsnl)}
    except NoDataToScrape as ndts:
        return {"data":"No records"}
    finally:
        krs_dokumenty_finansowe.driver.quit()
    return {"data":{"saved_to_path":saved_to}}

def scrape_krs_dokumenty_finansowe_all_documents(krs:str,
                                                 job_id:str):
    krs_dokumenty_finansowe = KRSDokumentyFinansowe(job_id)
    try:
        krs_dokumenty_finansowe.initialize_driver()
        krs_dokumenty_finansowe.search_krs(krs)
        saved_to = krs_dokumenty_finansowe.get_all_documents()
    except WebpageThrottlingError as wte:
        return {"data":"error",
                "error_type":type(wte).__name__,
                "error_message":str(wte)}
    except BusinessSiteNotLoaded as bsnl:
        return {"data":"error",
                "error_type":type(bsnl).__name__,
                "error_message":str(bsnl)}
    except NoDataToScrape as ndts:
        return {"data":"No records"}
    finally:
        krs_dokumenty_finansowe.driver.quit()
    return {"data":{"saved_to_paths":saved_to}}
        