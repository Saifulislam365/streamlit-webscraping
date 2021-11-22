import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

st.title('APLIKASI S&P 500 ')

st.markdown("""
S&P 500 adalah sebuah indeks yang terdiri dari saham 500 perusahaan terbesar dari berbagai sektor yang terdaftar di bursa saham Amerika Serikat.
Aplikasi ini mengambil daftar **S&P 500** (dari Wikipedia) dan **Harga Penutupan Saham** yang sesuai (tahun-ke-tanggal)!
* **libray Python:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Sumber Data:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
* **Sumber Belajar:** [Youtube](https://www.youtube.com/watch?v=ZZ4B0QUHuNc&list=PLtqF5YXg7GLmCvTswG32NqQypOuYkPRUE).
""")

st.sidebar.header('Fitur Masukan Pengguna')

# Web scraping of S&P 500 data
#
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['GICS Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

st.header('Tampilkan Perusahaan di Sektor Terpilih')
st.write('Dimensi Data: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/

data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol
def price_plot(symbol):
  df = pd.DataFrame(data[symbol].Close)
  df['Date'] = df.index
  plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
  plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  st.set_option('deprecation.showPyplotGlobalUse', False)
  return st.pyplot()

num_company = st.sidebar.slider('Jumlah Perusahaan', 1, 5)

if st.button('Gambar Grafik'):
    st.header('Harga Penutupan Saham')
    for i in list(df_selected_sector.Symbol)[:num_company]:
        price_plot(i)
