from urllib.request import urlopen
import requests
import pandas as pd
from datetime import datetime
import pymysql
import sys
from sqlalchemy import create_engine
import os
import xlrd

access_token = '<insert user password>'
user_id = '<insert user id>'
schema = '<insert schema>'

conn = pymysql.connect(host='localhost', port=3306, user=user_id, passwd=access_token, db=schema)

def SPDR_scrape(etf_ticker, bond_class, url):

    SPDR_url = requests.get(url)
    with open('SPDR_temp.xls', 'wb') as output:
        output.write(SPDR_url.content)

    book = xlrd.open_workbook("C:\\Users\\tlack\Documents\\Python Scripts\\Machine Learning\\SPDR_temp.xls")
    sheet = book.sheet_by_index(0)
    dater = str(sheet.cell_value(rowx=2, colx=1))[7:]
    SPDR_date = datetime.strptime(dater, '%m/%d/%Y').strftime('%Y-%m-%d')
    funder = str(sheet.cell_value(rowx=1, colx=1))

    holdings_df = pd.read_excel('SPDR_temp.xls', header=3, encoding='utf8')
    holdings_df.dropna(subset=['Identifier', 'Maturity'], how='any', inplace=True)
    holdings_df = holdings_df.loc[holdings_df['Maturity'] != '0/0/2000']
    holdings_df = holdings_df.loc[~holdings_df['Name'].str.contains('STATE ST INST')].reset_index(drop=True)
    holdings_df['Maturity'] = pd.to_datetime(holdings_df['Maturity'])
    #holdings_df['Maturity'] = pd.to_datetime(holdings_df['Maturity']).apply(lambda x: x.strftime('%Y-%m-%d') if not pd.isnull(x) else '')
    #holdings_df['Maturity'] = holdings_df['Maturity'].apply(lambda x: x.strftime('%Y-%m-%d') if not pd.isnull(x) else '')
    holdings_df['Holdings_Date'] = SPDR_date
    holdings_df['Fund'] = funder
    holdings_df['Cusip'] = holdings_df['Identifier'].str[2:11]
    holdings_df['Asset_Class'] = bond_class

    Holdings_Date = holdings_df['Holdings_Date'].tolist()
    ISIN = holdings_df['Identifier'].tolist()
    FUND_ID = holdings_df['Fund'].tolist()
    Asset_Class = holdings_df['Asset_Class'].tolist()
    Weight = holdings_df['Weight'].tolist()
    Market_Value = holdings_df['Market Value'].tolist()
    Coupon = holdings_df['Coupon'].tolist()
    Maturity = holdings_df['Maturity'].tolist()
    Cusip = holdings_df['Cusip'].tolist()

    length = len(ISIN)

    try:
        db = pymysql.connect(
            host='localhost',
            user=user_id,
            passwd=access_token,
            db=schema
        )

    except Exception as e:
        print('MySQL server is not running')
        sys.exit('cant connect')

    cursor = db.cursor()

    values = "REPLACE INTO spdr_holdings (Holdings_Date, ISIN, FUND_ID, Asset_Class, Weight, Market_Value, Coupon, Maturity, Cusip) \
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    params = [(str(Holdings_Date[i]), str(ISIN[i]), str(FUND_ID[i]), str(Asset_Class[i]), str(Weight[i]),
               str(Market_Value[i]), str(Coupon[i]), str(Maturity[i]),
               str(Cusip[i])) for i in range(length)]

    cursor.executemany(values, params)
    db.commit()

    print('###HOLDINGS DATE###')
    print(dater)
    print('###FUND TICKER###')
    print(etf_ticker)

SPDR_scrape('JNK', 'HY', 'https://us.spdrs.com/site-content/xls/JNK_All_Holdings.xls?fund=JNK&docname=All+Holdings&onyx_code1=&onyx_code2=')
SPDR_scrape('CJNK', 'BORDER', 'https://us.spdrs.com/site-content/xls/CJNK_All_Holdings.xls?fund=CJNK&docname=All+Holdings&onyx_code1=&onyx_code2=')
SPDR_scrape('SJNK', 'HY', 'https://us.spdrs.com/site-content/xls/SJNK_All_Holdings.xls?fund=SJNK&docname=All+Holdings&onyx_code1=&onyx_code2=')
SPDR_scrape('FLRN', 'IG', 'https://us.spdrs.com/site-content/xls/FLRN_All_Holdings.xls?fund=FLRN&docname=All+Holdings&onyx_code1=&onyx_code2=')
