import streamlit as st
import os
import shutil
from sec_edgar_downloader import Downloader
from k10parser import tenkparser
from filings import Filings
import pandas as pd
from llm import Llminsights

tenkparserobj =  tenkparser()
llmcaller = Llminsights()

def download10K(ticker):

    shutil.rmtree('sec-edgar-filings')
    dl = Downloader("MyCompanyName", "my.email@domain.com")
    dl.get(ticker_or_cik=ticker,form='10-K',after='2014-01-01',before='2024-01-01',download_details=True)
    

def find_html_files(folder_path='Data'):
        html_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.join(root, file))
        print(html_files)
        return html_files


folder_path = 'Data'

filingobj = Filings()


# Streamlit UI code
st.title('10-K Analyzer')

ticker = st.text_input("Enter Company's Ticker")

if ticker:
    try:
        shutil.rmtree(folder_path)
    except:
        os.makedirs(folder_path)

    try:
        os.makedirs(folder_path)
    except:
        st.write('cant make data directory')

    filingobj.initialise(ticker)
    html_files = find_html_files(folder_path) 
    st.write(f"{len(html_files)} 10-K filings downloaded ")

    llmcaller.cash_flow = filingobj.consolidated_cf.to_markdown(tablefmt='pipe', colalign=['center']*len(filingobj.consolidated_cf.columns))
    llmcaller.balance_sheet = filingobj.consolidated_bs.to_markdown(tablefmt='pipe', colalign=['center']*len(filingobj.consolidated_bs.columns))
    llmcaller.income_statement = filingobj.consolidated_ic.to_markdown(tablefmt='pipe', colalign=['center']*len(filingobj.consolidated_ic.columns))
    llmcaller.company = filingobj.company

    col1, col2 = st.columns(2)

    with col1:
        income_statement = st.button("Display Income Statements")

    with col2:
        cash_flow = st.button("Display Cash Flow Statements")

    col3, col4 = st.columns(2)

    with col3:
        balance_sheet = st.button("Display Balance Sheets")

    with col4:
        generate_insights = st.button('Click For AI Generated Insights')



    if income_statement:
        
        st.dataframe(filingobj.consolidated_ic)
        for label in filingobj.consolidated_ic.index:  # Iterate over labels
            st.subheader(f"{label}")
            st.bar_chart(filingobj.consolidated_ic.loc[label])  # Plot bar chart for each label

    if cash_flow:
        st.dataframe(filingobj.consolidated_cf)
        for label in filingobj.consolidated_cf.index:  # Iterate over labels
            st.subheader(f"{label}")
            st.bar_chart(filingobj.consolidated_cf.loc[label])  # Plot bar chart for each label

    if balance_sheet:
        st.dataframe(filingobj.consolidated_bs)
        for label in filingobj.consolidated_bs.index:  # Iterate over labels
            st.subheader(f"{label}")
            st.bar_chart(filingobj.consolidated_bs.loc[label])  # Plot bar chart for each label

    if generate_insights:
        st.write(llmcaller.makecall(),unsafe_allow_html=True)

    file_to_analyze = st.selectbox("Which file do you want to see", html_files, index=None, placeholder="Select file")

    try:
        tenkparserobj.parse10K(file_to_analyze) 
        items = tenkparserobj.getitems() 
    except:
        pass

    try:
        section_to_display = st.selectbox("Which section do you want to see", items, index=None, placeholder="Select section")
    except:
        section_to_display = ''

    if section_to_display:
        try:
            result = tenkparserobj.getsegmenthtml(section_to_display) # Get HTML segment for selected section
            st.write(result, unsafe_allow_html=True) # Display HTML segment
        except Exception as e:
            st.write('Error:', e)

    






