import requests


def get_waether_condition(city):
    # api key from openweathermap.org
    API_key = 'eb98e74c4e57783dd86a301a689acaa5'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    # reuest from the api the data sampled in json
    req = requests.get(url)
    data = req.json()
    # getting data (city and its longitude and latitude) from the request to use it into another api for getting the temprature and its skyConditions
    name = data['name']
    lon = data['coord']['lon']
    lat = data['coord']['lat']
    # We have now the city name and its longitude and latitude
    # we dont nead hour and minute in this condition so we exclude them
    exclude = 'minute,hourly'

    # Using one call api to get the 8 days forecast
    url2 = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={exclude}&appid={API_key}'
    req2 = requests.get(url2)
    data2 = req2.json()

    # lists of the tempratures of day\night and its sky decription for each city
    days = []
    nights = []
    descr = []
    Day_data = []
    for i in data2['daily']:
        # As the given data from the api isin kelvin and celsius = kelvin - 273.15
        days.append(round(i['temp']['day']-273.15, 2))
        # Rounding the output to 2 decimal points to be more readable
        nights.append(round(i['temp']['night']-273.15, 2))
        descr.append(i['weather'][0]['main']+': ' +
                     i['weather'][0]['description'])

    # now we have the city name and its temprature,sky condition ,description for 8 days
    # formating the output to make the tts more accurate
    phrase = f'{city} - forecast\n'

    for j in range(len(days)):
        if j == 0:
            phrase += f'\nDay {j+1} (Today)\n'
        elif j == 1:
            phrase += f'\nDay {j+1} (Tomorrow)\n'
        else:
            phrase += f'\nDay {j+1}\n'

        phrase += 'Day temprature is ' + str(days[j]) + '°C\n'
        phrase += 'Night temprature is ' + str(nights[j]) + '°C\n'
        phrase += 'Sky Condition is ' + str(descr[j]) + '\n'
        Day_data.insert(j,phrase)
        phrase = ""

    return Day_data


