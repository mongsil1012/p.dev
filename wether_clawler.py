from bs4 import BeautifulSoup
import requests

def getWetherInfoFromNaver(str_locationInfo):
    url = "https://search.naver.com/search.naver?query={}+날씨".format(str_locationInfo)
    url_yesterday = "https://search.naver.com/search.naver?query=어제+날씨"
    html = requests.get(url)
    html_yesterday = requests.get(url_yesterday)
    soup = BeautifulSoup(html.text, 'html.parser')
    soup_yesterday = BeautifulSoup(html_yesterday.text, 'html.parser')

    wetherbox = soup.find('div', {'class': 'weather_box'})
    currentcast = wetherbox.find('p',{'class': 'cast_txt'}).text.split(',')[0]
    minmaxtempData = wetherbox.find('span',{'class': 'merge'})
    temp_min = minmaxtempData.find('span',{'class': 'min'}).text
    temp_max = minmaxtempData.find('span',{'class': 'max'}).text

    wether_yesterday = soup_yesterday.find('tr', {'class': 'rw_tr2'})
    temp_yesterday = wether_yesterday.find('p',{'class': 'temp'}).text
    temp_max_prev = int(temp_yesterday.split('/')[1].split("℃")[0])
    temp_max_interval = int(temp_max.split('˚')[0]) - temp_max_prev
    
    blindData = wetherbox.findAll('li',{'class': 'date_info today'})
    
    rain_rate_morning = int(str(blindData[0]).split("<span class=\"num\">")[1].split('<')[0])
    rain_rate_afternoon = int(str(blindData[0]).split("<span class=\"num\">")[2].split('<')[0])
    
    data2 = wetherbox.findAll('dd')
    status_dust = str(data2[0]).split("</span>")[1].split('<')[0]
    status_ultraDust = str(data2[1]).split("</span>")[1].split('<')[0]
    status_ozone = str(data2[2]).split("</span>")[1].split('<')[0]

    returnValue = str_locationInfo + "의 오늘 최저/최고 온도 : " + temp_min + "/" + temp_max
    returnValue = returnValue + "\n" + currentcast
    if temp_max_interval > 0: returnValue = returnValue + ", 낮기준 어제보다 " + str(temp_max_interval) + "도 높아요"
    elif temp_max_interval < 0: returnValue = returnValue + ", 낮기준 어제보다 " + str(temp_max_interval) + "도 낮아요"
    else : returnValue = returnValue + ", 최고온도 어제와 같아요"
    
    if rain_rate_morning > 50 or rain_rate_afternoon > 50:
        returnValue = returnValue + "\n강수확률이 오전" + str(rain_rate_morning) + "%/오후" + str(rain_rate_afternoon) + "%이니 주의!"
    returnValue = returnValue + "\n-미세먼지 : " + status_dust
    returnValue = returnValue + "\n-초미세먼지 : " + status_ultraDust
    returnValue = returnValue + "\n-오존지수 : " + status_ozone

    return returnValue

if __name__ == '__main__':
    result = getWetherInfoFromNaver("마북동")
    print(result)