from selenium import webdriver 

from business_info_fetcher.krajowy_rejestr_sadowy import scrape_krs_dokumenty_finansowe
from business_info_fetcher.krajowy_rejestr_sadowy.krs_dokumenty_finansowe import KRSDokumentyFinansowe

import time

def test_krs_dokumenty_finansowe_class():
    krs_df_api = KRSDokumentyFinansowe()
    krs_df_api.initialize_driver()
    assert (isinstance(krs_df_api.driver, webdriver.Chrome))
    assert krs_df_api.information_about_no_documents_to_display_is_present == False
    assert krs_df_api.information_about_table_with_available_documents_is_present == False
    assert krs_df_api.is_business_page_open == False
    krs_df_api.search_krs("0000057814")
    assert krs_df_api.throttling_error_from_webpage == False
    assert krs_df_api.information_about_no_documents_to_display_is_present == False
    assert krs_df_api.information_about_table_with_available_documents_is_present == True
    assert krs_df_api.is_business_page_open == True 
    assert krs_df_api.number_of_current_page == 1
    # NOTE - prone to change if number of available documents increases
    assert krs_df_api.number_of_pages_with_documents == 4
    doc_list = krs_df_api.get_available_documents_list()
    assert len(doc_list) > 0
    krs_df_api.search_krs("0000000000")
    assert krs_df_api.throttling_error_from_webpage == False
    assert krs_df_api.information_about_no_documents_to_display_is_present == True
    assert krs_df_api.information_about_table_with_available_documents_is_present == False
    assert krs_df_api.is_business_page_open == True 

# def test_krs_dokumenty_finansowe_class_next_button():
#     krs_df_api = KRSDokumentyFinansowe()
#     krs_df_api.initialize_driver()
#     assert krs_df_api.number_of_current_page == 1
#     # NOTE - prone to change if number of available documents increases
#     assert krs_df_api.number_of_pages_with_documents == 4
#     krs_df_api.go_to_next_page()
#     assert krs_df_api.number_of_current_page == 2
    

# def test_krs_dokumenty_finansowe_function():
#     result = scrape_krs_dokumenty_finansowe("0000057814")
