from pandas_datareader import data as pdr

import fix_yahoo_finance as yf
yf.pdr_override()  # <== that's all it takes :-)

# download dataframe
company = "AAPL"
data = pdr.get_data_yahoo(company, start="2017-10-01", end="2018-10-01")
print(data)