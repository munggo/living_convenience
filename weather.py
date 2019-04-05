 #-*- coding: utf-8 -*-

from urllib.parse import urlencode
from urllib.request import urlopen
import bs4


def get_weather(city):
    city = urlencode({'weasearchstr': city})
    url = "http://weather.service.msn.com/data.aspx?culture=ko-KR&weadegreetype=C&src=outlook&%s" % (city)

    with urlopen(url) as response:
        msn_data = response.read()
        res = bs4.BeautifulSoup(msn_data, 'html.parser')

        temperature = res.current.get('temperature') # 현재 온도
        feelslike = res.current.get('feelslike') # 체감 온도
        skytext = res.current.get('skytext') # 스카이코드
        humidity = res.current.get('humidity') # 습도
        wind = res.current.get('winddisplay') # 바람
        day = res.current.get('day')
        observationpoint = res.current.get('observationpoint')

        today = res.find_all('forecast')[1]
        tm = res.find_all('forecast')[2]

        res = "`%s`\n[현재] %s %s°С(체감 %s°С), 습도 %s%%, 바람 %s" % \
            (city, skytext, temperature, feelslike, humidity, wind)

        res = res + "\n[오늘] 최고 %s°С, 최저 %s°С, %s" % (today.get('high'), today.get('low'), today.get('skytextday'))
        res = res + "\n[내일] 최고 %s°С, 최저 %s°С, %s" % (tm.get('high'), tm.get('low'), tm.get('skytextday'))
        res = res + "\n지역: %s" % (observationpoint)

        return res

print(get_weather('청담동'))
