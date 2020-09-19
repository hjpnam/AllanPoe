import pandas as pd
import os
from datetime import datetime
import pathlib


class renamer():
  def __init__(self):
    self.colDict = dict()
  def __call__(self, x):
    if x not in self.colDict:
      self.colDict[x] = 0
      return x
    else:
      self.colDict[x] += 1
      return f'{x}_{self.colDict[x]}'

dt_string = datetime.now().strftime("%d%m%Y_%H%M%S")

def cleanReport(cik): 
  path = fr'reports/{cik}/'
  excelFiles = [file for file in os.listdir(path) if file.endswith('.xlsx')]
  cols = list(range(2))
  pathlib.Path(fr'./csv/{cik}').mkdir(parents=True, exist_ok=True)

  # create one dataframe with first file to append the rest of the files
  xls = pd.ExcelFile(path + excelFiles[0])
  sheet1df = pd.read_excel(xls, sheet_name=1, header=None, usecols=cols)
  sheet1df = sheet1df.drop([0])  # drop useless table name and "3 months end"
  sheet1df[0][1] = 'Date'  # label the quarter end date as Date
  sheet1df = sheet1df.T  # Transpose the dataframe
  sheet1df.columns = sheet1df.iloc[0]  # Set column headers
  sheet1df = sheet1df.drop([0])  # Remove row of labels now that it's been used as header
  sheet1df = sheet1df.rename(columns=renamer())

  # append the rest of the files to data frame extracted from first file
  other_dfs = []

  for doc in excelFiles[1:]:
    sheet1df2 = pd.read_excel(path + doc, sheet_name=1, header=None, usecols=cols)
    sheet1df2 = sheet1df2.drop([0]) 
    sheet1df2[0][1] = 'Date' 
    sheet1df2 = sheet1df2.T  
    sheet1df2.columns = sheet1df2.iloc[0] 
    sheet1df2 = sheet1df2.drop([0]) 
    sheet1df2 = sheet1df2.rename(columns=renamer())
    print(doc)
    other_dfs.append(sheet1df2)

  sheet1df = sheet1df.append(other_dfs, ignore_index=True, sort=False)
  sheet1df['Date'] = pd.to_datetime(sheet1df['Date'])
  sheet1df = sheet1df.sort_values(by=['Date'])

  sheet1df.to_csv(fr'csv/{cik}/combined_sheet1_{dt_string}.csv')

  sheet2df = pd.read_excel(xls, sheet_name=2, header=None, usecols=cols)
  sheet2df = sheet2df.drop([0])  # drop useless table name and "3 months end"
  sheet2df[0][1] = 'Date'  # label the quarter end date as Date
  sheet2df = sheet2df.T  # Transpose the dataframe
  sheet2df.columns = sheet2df.iloc[0]  # Set column headers
  sheet2df = sheet2df.drop([0])  # Remove row of labels now that it's been used as header
  sheet2df = sheet2df.rename(columns=renamer())

  # append the rest of the files to data frame extracted from first file
  other_dfs = []

  for doc in excelFiles[1:]:
    sheet2df2 = pd.read_excel(path + doc, sheet_name=2, header=None, usecols=cols)
    sheet2df2 = sheet2df2.drop([0]) 
    sheet2df2[0][1] = 'Date' 
    sheet2df2 = sheet2df2.T  
    sheet2df2.columns = sheet2df2.iloc[0] 
    sheet2df2 = sheet2df2.drop([0]) 
    sheet2df2 = sheet2df2.rename(columns=renamer())
    print(doc)
    other_dfs.append(sheet2df2)

  sheet2df = sheet2df.append(other_dfs, ignore_index=True, sort=False)
  sheet2df['Date'] = pd.to_datetime(sheet2df['Date'])
  sheet2df = sheet2df.sort_values(by=['Date'])

  sheet2df.to_csv(fr'csv/{cik}/combined_sheet2_{dt_string}.csv')
'''
  balanceSheetdf = None
  try:
    balanceSheetdf = pd.read_excel(xls, sheet_name='CONDENSED CONSOLIDATED BALANCE ', header=None, usecols=cols)
  except:
    balanceSheetdf = pd.read_excel(xls, sheet_name='Consolidated_Balance_Sheets', header=None, usecols=cols)
  balanceSheetdf[0][1] = 'Date'
  balanceSheetdf = balanceSheetdf.T
  balanceSheetdf.columns = balanceSheetdf.iloc[0]
  balanceSheetdf = balanceSheetdf.drop([0])
  balanceSheetdf = balanceSheetdf.rename(columns=renamer())

  other_dfs = []

  for doc in excelFiles[1:]:
    balanceSheetdf2 = None
    try:
      balanceSheetdf2 = pd.read_excel(path + doc, sheet_name='CONDENSED CONSOLIDATED BALANCE ', header=None, usecols=cols)
    except:
      balanceSheetdf2 = pd.read_excel(xls, sheet_name='Consolidated_Balance_Sheets', header=None, usecols=cols)
    balanceSheetdf2[0][1] = 'Date' 
    balanceSheetdf2 = balanceSheetdf2.T  
    balanceSheetdf2.columns = balanceSheetdf2.iloc[0] 
    balanceSheetdf2 = balanceSheetdf2.drop([0]) 
    balanceSheetdf2 = balanceSheetdf2.rename(columns=renamer())
    other_dfs.append(balanceSheetdf2)
  
  balanceSheetdf = balanceSheetdf.append(other_dfs, ignore_index=True, sort=False)
  balanceSheetdf['Date'] = pd.to_datetime(balanceSheetdf['Date'])
  balanceSheetdf = balanceSheetdf.sort_values(by=['Date'])

  balanceSheetdf.to_csv(fr'csv/{cik}/combined_balancesheet_{dt_string}.csv')
'''

def mergeCSVs(cik):
  path = fr'csv/{cik}/'
  csvFiles = [file for file in os.listdir(path) if file.endswith('.csv')]
  writer = pd.ExcelWriter(fr'csv/{cik}/combined_{dt_string}.xlsx')

  for f in csvFiles:
    df = pd.read_csv(path + f)
    df.to_excel(writer, sheet_name=os.path.splitext(os.path.basename(f))[0], index=False)
    os.remove(path + f)
  
  writer.save()

cleanReport('0000320193')
mergeCSVs('0000320193')