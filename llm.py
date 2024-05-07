from openai import OpenAI
from dotenv import dotenv_values





class Llminsights:
    
    def __init__(self):        
        config = dotenv_values(".env")
        self.client = OpenAI(api_key=config['APIKEY'])
        self.balance_sheet = ''
        self.income_statement = ''
        self.cash_flow = ''
        self.company = ''
        
    
    def makecall(self):
        
        prompt = f" CASH FLOW STATEMENT \n {self.cash_flow} \n INCOME STATEMENT \n {self.income_statement} \n BALANCE SHEET \n {self.balance_sheet} \n Company : {self.company} \n Generate insights for the above using the following format STRICTLY:\n General Insights TEN LINES ONLY:\n Calculate IMPORTANT Ratios for all the years in one table only followed by a few lines of your insight:\n Risk Rating on a scale of 1-10 for an investor JUST A NUMBER :"
        


        completion = self.client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "user", "content": prompt}
          ],
          temperature=1,
          max_tokens=1500,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

        prompt2body = completion.choices[0].message
        prompt2 = f"Generate the following as html ACCURATELY: \n {prompt2body}"
        
        completion = self.client.chat.completions.create(
          model="gpt-3.5-turbo",
          messages=[
            {"role": "user", "content": prompt2}
          ],
          temperature=1,
          max_tokens=4000,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

        result = completion.choices[0].message.content

        return result
