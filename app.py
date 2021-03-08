from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests
import numpy

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')
temp = [] #initiating a tuple

for i in range(0, len(tr)):
#insert the scrapping process here
    if(i == 12) :
        continue
        
    if(i == 36):
        continue
    
    row = table.find_all('tr')[i]
 
    #get date
    tanggal = row.find_all('td')[0].text
    tanggal = tanggal.strip()
    #get currency
    harga_harian = row.find_all('td')[2].text
    harga_harian = harga_harian.strip()
    
    #get 
    temp.append((harga_harian,tanggal))

temp = temp[::-1]

# print(temp)	

#change into dataframe
df = pd.DataFrame(temp, columns = ('harga_harian','tanggal'))

#insert data wrangling here
df['harga_harian'] = df['harga_harian'].str.replace(' IDR','')

df['harga_harian'] = df['harga_harian'].str.replace(',','')

df['harga_harian'] = df['harga_harian'].astype('float64')

df['tanggal'] = df['tanggal'].astype('datetime64')
df.head()
#end of data wranggling 

@app.route("/")
def index(): 
	# counter = 0
	card_data = f'{df["harga_harian"].mean().round(2)} IDR'

	# generate plot
	x = df['tanggal']
	y = df['harga_harian']

	plt.clf()
	plt.plot(x, y, marker='.', linestyle='-',color='b', label=df['harga_harian'].describe().round(2))  
	plt.xlabel('Period')
	plt.ylabel('Currency') 
	plt.legend( prop={'size': 7.5})
	plt.title('Indonesian Rupiahs (IDR) per US Dollar (USD)') 
	
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
