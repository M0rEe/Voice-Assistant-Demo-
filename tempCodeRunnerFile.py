
url='https://www.google.com/search=?q' + 'weather' + city
html_req = requests.get(url)
soup= BeautifulSoup(html_req,'html.parser')
temprature = soup.find('div',attrs={'class':'BNeawe iBp4i AP7wnd'}).text
sky_state  = soup.find('div',attrs={'class':'BNeawe tAd8D AP7wnd'}).text
data       = sky_state.split('\n')
time = data[0]
sky  = data[1]


list_div = soup.find('div',attrs={'class':'BNeawe s3v8rd AP7wnd'}).text
listtxt = list_div[5].text
wind = listtxt.find('wind')
otherdata = listtxt[wind:]

print('temprature is '+ temprature)
print('time is '+ time)
print('sky descrition is '+ sky)
print(otherdata)

