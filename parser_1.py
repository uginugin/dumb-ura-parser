import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pyfiglet import Figlet


f = Figlet(font='slant')
print(f.renderText("Super dumb parser"))

url = 'https://ura.news/svrd'
amount = int(input(
'''
Привет, я-парсер URA.news :)
Я рад, что мной кто-то пользуется!! Спасибо!
Сколько новостей будем парсить?
Введите кол-во: 
'''
))


def get_enough_news(amount):
    # Прогружаем новости до тех пор, пока у нас не наберется достаточного количества новостей на странице
    time.sleep(1)
    news = driver.find_elements(By.CLASS_NAME, 'publication-item')
    if len(news) < amount:
        update_button.click()
        get_enough_news(amount)


def get_text(url):
    # Получаем текст из конкретной новости
    soup=BeautifulSoup(requests.get(url).text, "html.parser")    
    data=soup.find_all('p')
    text = ' '.join(i.text for i in data[:len(data)-1])
    return text


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)
update_button = driver.find_element(By.ID, 'vc_load_more')
get_enough_news(amount)

soup = BeautifulSoup(driver.page_source, "html.parser")

data=soup.find_all('div', {'class': 'publication-item'})

href=[]
title=[]
text=[]
counter = 0

for i in data[:amount]:
    print(f"[{counter}] Парсим статью...", end=" ")
    _href = 'https://ura.news'+ i.find('a')['href']
    href.append(_href)
    title.append((i.find('div',class_="publication-item--title")).text.strip())
    text.append(get_text(_href))
    print("Done!")
    counter += 1

    
df=pd.DataFrame({
    'title':title,
    'href':href,
    'text':text,
    })

print("Записываем в Excel...", end=" ")
df.to_excel('uranews.xlsx')
print("Done!")
