import tabula
import pandas as pd
from pandas.tseries.offsets import BDay
import glob,os
import urllib.request
import numpy as np
from html_table_parser.parser import HTMLTableParser

HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
ops = pd.DataFrame()

directory = os.path.dirname("./")
ufe_df = pd.DataFrame()
dollar_df = pd.DataFrame()



def url_get_contents(url):

	# Opens a website and read its
	# binary contents (HTTP Response Body)

	#making request to the website
	req = urllib.request.Request(url=url,headers=HEADERS)
	f = urllib.request.urlopen(req)

	#reading contents of the website
	return f.read()


def get_indexed_ufe(satis_ufe,alis_ufe):
    diff=(satis_ufe-alis_ufe)/alis_ufe
    if diff >= 0.1:
        return 1+ diff
    else:
        return 1


def get_ufe(year, month):

    index = ufe_df[ufe_df['YIL'] == year].index[0]
    ufe = ufe_df.loc[index].values[int(month)]
    return ufe
def get_currency_per_op(previous_working_day):
    date =  previous_working_day.strftime('%Y-%m-%d')
    index = dollar_df[dollar_df['Tarih'] == date].index[0]
    dollar = dollar_df.loc[index,'currency']
    print(f"bulundan dolar kuru {dollar}")
    while pd.isna(dollar): 
        print(f"Tatil gunu oldugu icin onceki ilk is gunune bakiyoruz")
        index=index - 1
        dollar = dollar_df.loc[index,'currency']

    return dollar

def get_split_ratio(symbol, buy_date, sell_date ):
    split_row = splits_df[splits_df['Symbol'] == symbol]
    if not split_row.empty:
        split = split_row.iloc[0].to_dict()
        if split['Date'] > buy_date and split['Date'] < sell_date:
            return split['Split Ratio']
        else:
            return 1
    else :
        return 1

def get_dollar_history():
    excel_file = 'EVDS.xlsx'  # Replace 'example.xlsx' with the path to your Excel file
    df = pd.read_excel(excel_file)
     #changing column name to "currency"
    df.rename(columns={df.columns[1]: "currency"}, inplace=True)
    df['Tarih'] = pd.to_datetime(df['Tarih'],format='%d-%m-%Y', errors='coerce')

    df = df[df['Tarih'].notna()]
    df = df.drop(df.columns[2],axis=1)

    return df

def get_splits_history():
    split_file = 'split_2023.json'  # Replace 'example.xlsx' with the path to your Excel file
    df = pd.read_json(split_file)
    test_row = {
        "Date" : "2023-12-01  00:00:00",
        "Symbol" : "TMF",
        "Company Name": "Test Company",
        "Type" : "Reverse",
        "Split Ratio" : 0.1
    }
    print(f"df length {len(df)}")
    df.loc[len(df)] = test_row
    df['Date']=pd.to_datetime(df['Date'],format='%Y-%m-%d %H:%M:%S')
    df['Split Ratio'] = df['Split Ratio'].astype(float)

    return df

def get_ufe_history():
    #GET UFE history to a dataframe 
    #temporarilt using the link to get ufe history since json reading writing has an issue

    if not os.path.exists('TTTT'):
        ufe_html = url_get_contents('https://www.hakedis.org/endeksler/yi-ufe-yurtici-uretici-fiyat-endeksi').decode('utf-8')

        page = HTMLTableParser()
        page.feed(ufe_html)
        ufe_df=pd.DataFrame(page.tables[0])
        ufe_df.columns = ufe_df.iloc[0]
        ufe_df=ufe_df[1:]
        ufe_df.to_json("ufe_history.json",force_ascii = False)
    else:
        ufe_df = pd.read_json("ufe_history.json")
        print(ufe_df)
    return ufe_df



#GET DOLLAR History
dollar_df = get_dollar_history()
print(dollar_df)

ufe_df = get_ufe_history()
print(ufe_df)

splits_df = get_splits_history()
print(splits_df)

pdf_files = glob.glob(directory + '/*.pdf')
for pdf_file in pdf_files:
    print(pdf_file)
    dfs = tabula.read_pdf(pdf_file,pages="all",encoding='utf-8', multiple_tables=True)
    for df in dfs:
        if df.empty:
            continue
        if any("YATIRIM İŞLEMLERİ" in column for column in df.columns):
            print(df)
            df.columns=df.iloc[0]
            df=df[df['İşlem Durumu']=="Gerçekleşti"]
            if ops.empty:
                ops=df
            else:
                ops=ops._append(df)


ops['Tarih']=pd.to_datetime(ops['Tarih'],format='%d/%m/%y %H:%M:%S')
ops = ops.sort_values(by='Tarih')
ops = ops.reset_index()





ops['previous_month']= ops['Tarih'] - pd.DateOffset(months=1)
# Extract year and month as strings from the previous month
ops['previous_month_year'] = ops['previous_month'].dt.year.astype(str)
ops['previous_month_month'] = ops['previous_month'].dt.month.astype(str)

# Extract year and month as strings from the current operation date
ops['previous_working_day'] = ops['Tarih'] - BDay()
ops['current_year'] = ops['Tarih'].dt.year.astype(str)

ops['ops_time_ufe'] = ops.apply(lambda row: get_ufe(row['previous_month_year'], row['previous_month_month']), axis=1)
ops['Islem Tarihi Dolar'] = ops.apply(lambda row: get_currency_per_op(row['previous_working_day']), axis=1)

#convert necessary columns to float for calculations
ops['Gerçekleşen Adet']=ops['Gerçekleşen Adet'].str.replace(',', '.').astype(float)
ops['ops_time_ufe']=ops['ops_time_ufe'].str.replace(',', '.').astype(float)
ops['Ortalama İşlem Fiyatı']=ops['Ortalama İşlem Fiyatı'].str.replace(',', '.').astype(float)
ops['İşlem Ücreti']=ops['İşlem Ücreti'].str.replace(',', '.').astype(float)

### ENF OF UFE OPERATIONS ###

### GETTING CURRENCY OPERATION ###




print(ops)
print(dollar_df)

buy_ops = ops[ops['İşlem Tipi']=="Alış"]
buy_ops['not_calculated'] = buy_ops['Gerçekleşen Adet']
sell_ops = ops[ops['İşlem Tipi']=="Satış"]
symbols = {}
for symbol in buy_ops['Sembol'].unique():
    print(symbol)
    symbols[symbol] = { "buy_ops": buy_ops[buy_ops['Sembol']==symbol] }

for symbol in sell_ops['Sembol'].unique():
    print(symbol)
    symbols[symbol]['sell_ops'] = sell_ops[sell_ops['Sembol']==symbol] 

sell_ops_calculated = pd.DataFrame()
for symbol in sell_ops['Sembol'].unique():
    print(f"calculating tax and net revevue for {symbol}")
    for ind in symbols[symbol]['sell_ops'].index:
        sell_op = sell_ops.loc[ind].to_dict()
        remained_sell = sell_op['Gerçekleşen Adet']
        print(f"working on sell {sell_op}  date {symbol}")
        buy_ops_symbol = symbols[symbol]['buy_ops']
        print(buy_ops_symbol)
        for ind in buy_ops_symbol.index:
            remained_buy=buy_ops_symbol['not_calculated'][ind]
            if remained_buy > 0:
                split_ratio=get_split_ratio(symbol,buy_ops_symbol['Tarih'][ind],sell_op['Tarih'])
                print(f"split ratio is {split_ratio}")
                
                if remained_buy*split_ratio >= remained_sell:
                    sell_count=remained_sell
                    remained_buy = remained_buy - remained_sell/split_ratio
                    remained_sell = 0
                else:
                    sell_count=remained_buy*split_ratio
                    remained_sell = remained_sell - remained_buy*split_ratio
                    remained_buy = 0
                buy_ops_symbol.loc[ind, 'not_calculated'] = remained_buy
                sell_op['Hesaplanan Adet']=sell_count
                sell_op['Split Ratio']=split_ratio
                sell_op['Ortalama Alis Fiyatı']=buy_ops_symbol['Ortalama İşlem Fiyatı'][ind] / split_ratio
                sell_op['Alış Tarihi UFE']=buy_ops_symbol['ops_time_ufe'][ind]
                sell_op['Alış Tarihi Dolar']=buy_ops_symbol['Islem Tarihi Dolar'][ind]
                print(sell_op)
                if sell_ops_calculated.empty:
                    sell_ops_calculated = pd.DataFrame.from_records([sell_op])
                else:
                    sell_ops_calculated = pd.concat([sell_ops_calculated, pd.DataFrame.from_records([sell_op])], ignore_index=True)
                print(sell_ops_calculated)
                if remained_sell==0:
                    break
        #symbols[symbol]['buy_ops']=buy_ops_symbol



print(sell_ops_calculated)

sell_ops_calculated['Alis Toplam TL'] = sell_ops_calculated['Hesaplanan Adet'] * \
                                 sell_ops_calculated['Ortalama Alis Fiyatı'] *  \
                                 sell_ops_calculated['Alış Tarihi Dolar']
sell_ops_calculated['Ufe Endeksi'] = sell_ops_calculated.apply(lambda row: get_indexed_ufe(row['ops_time_ufe'], row['Alış Tarihi UFE']), axis=1)
sell_ops_calculated['Alis Toplam Endeksli TL'] = sell_ops_calculated['Alis Toplam TL'] * sell_ops_calculated['Ufe Endeksi']
sell_ops_calculated['Satis Toplam TL'] = sell_ops_calculated['Hesaplanan Adet'] * \
                                 sell_ops_calculated['Ortalama İşlem Fiyatı'] *  \
                                 sell_ops_calculated['Islem Tarihi Dolar']

sell_ops_calculated['Vergiye Tabi Kazanc'] = sell_ops_calculated['Satis Toplam TL'] - sell_ops_calculated['Alis Toplam Endeksli TL']

print(sell_ops_calculated)

print(sell_ops_calculated.groupby('Sembol')['Vergiye Tabi Kazanc'].sum())

sell_ops_calculated.to_html("sonuc.html",index=False)
sell_ops_calculated.to_excel("sonuc.xlsx",index=False)