#import datasets for analysis

import pandas as pd
from fredapi import Fred
import requests

def load_tuition():
    return pd.read_excel("data/tuition.xlsx")

def load_loan_debt(api_key):
    fred = Fred(api_key=api_key)
    debt = fred.get_series('SLOAS').to_frame(name='Student_Loan_Debt')
    debt.index = debt.index.year
    return debt.groupby(debt.index).mean().reset_index().rename(columns={'index':'Year'})

def load_income(api_key):
    url = f"https://api.census.gov/data/2022/acs/acs1?get=NAME,B19013_001E&for=us:*&key={api_key}"
    response = requests.get(url).json()
    df = pd.DataFrame(response[1:], columns=['Name','Median_Income','us'])
    df['Median_Income'] = df['Median_Income'].astype(int)
    df['Year'] = 2022
    return df
