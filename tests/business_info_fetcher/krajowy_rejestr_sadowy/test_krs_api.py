from business_info_fetcher.krajowy_rejestr_sadowy import scrape_krs_api
from business_info_fetcher.errors import InvalidTypeOfReportPassed, NoEntityFoundError

def test_scrape_krs_api_always_returns_dict_and_proper_error_messages():
    proper_krs = scrape_krs_api('odpis_aktualny', '0000057814', 'P')
    invalid_krs = scrape_krs_api('odpis_aktualny', '000000000', 'P')
    invalid_rejestr = scrape_krs_api('odpis_aktualny', '0000057814', 'X')
    invalid_type_of_report = scrape_krs_api('xxxxxx', '0000057814', 'P')

    assert isinstance(proper_krs, dict)
    assert isinstance(invalid_krs, dict)
    assert isinstance(invalid_rejestr, dict)
    assert proper_krs["data"]["odpis"]["naglowekA"]["numerKRS"] == "0000057814"
    assert invalid_krs["data"] == "error"
    assert invalid_rejestr["data"] == "error"
    assert invalid_krs["error_type"] == NoEntityFoundError.__name__
    assert invalid_rejestr["error_type"] == NoEntityFoundError.__name__
    assert invalid_type_of_report["error_type"] == InvalidTypeOfReportPassed.__name__