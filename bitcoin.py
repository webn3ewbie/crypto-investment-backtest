import streamlit as st
import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta
cg = CoinGeckoAPI()
st.set_page_config(
layout="wide"
)
st.title('Crypto Investment Calculator')
st.write("""Eyeryone Enjoys a Good What if Scenario! Choose a Date You Wish You Bought Ethereum or Bitcoin
          Want to learn more?
        - Check out the repo [Here](https://github.com/webn3ewbie/defiterm)
        - Connect with me on [LinkedIn](https://www.linkedin.com/in/joseph-biancamano/)
        - Ask a question in the Streamlit community [forums](https://discuss.streamlit.io)
         """)
st.write('---')
st.write('## Choose Date and Amount')
today = datetime.utcnow().date()
previous_day = today - timedelta(days=1)
HIST_DATE = st.date_input("Date: ", value=previous_day, min_value=datetime(2012,1,1), max_value=previous_day)
ORG_USD = st.number_input("USD Amount: ", min_value=1, max_value=999999999)
eth_current = cg.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd']
st.write('''# Ethereum Calculator''')
#Reformat Historical Date for next function
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")
eth_historic = cg.get_coin_history_by_id(id='ethereum', vs_currencies='usd', date=HIST_DATE_REFORMAT)['market_data']['current_price']['usd']
eth_historic = round(eth_historic, 5)
col1, col2 = st.columns(2)
with col1:
    st.write( '#### If You Invested On', HIST_DATE)
    st.write("You would have originally bought: ***{:,.2f}*** Ethereum".format(round((ORG_USD/eth_historic),5)))
    st.write("At a price of  $***{:,.9f}*** per Ethereum".format(eth_historic))
    st.write(" ")
with col2:
    total_eth = ORG_USD/eth_historic
    current_USD = total_eth * eth_current
    perc_change = (current_USD - ORG_USD)/(ORG_USD)*100
    usd_diff = current_USD - ORG_USD
    st.write('''## Current Values''')
    st.write("Your Initial Investment is Currently Worth: ***${:,.2f}***".format(round(current_USD,2)))
    st.write("Which is a percentage change of ***{:,.2f}%***".format(round(perc_change, 2),))
if usd_diff == 0:
   st.write('''## You Broke Even''')
elif usd_diff <= 0:
   st.write('''# You Would Have Lost''')
else:
   st.write('''## You Could have Made''') 
st.subheader('***${:,.2f}***'.format(abs(round(usd_diff,2)),))

now = datetime.now()
historical_prices = cg.get_coin_market_chart_range_by_id(id='ethereum', vs_currency="usd", from_timestamp=HIST_DATE_datetime.timestamp(), to_timestamp=now.timestamp())['prices']
dates = []
prices = []

for x,y in historical_prices:
  dates.append(x)
  prices.append(y)

dictionary = {"Prices":prices, "Dates":dates}
df = pd.DataFrame(dictionary)
df['Dates'] = pd.to_datetime(df['Dates'],unit='ms',origin='unix')
 
st.line_chart(df.rename(columns={"Dates":"index"}).set_index("index"))

#Reformat Historical Date for next function
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")
bitcoin_historic = cg.get_coin_history_by_id(id='bitcoin', vs_currencies='usd', date=HIST_DATE_REFORMAT)['market_data']['current_price']['usd']
bitcoin_historic = round(bitcoin_historic, 5)
bitcoin_current = cg.get_price(ids='bitcoin', vs_currencies='usd')['bitcoin']['usd']
st.write('''# Bitcoin Calculator''')
col1, col2 = st.columns(2)
with col1:
    st.write( '#### If You Invested On', HIST_DATE)
    st.write("You would have originally bought: ***{:,.2f}*** Bitcoin".format(round((ORG_USD/bitcoin_historic),5)))
    st.write("At a price $***{:,.9f}*** per Bitcoin".format(bitcoin_historic))
    st.write(" ")
with col2:
    total_bitcoin = ORG_USD/bitcoin_historic
    current_USD = total_bitcoin * bitcoin_current
    perc_change = (current_USD - ORG_USD)/(ORG_USD)*100
    usd_diff = current_USD - ORG_USD
    st.write('## Current Values')
    st.write("Your Initial Investment is Currently Worth: ***${:,.2f}***".format(round(current_USD,2)))
    st.write("Which is a percentage change of ***{:,.2f}%***".format(round(perc_change, 2),))

if usd_diff == 0:
   st.write('''# You Broke Even''')
elif usd_diff <= 0:
   st.write('''# You Would Have Lost''')
else:
   st.write('''## You Could Have Made''') 
st.subheader('***${:,.2f}***'.format(abs(round(usd_diff,2)),))

now = datetime.now()
historical_prices = cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency="usd", from_timestamp=HIST_DATE_datetime.timestamp(), to_timestamp=now.timestamp())['prices']
dates = []
prices = []

for x,y in historical_prices:
  dates.append(x)
  prices.append(y)

dictionary = {"Prices":prices, "Dates":dates}
df = pd.DataFrame(dictionary)
df['Dates'] = pd.to_datetime(df['Dates'],unit='ms',origin='unix')
st.line_chart(df.rename(columns={"Dates":"index"}).set_index("index"))
st.write("Please note this app is not financial advise!")
