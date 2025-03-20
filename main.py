from src.business_info_fetcher.krajowy_rejestr_sadowy import fetch_information_from_krs_api
from src.business_info_fetcher.scripts import save_to_json

save_to_json(
    fetch_information_from_krs_api("odpis_aktualny", "0000057814", "P")
    , "output.json")
