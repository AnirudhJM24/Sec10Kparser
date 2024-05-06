from sec_edgar_downloader import Downloader
import time
import os


path_to_save = "10Kdata"

def download10K(ticker):

    dl.get(ticker_or_cik=ticker,form='10-K',after='2014-01-01',before='2024-01-01',download_details=True)


if __name__ == "__main__":


    dl = Downloader("MyCompanyName", "my.email@domain.com",path_to_save)
    ticker = input("Enter Company's Ticker")
    download10K(ticker)