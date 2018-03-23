import eikon as ek
from datetime import date
import re
import lxml.html
import pandas as pd
import win32com.client

outlook = win32com.client.Dispatch("Outlook.Application")
mail = outlook.CreateItem(0)
ek.set_app_id('<Eikon_token_id>')

#start_date, end_date = date(2017, 10, 22), date.today()
start_date, end_date = date(2017, 10, 1), date(2017, 12, 14)
q = "Product:IFRC AND Topic:ISU AND (\"PRICED\" OR \"DEAL\")"
headlines = ek.get_news_headlines(query=q, date_from=start_date, date_to=end_date, count=100)
headlines = headlines[headlines['storyId'].str.contains('nIFR')]
headlines.to_csv('test.csv')

def termsheet_to_dict(storyId):
    x = ek.get_news_story(storyId)
    story = lxml.html.document_fromstring(x).text_content()
    matches = dict(re.findall(pattern=r"\[(.*?)\]:\s?([A-Z,a-z,0-9,\-,\(,\),\+,/,\n,\r,\.,%,\&,>, ]+)", string=story))
    clean_matches = {key.strip(): item.strip() for key, item in matches.items()}
    return clean_matches

result = []

index = pd.DataFrame(headlines, columns=['storyId']).values.tolist()

for i, storyId in enumerate(index):
    x = termsheet_to_dict(storyId[0])
    if x:
        result.append(x)

df = pd.DataFrame(result)

df = df.loc[df['Country'] == 'UNITED STATES']
df = df.loc[df['Issuer/Borrower Type'] == 'Corporate']

df = df[['Issuer Long Name', '1st Pay', 'Asset Type', 'CUSIP/ISIN', 'Tenor/Mty', 'Pricing Date', 'Sector', 'Size', 'Status',
         'Yield','Ratings','Issuer/Borrower Type','Format','Coupon', 'Region']]

body = df.to_html()
dater = end_date.strftime("%m%d%Y")
print(dater)
subject = "NEW ISSUES"
print(body)

mail.To = <Insert Email Address>
mail.Subject = subject
mail.HTMLBody = body
mail.Send()
