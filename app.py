import streamlit as st
import os
from sec_edgar_downloader import Downloader
from k10parser import tenkparser


tenkparserobj =  tenkparser()


def download10K(ticker):
    
    dl = Downloader("MyCompanyName", "my.email@domain.com")
    dl.get(ticker_or_cik=ticker,form='10-K',after='2014-01-01',before='2024-01-01',download_details=True)

def find_html_files(folder_path):
        html_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        return html_files


folder_path = 'sec-edgar-filings'

st.title('10-K analyzer')

ticker = st.text_input("Enter Company's Ticker")
items = []
download = st.button('Download 10K')
downloaded = False

if download and ticker:

    download10K(ticker)

    downloaded = True

    html_files = find_html_files(folder_path)
    
    st.write(f"{len(html_files)} 10-K filings downloaded from 2014 onwards")


html_files = find_html_files(folder_path)

file_to_analyze = st.selectbox("Which file do you want to see", html_files, index=None, placeholder="Select file")

tenkparserobj.parse10K(file_to_analyze)
items = tenkparserobj.getitems()


section_to_display = st.selectbox("which section do you want to see",
                                  items,
                                  index=None, placeholder="Select section")

try:
    result = tenkparserobj.getsegmenthtml(section_to_display)
    st.write(result,unsafe_allow_html=True)
except:
    st.write('choose file and section')





