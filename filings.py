from edgar.core import set_identity
import pandas as pd
from edgar._filings import get_filings
from edgar.entities import (Company,
                            CompanyData,
                            CompanyFacts,
                            CompanySearchResults,
                            CompanyFilings,
                            CompanyFiling,
                            Entity,
                            EntityData,
                            find_company,
                            get_entity,
                            get_company_facts,
                            get_company_tickers,
                            get_entity_submissions,
                            get_ticker_to_cik_lookup,
                            get_cik_lookup_data)

class Filings:

    
    def __init__(self,ticker='ABNB'):

        set_identity("Michael Mccallum mike.mccalum@indigo.com")
        self.filings,self.filing_to_html,self.company = [],{},''
        self.income_statement, self.cash_flow, self.balance_sheet = [],[],[]
        self.consolidated_ic, self.consolidated_cf,self.consolidated_bs = pd.DataFrame(),pd.DataFrame(),pd.DataFrame()

    def initialise(self,ticker):
        self.filings,self.filing_to_html,self.company = self.download10k(ticker)
        self.income_statement, self.cash_flow, self.balance_sheet = self.getfinancials()
        self.consolidated_ic, self.consolidated_cf,self.consolidated_bs = self.consolidatedfinancials(self.income_statement),self.consolidatedfinancials(self.cash_flow),self.consolidatedfinancials(self.balance_sheet)

    def download10k(self,ticker,period=30):

        
        filings = Company(ticker).get_filings(form="10-K").latest(period)
        tenkobjs =[]
        filing_to_html = {}
        company = ''
        for filing in filings:
            tenkobjs.append(filing.obj())
            filename = 'Data/'+str(filing.company) + 'X' + str(filing.filing_date) + '.html'
            filing_to_html[filename.replace('/','//')] = filing
            with open(filename,'w') as f:
                try:
                    f.write(filing.html())
                except:
                    pass
            company = filing.company

        return filings,filing_to_html,company    

    def getfinancials(self):

        income_statement, cash_flow, balance_sheet = [],[],[]
        for filing in self.filings:
            filingTenK = filing.obj()
            try:
                income_statement.append(filingTenK.income_statement.to_dataframe())
            except:
                pass
            try:
                cash_flow.append(filingTenK.cash_flow_statement.to_dataframe())
            except:
                pass
            try:
                print(filingTenK.balance_sheet)
                balance_sheet.append(filingTenK.balance_sheet.to_dataframe())
            except:
                pass

        return income_statement,cash_flow,balance_sheet
    
    def intcnv(self,num):
        try:
            if len(num)>6:
                return int(num[:-6])             
            elif  '.' in num:
                return float(num)
            else:
                return num
        except:
            return 0
        
    def consolidatedfinancials(self,fc):

        df = pd.DataFrame()
        for dataf in fc:
            dataf.reset_index(drop=True,inplace=True)
            df = pd.concat([df,dataf],axis=1)
        df = df.dropna()
        df = df.loc[:,~df.columns.duplicated()].copy()
        df.reset_index(drop=True, inplace=True)
        df.set_index('Label',inplace=True)
        #data.set_index('Label', inplace=True)
        df.index = df.index.str.replace("'", "")
        for column in df.columns:
            df[column] = df[column].apply(lambda x : self.intcnv(x))

        return df

            