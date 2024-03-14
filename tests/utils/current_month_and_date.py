from datetime import datetime


class CurrentMonthAndYear:
    def __init__(self):
        pass

    def current_month_and_year(self):
        now = datetime.now()
        month_year_format = now.strftime("%m/%y")
        return month_year_format
