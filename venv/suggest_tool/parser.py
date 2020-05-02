import requests
import re
from bs4 import BeautifulSoup

def parse_page(link):
    if 'www.edimdoma.ru' in link:
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
            cal = float(raw_cal.text)
        pfc = [0 ,0 , 0]
        i = 0
        for raw_nutr in soup.select('td.definition-list-table__td.definition-list-table__td_value'):
            
            if i > 2:
                break
            for better_nutr in re.findall(r'([\d]+) г', raw_nutr.text):
                pfc[i] = int(better_nutr)

            i += 1

        protein = float(pfc[0])
        fat = float(pfc[1])
        corb = float(pfc[2])

    elif 'eda.ru' in link:
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        name = 0
        for raw_name in soup.select('h1.recipe__name'):
            name = raw_name.text.strip().replace('\xa0', ' ')

        cpfc = [0, 0, 0 , 0]
        ind = 0
        for tag in soup.select('ul.nutrition__list li p.nutrition__weight'):
            minus_ones = False
            try:
                cpfc[ind] = float(tag.text.replace(',', '.'))
            except:
                minus_ones = True
            ind += 1

        if ind == 0 or minus_ones:
            for j in range(4):
                cpfc[j] = -1.0
        cal, protein, fat, corb = cpfc[0], cpfc[1], cpfc[2], cpfc[3]
        time = 0
        for raw_time in soup.select('span.info-pad__item span.info-text'):
            time = raw_time.text

    return name, time, cal, protein, fat, corb




