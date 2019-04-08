import pandas as pd
import xlrd

data_xls = pd.read_excel('csvFiles/data.xlsx', 'Data', index_col=None)
data_xls.to_csv('data-real.csv', encoding='utf-8', index=False)