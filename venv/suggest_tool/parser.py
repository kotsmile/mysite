import requests
import re
from bs4 import BeautifulSoup


def get_all_from(link):
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    name = 0
    for raw_name in soup.select('h1.recipe-header__name'):  
        name = raw_name.text.strip()
    time = 0 

    for raw_time in soup.select('div.entry-stats__item.entry-stats__item_cooking'):
        for better_time in re.findall(r'Приготовление([\d\w\s]+)', raw_time.text):
                time = better_time
    cal = 0
    for raw_cal in soup.select('div.kkal-meter__value'):
        cal = int(raw_cal.text)
    pfc = [0 ,0 , 0]
    i = 0
    for raw_nutr in soup.select('td.definition-list-table__td.definition-list-table__td_value'):
        
        if i > 2:
            break
        for better_nutr in re.findall(r'([\d]+) г', raw_nutr.text):
            pfc[i] = int(better_nutr)

        i += 1

    protein = pfc[0]
    fat = pfc[1]
    corb = pfc[2]

    code = 0
    for raw_code in re.findall(r'([\d]+)', link.split('/')[-1]):
        code = int(raw_code)

    return code, name, time, cal, protein, fat, corb



