class NoEntityFoundError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidTypeOfReportPassed(Exception):
    def __init__(self, *args):
        super().__init__(*args)
    

class BusinessSiteNotLoaded(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class WebpageThrottlingError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class NoDataToScrape(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class WebpageSessionExpired(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class DocumentNotFound(Exception):
    def __init__(self, *args):
        super().__init__(*args)