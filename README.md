## Introduction

**Tech Stack Used:** Python and Streamlit for easy visualization and rapid prototyping

**Libraries Used** 
1. https://github.com/alphanome-ai/sec-parser - built upon their library and 10QParser to create my 10K Html Parser
2. https://github.com/dgunning/edgartools - Used this libray to download sec filings and extract XBRL data

**Factors Considered for Drawing Insights:**
1. **Financial Statements:** Including cash flow statements, income statements, and balance sheets. These provide a comprehensive understanding of a company's financial health, performance, and stability over time. They offer insights into revenue, expenses, profitability, liquidity, and overall financial position.

2. **Company Information:** Name and Sector. Incorporating company-specific details is crucial for contextualizing the financial data, identifying trends and patterns unique to particular industries or companies, and facilitating informed analysis and decision-making. Additionally, this information enables comparisons with industry peers or competitors, aiding benchmarking and strategic planning.

**Insights Drawn:**
1. General insights about the performance over the past 30 years for the company.
2. Ratios exemplifying the performance and status of the company, accompanied by relevant insights.
3. A risk rating for an investor on a scale of 1-10.

**App can be found here** - https://10kanalyzer.streamlit.app/

## How to Use the App and Its Features

**Landing Page :** Enter The Company Ticker to download the 10K filings for the past 30 years
![landing page](Images\landing page.png)

**Once downloaded you can view different 10K files and their sections:** 
![sections](Images\datadownloaded.png)
![section data](Images\searchforfileanditem.png)
![section data](Images\itemdisplayed.png)

**View Financial Statements Visualisation:**
![Visualisation](Images\incomestatements.png)

**AI generated Insights using GPT 3.5 :**
![Ai gen](Images\aigeneratedresult.png)
![Ai gen](Images\gatech2.png)

