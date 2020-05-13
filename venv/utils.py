# import requests
# import re
# from bs4 import BeautifulSoup
# import pickle
# #
#
# def get_code(ref):
#     code_search = re.findall(r'[\d]+', ref)
#     for code in code_search:
#         return code
#
#
# def remover(l):
#     if l[0] == '':
#         return l[1]
#     return l[0]
#
#
# def fat_ref(code): return f'https://fitaudit.ru/food/{code}/fat'
#
#
# def protein_ref(code): return f'https://fitaudit.ru/food/{code}/protein'
#
#
# def carbohydrate_ref(code): return f'https://fitaudit.ru/food/{code}/carbohydrate'
#
#
# def vitamins_ref(code): return f'https://fitaudit.ru/food/{code}/vitamins'
#
#
# def amino_ref(code): return f'https://fitaudit.ru/food/{code}/amino'
#
#
# def minerals_ref(code): return f'https://fitaudit.ru/food/{code}/minerals'
#
#
# def get_all(ref):
#     soup = BeautifulSoup(requests.get(ref).text, 'html.parser')
#     code = get_code(ref)
#
#     # Название
#     name = -1
#     for tag in soup.select('h1'):
#         for raw_name in re.findall(r'([\w\s]+\(\)) —', tag.text):
#             # print('Название:', name)
#             name = raw_name
#
#     # Калории
#     cal = -1
#     for tag in soup.select('span.him_bx__legend_text'):
#         for raw_cal in re.findall(r'— ([\d]*) кКал', tag.text):
#             # print('Калории:', cal)
#             cal = int(raw_cal)
#
#     # Белки
#     protein = -1
#     new_soup = BeautifulSoup(requests.get(protein_ref(code)).text, 'html.parser')
#     for tag in new_soup.select('p.pr__brick.pr__ind_c.pr__brd_b'):
#         for raw_protein in re.findall(r'(\d+,\d+) г', tag.text):
#             # print('Белки:', protein)
#             protein = float(raw_protein.replace(',', '.'))
#
#     # Жиры
#     fat = -1
#     new_soup = BeautifulSoup(requests.get(fat_ref(code)).text, 'html.parser')
#     for tag in new_soup.select('p.pr__brick.pr__ind_c.pr__brd_b'):
#         for raw_fat in re.findall(r'(\d+,\d+) г', tag.text):
#             fat = float(raw_fat.replace(',', '.'))
#
#     # Углеводы
#     corb = -1
#     new_soup = BeautifulSoup(requests.get(carbohydrate_ref(code)).text, 'html.parser')
#     for tag in new_soup.select('p.pr__brick.pr__ind_c.pr__brd_b'):
#         for raw_corb in re.findall(r'([\d,]+) г \(клетчатка \+ крахмал \+ сахара\)', tag.text):
#             corb = float(raw_corb.replace(',', '.'))
#
#     gramm = 100
#     return name, cal, protein, fat, corb, gramm, ref
#
#
# link = 'https://fitaudit.ru/categories'
# print(link)
# cats = []
# soup = BeautifulSoup(requests.get(link).text, 'html.parser')
# for tag in soup.select('li.pr__brick.pr__brd_b > a'):
#     print((tag.text.strip(), tag['href']))
#     cats.append((tag.text.strip(), tag['href']))
# products = {}
# i = 0
# for cat_name, ref in cats[1:]:
#     print(f'{i}/{len(cats)}')
#     i += 1
#     soup = BeautifulSoup(requests.get(ref).text, 'html.parser')
#     products_ref = [tag['href'] for tag in soup.select('a.vertical_pseudo')]
#     products[cat_name] = []
#     j = 0
#     for pr in products_ref:
#         print(f'- {j}/{len(products_ref)}')
#         j += 1
#         products[cat_name].append(get_all(pr))
#         # print(get_all(pr))
# with open('name_cal_protein_fat_corb_gramm.pck', 'wb') as f:
#     pickle.dump(products, f)

import matplotlib.pyplot as plt

fig = plt.figure()
# Добавление на рисунок прямоугольной (по умолчанию) области рисования
a = [2500.0, 2471.4285714285716, 2442.857142857143, 2414.2857142857147, 2385.7142857142862, 2357.142857142858, 2328.5714285714294, 2300.000000000001, 2271.4285714285725, 2242.857142857144, 2214.2857142857156, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003, 2197.7133750000003]
plt.plot(range(len(a)), a)
plt.xlabel('День')
plt.ylabel('Вес, кг')
plt.grid(True)
plt.show()
