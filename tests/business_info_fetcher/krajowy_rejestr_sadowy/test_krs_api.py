from business_info_fetcher.krajowy_rejestr_sadowy.krs_api import KRSApi

def test_krs_api_always_returns_json():
    krs_api = KRSApi()
    assert isinstance(krs_api.get_odpis_aktualny("0000057814", "P"), dict)
    assert isinstance(krs_api.get_odpis_pelny("000000000", "P"), dict)