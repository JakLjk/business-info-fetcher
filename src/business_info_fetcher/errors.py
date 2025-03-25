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