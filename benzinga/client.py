import requests, json
import datetime as dt
from benzinga_errors import (TokenAuthenticationError, RequestAPIEndpointError, IncorrectParameterEntry,
                             URLIncorrectlyFormattedError )

class Benzinga: 

    def __init__(self, api_token):

        self.token = api_token
        self.headers = {'accept': 'application/json'}
        self.url_dict = {"API v1": "https://api.benzinga.com/api/v1" ,"API v2": "https://api.benzinga.com/api/v2/",
                         "Data v3": "http://data-api.zingbot.bz/rest/v3/","Data v2": "https://data.benzinga.com/rest/v2/"}
        self.endpoint_type = {"Calendar / Fundamentals": self.url_dict["API v2"], "Charts": self.url_dict["Data v2"],
                              "Instruments": self.url_dict["Data v3"]}

        self.__token_check__(self.token)

    def __token_check__(self, api_token):
        end_date = dt.date.today().strftime('%Y-%m-%d')
        company_ticker = "AAPL"
        params = {'token': api_token, 'parameters[date_to]': end_date,
                  'parameters[tickers]': company_ticker}
        try:
            ratingsUrl = self.__url_call__("Calendar / Fundamentals", "calendar", "dividends")
            ratings = requests.get(ratingsUrl, headers= self.headers, params=params)
            if ratings.status_code == 401:
                raise TokenAuthenticationError
        except TokenAuthenticationError as t:
            print("%sYour token is not valid. Please try again" % (t))


    def __url_call__(self, type , part_one = "", part_two = ""):  # Private Method to modify requests calls
        if type == "Calendar / Fundamentals":
            url_string = self.endpoint_type[type] + str("%s/%s"%(part_one, part_two))
        elif type == "Chart":
            url_string = self.endpoint_type[type] + "chart"
        elif type == "Instruments":
            url_string = self.endpoint_type[type] + "instruments"
        else:
            raise URLIncorrectlyFormattedError
        return url_string

    def instruments(self, fields = "", query = "", start_date = "", to = "", asOf = "", sortfield = "", sortdir = ""):
        params_passed_in = locals()
        params = {}
        for key, value in params_passed_in.items():
            if key == "self":
                continue
            if key == "start_date":
                key = "from"
            if value != "":
                params[key] = value
        instrumentsUrl = self.__url_call__("Instruments")
        instruments = requests.get(instrumentsUrl, headers=self.headers, params=params)
        print(instruments.url)
        return instruments.json()

    "Calendar Oriented Data"

    def dividends(self, page=None, pagesize=None, base_date=None, date_from=None, date_to=None,
                  company_tickers=None, importance=None, date_sort=None, updated_params=None,
                  div_yield_operation=None, div_yield = None):
        params = {'token': self.token, "page": page, "pagesize": pagesize, "parameters[date]": base_date,
                  "parameters[date_from]": date_from, "parameters[date_to]": date_to, "parameters[tickers]"
                  :company_tickers, "parameters[importance]": importance, "parameters[date_sort]": date_sort,
                  "parameters[updated]": updated_params, "paramaters[dividend_yield_operation]": div_yield_operation,
                  "parameters[dividend_yield]": div_yield}
        try:
            dividends_url = self.__url_call__("Calendar / Fundamentals", "calendar", "dividends")
            dividends = requests.get(dividends_url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return dividends.json()

    def earnings(self, page=None, pagesize=None, base_date=None, date_from=None, date_to=None,
                  company_tickers=None, importance=None, date_sort=None, updated_params=None):
        params = {'token': self.token, "page": page, "pagesize": pagesize, "parameters[date]": base_date,
                  "parameters[date_from]": date_from, "parameters[date_to]": date_to, "parameters[tickers]"
                  :company_tickers, "parameters[importance]": importance, "parameters[date_sort]": date_sort,
                  "parameters[updated]": updated_params}
        try:
            earnings_url = self.__url_call__("Calendar / Fundamentals", "calendar", "earnings")
            earnings = requests.get(earnings_url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return earnings.json()

    def splits(self, page=None, pagesize=None, base_date=None, date_from=None, date_to=None,
                  company_tickers=None, importance=None, date_sort=None, updated_params=None):
        params = {'token': self.token, "page": page, "pagesize": pagesize, "parameters[date]": base_date,
                  "parameters[date_from]": date_from, "parameters[date_to]": date_to, "parameters[tickers]"
                  :company_tickers, "parameters[importance]": importance, "parameters[date_sort]": date_sort,
                  "parameters[updated]": updated_params}
        try:
            splits_url = self.__url_call__("Calendar / Fundamentals", "calendar", "splits")
            splits = requests.get(splits_url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return splits.json()

    def economics(self, page=None, pagesize=None, base_date=None, date_from=None, date_to=None,
                    company_tickers=None, importance=None, date_sort=None, updated_params=None, country=None):
        params = {'token': self.token, "page": page, "pagesize": pagesize, "parameters[date]": base_date,
                  "parameters[date_from]": date_from, "parameters[date_to]": date_to, "parameters[tickers]"
                  : company_tickers, "parameters[importance]": importance, "parameters[date_sort]": date_sort,
                  "parameters[updated]": updated_params, "country": country}
        try:
            economics_url = self.__url_call__("Calendar / Fundamentals", "calendar", "economics")
            economics = requests.get(economics_url, headers= self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return economics.json()

    def guidance(self, page=None, pagesize=None, base_date=None, date_from=None, date_to=None,
                    company_tickers=None, importance=None, date_sort=None, updated_params=None, country=None):
        params = {'token': self.token, "page": page, "pagesize": pagesize, "parameters[date]": base_date,
                  "parameters[date_from]": date_from, "parameters[date_to]": date_to, "parameters[tickers]"
                  : company_tickers, "parameters[importance]": importance, "parameters[date_sort]": date_sort,
                  "parameters[updated]": updated_params, "country": country}
        try:
            guidance_url = self.__url_call__("Calendar / Fundamentals", "calendar", "economics")
            guidance = requests.get(guidance_url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return guidance.json()

    def ipo(self, page=None, pagesize=None, base_date=None, date_from=None, date_to=None,
                  company_tickers=None, importance=None, date_sort=None, updated_params=None):
        params = {'token': self.token, "page": page, "pagesize": pagesize, "parameters[date]": base_date,
                  "parameters[date_from]": date_from, "parameters[date_to]": date_to, "parameters[tickers]"
                  :company_tickers, "parameters[importance]": importance, "parameters[date_sort]": date_sort,
                  "parameters[updated]": updated_params}
        try:
            ipo_url = self.__url_call__("Calendar / Fundamentals", "calendar", "ipos")
            ipo = requests.get(ipo_url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return ipo.json()

    def retail(self, page=None, pagesize=None, base_date=None, date_from=None, date_to=None,
                  company_tickers=None, importance=None, date_sort=None, updated_params=None):
        params = {'token': self.token, "page": page, "pagesize": pagesize, "parameters[date]": base_date,
                  "parameters[date_from]": date_from, "parameters[date_to]": date_to, "parameters[tickers]"
                  :company_tickers, "parameters[importance]": importance, "parameters[date_sort]": date_sort,
                  "parameters[updated]": updated_params}
        try:
            retail_url = self.__url_call__("Calendar / Fundamentals", "calendar", "retail")
            retail = requests.get(retail_url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return retail.json()

    def ratings(self, page=None, pagesize=None, base_date=None, date_from=None, date_to=None,
                  company_tickers=None, importance=None, date_sort=None, updated_params=None, action=None):
        params = {'token': self.token, "page": page, "pagesize": pagesize, "parameters[date]": base_date,
                  "parameters[date_from]": date_from, "parameters[date_to]": date_to, "parameters[tickers]"
                  :company_tickers, "parameters[importance]": importance, "parameters[date_sort]": date_sort,
                  "parameters[updated]": updated_params, "parameters[action]": action}
        try:
            ratings_url = self.__url_call__("Calendar / Fundamentals", "calendar", "ratings")
            ratings = requests.get(ratings_url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return ratings.json()

    def conference_calls(self, page=None, pagesize=None, base_date=None, date_from=None, date_to=None,
                  company_tickers=None, importance=None, date_sort=None, updated_params=None):
        params = {'token': self.token, "page": page, "pagesize": pagesize, "parameters[date]": base_date,
                  "parameters[date_from]": date_from, "parameters[date_to]": date_to, "parameters[tickers]"
                  :company_tickers, "parameters[importance]": importance, "parameters[date_sort]": date_sort,
                  "parameters[updated]": updated_params}
        try:
            conference_url = self.__url_call__("Calendar / Fundamentals", "calendar", "conference_call")
            conference = requests.get(conference_url, headers=self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return conference.json()

    """Financial Fundamentals"""
    

    def financials(self, company_ticker=None, isin=None, cik=None, date_asof=None)
        params = {'token': self.token, "symbols": company_ticker, "isin": isin, "cik": cik, "asOf": date_asof}
        try:
            financials_url = self.__url_call__("Calendar / Fundamentals", "fundamentals", "financials")
            financials = requests.get(financials_url, headers=self.headers, params= params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return financials.json()

    def valuation_ratios(self, company_ticker, asof):
        params = {'token': self.token, "symbols": company_ticker, "asOf": asof}
        try:
            valuationsUrl = self.__url_call__("Calendar / Fundamentals", "calendar", "valuationRatios")
            valuation = requests.get(valuationsUrl, headers = self.headers, params = params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return valuation.json()

    def earning_ratios(self, company_ticker, asof):
        params = {'token': self.token, "symbols": company_ticker, "asOf": asof}
        try:
            earningsUrl = self.__url_call__("Calendar / Fundamentals", "calendar", "earningRatios")
            earnings = requests.get(earningsUrl, headers = self.headers, params= params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return earnings.json()

    def operations_ratios(self, company_ticker, asof):
        params = {'token': self.token, "symbols": company_ticker, "asOf": asof}
        try:
            operationsUrl = self.__url_call__("Calendar / Fundamentals", "calendar", "operationRatios")
            operations = requests.get(operationsUrl, headers=self.headers, params= params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return operations.json()

    """Chart"""

    def chart(self, ticker, date_range, interval):
        params = {'symbol': ticker.upper(), 'from': date_range, 'interval': interval}
        url = self.__url_call__("Chart")
        chart = requests.get(url, headers=self.headers, params=params)
        return chart.json()

    """Delayed Quotes"""

    def delayed_quote(self, company_ticker):
        params = {'token': self.token, "symbols": company_ticker}
        try:
            delayedquoteUrl = self.__url_call__("quoteDelayed", "earningRatios")
            delayedquote = requests.get(delayedquoteUrl, headers=self.headers, params=params)
        except requests.exceptions.RequestException as request_denied:
            print(request_denied)
        return delayedquote.json()

    """Output"""

    def JSON(self, func_output):
        result = json.dumps(func_output, indent= 4)
        print(result)
        return result

if __name__ == '__main__':
    token = "899efcbfda344e089b23589cbddac62b"
    false_token = 0
    company_ticker = "AAPlL"
    start_date = "2018-01-01"
    sample_run = Benzinga(token)
    div = sample_run.dividends()
    sample_run.JSON(div)






    

