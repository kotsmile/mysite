from suggest_tool.paths import *
import pickle
import requests
from suggest_tool.models import *
from suggest_tool.parser import *

import sys
import time
import re
from bs4 import BeautifulSoup
import pandas as pd

# recipes = load_pck(RECIPES_PATH)
# code_recipes = {}
# for r in recipes:
#     code_recipes[r.code] = r
# save_pck(code_recipes, CODE_RECIPES_PATH)
# b_s = '''https://www.edimdoma.ru/retsepty/135705-tselnozernovye-blinchiki
# https://www.edimdoma.ru/retsepty/134059-domashniy-yogurt-s-medom-i-orehami
# https://www.edimdoma.ru/retsepty/134058-ovsyanaya-kasha-s-fruktovym-salatom
# https://www.edimdoma.ru/retsepty/132702-pita-s-kuritsey
# https://www.edimdoma.ru/retsepty/131902-kruassan-s-semgoy
# https://www.edimdoma.ru/retsepty/133296-zapechennoe-avokado-s-yaytsom-i-syrom
# https://www.edimdoma.ru/retsepty/131535-tortilya-s-kuritsey-i-ovoschami
# https://www.edimdoma.ru/retsepty/130555-omlet-s-vetchinoy-i-ovoschami
# https://www.edimdoma.ru/retsepty/130006-brusketta-s-tuntsom
# https://www.edimdoma.ru/retsepty/130499-yaichnitsa-s-ovoschami
# https://www.edimdoma.ru/retsepty/127401-ovsyanoblin-s-lososem
# https://www.edimdoma.ru/retsepty/126316-salat-kapri
# https://www.edimdoma.ru/retsepty/126319-salat-s-tvorogom
# https://www.edimdoma.ru/retsepty/126199-yaytso-pashot-s-avokado
# https://www.edimdoma.ru/retsepty/125989-syrnyy-sandvich
# https://www.edimdoma.ru/retsepty/125546-salat-s-tuntsom-i-domashnim-mayonezom
# https://www.edimdoma.ru/retsepty/125631-salat-lyumier-s-forelyu
# https://www.edimdoma.ru/retsepty/125269-vesenniy-zavtrak
# https://www.edimdoma.ru/retsepty/125131-sandvich-iz-avokado-i-semgi
# https://www.edimdoma.ru/retsepty/125057-brusketta-s-avokado-i-krevetkami
# https://www.edimdoma.ru/retsepty/122544-tost-zlakovyy-s-avokado
# https://www.edimdoma.ru/retsepty/113564-tosty-so-shpinatom-yaytsami-i-parmezanom
# https://www.edimdoma.ru/retsepty/76990-salat-s-lososem-i-yaytsami-pashot
# https://www.edimdoma.ru/retsepty/77255-draniki-iz-tykvy
# https://www.edimdoma.ru/retsepty/137178-salat-s-krevetkami-sladkim-pertsem-i-zapravkoy-iz-avokado
# https://www.edimdoma.ru/retsepty/137265-pankeyki-bliny-dlya-stroynosti
# https://www.edimdoma.ru/retsepty/133871-karamelnaya-gerkulesovaya-kasha
# https://www.edimdoma.ru/retsepty/133544-pitstsa-na-rimskom-teste-s-syrom-buratta-i-proshutto
# https://www.edimdoma.ru/retsepty/133699-pshennaya-kasha-s-tykvoy-i-izyumom
# https://www.edimdoma.ru/retsepty/132586-frittata-s-gribami
# https://www.edimdoma.ru/retsepty/132806-brusketta-s-tvorogom-krasnoy-ryboy-i-perepelinym-yaytsom'''
# l_d = '''https://www.edimdoma.ru/retsepty/135793-salat-s-fasolyu-avokado-i-syrom-feta
# https://www.edimdoma.ru/retsepty/135306-tykvennyy-sup-pyure
# https://www.edimdoma.ru/retsepty/135242-ryba-s-ovoschami-na-paru
# https://www.edimdoma.ru/retsepty/136332-postnyy-gamburger
# https://www.edimdoma.ru/retsepty/137888-sochnaya-kurinaya-grudka-v-folge
# https://www.edimdoma.ru/retsepty/137656-azu-iz-indeyki
# https://www.edimdoma.ru/retsepty/137496-kurinyy-sup-s-lapshoy
# https://www.edimdoma.ru/retsepty/137708-ovoschnoy-sup-s-treskoy
# https://www.edimdoma.ru/retsepty/137408-salat-iz-pomidorov-i-rukoly
# https://www.edimdoma.ru/retsepty/137320-zapekanka-s-brokkoli-syrom-i-sousom-beshamel
# https://www.edimdoma.ru/retsepty/137032-domashnyaya-pasta-s-moreproduktami
# https://www.edimdoma.ru/retsepty/137002-azu-iz-kurinoy-grudki
# https://www.edimdoma.ru/retsepty/136678-salat-s-krevetkami-i-balzamicheskim-kremom
# https://www.edimdoma.ru/retsepty/136865-teplyy-salat-s-govyadinoy-i-rukoloy
# https://www.edimdoma.ru/retsepty/134574-kurinaya-grudka-s-tykvoy
# https://www.edimdoma.ru/retsepty/134157-salat-s-risom-i-seldereem
# https://www.edimdoma.ru/retsepty/133988-tykvennyy-sup-pyure-s-nutom
# https://www.edimdoma.ru/retsepty/133648-zelenoe-rizotto-s-krevetkami
# https://www.edimdoma.ru/retsepty/133575-kabachkovaya-zapekanka
# https://www.edimdoma.ru/retsepty/132581-penne-s-tykvoy-i-indeykoy
# https://www.edimdoma.ru/retsepty/133297-talyatelle-s-ovoschami-i-soevym-sousom
# https://www.edimdoma.ru/retsepty/132281-pasta-s-kalmarami-v-tomatnom-souse
# https://www.edimdoma.ru/retsepty/132303-fuzilli-s-mintaem
# https://www.edimdoma.ru/retsepty/132810-zapechennye-ruletiki-iz-baklazhanov-s-parmezanom
# https://www.edimdoma.ru/retsepty/131979-slivochno-kurinyy-sup
# https://www.edimdoma.ru/retsepty/132749-nezhnaya-kuritsa-s-kartoshkoy-v-banke
# https://www.edimdoma.ru/retsepty/131970-teplyy-ovoschnoy-salat-s-bekonom-i-yaytsom-pashot
# https://www.edimdoma.ru/retsepty/132501-teplyy-salat-s-shampinonami-i-kedrovymi-oreshkami
# https://www.edimdoma.ru/retsepty/131973-losos-s-sousom-pesto
# https://www.edimdoma.ru/retsepty/132410-zapekanka-iz-kabachkov-s-syrom-i-pomidorami
# https://www.edimdoma.ru/retsepty/132003-kurinoe-file-kapreze'''
# recipes = []
# code_recipes = {}

# eq_conf = {
#     'const': 88.36,
#     'c_weight': 13.4,
#     'c_height': 4.8,
#     'c_age': -5.7,
# }

# with open(EQ_CONF_PATH, 'wb') as file:
#     pickle.dump(eq_conf, file)

# for link in b_s.split('\n'):
#     print(link)
#     print(get_all_from(link))
#     if link == '':
#         continue
#     recipe1 = Recipe(recipe_type=BREAKFAST, link=link)
#     recipe2 = Recipe(recipe_type=SNACK, link=link)

#     recipes.append(recipe1)
#     recipes.append(recipe2)

#     code_recipes[recipe1.code] = recipe1
#     code_recipes[recipe2.code] = recipe2

# for link in l_d.split('\n'):
#     print(link)
#     if link == '':
#         continue
#     recipe1 = Recipe(recipe_type=LUNCH, link=link)
#     recipe2 = Recipe(recipe_type=DINNER, link=link)

#     recipes.append(recipe1)
#     recipes.append(recipe2)

#     code_recipes[recipe1.code] = recipe1
#     code_recipes[recipe2.code] = recipe2

# recipes = sorted(recipes, key=lambda x: x.code)

# with open(RECIPES_PATH, 'wb') as file:
#     pickle.dump(recipes, file)

# with open(CODE_RECIPES_PATH, 'wb') as file:
#     pickle.dump(code_recipes, file)

# activity_levels = [
#     ActivityLevel(name='Минимальный', abr='min', percent=1.2),
#     ActivityLevel(name='Низкий', abr='low', percent=1.375),
#     ActivityLevel(name='Средний', abr='med', percent=1.55),
#     ActivityLevel(name='Высокий', abr='high', percent=1.725),
#     ActivityLevel(name='Очень высокий', abr='ex_high', percent=1.9)
# ]

# goals = [
#     Goal(name='Похудание', abr='losing', percent=0.8, pfc=[0.0, 0.0, 0.0]),
#     Goal(name='Поддержка', abr='saving', percent=1.0, pfc=[0.0, 0.0, 0.0]),
#     Goal(name='Набор', abr='gain', percent=1.2, pfc=[0.25, 0.3, 0.45]),
# ]

# [('one_day', '1 день'), ('week', '7 дней')]
# periods = [
#     Period(name='1 день', abr='1', days=1),
#     Period(name='Неделя', abr='7', days=7),
#     Period(name='Месяц', abr='30', days=30),
#     Period(name='2 месяца', abr='60', days=60),
#     Period(name='4 месяца', abr='120', days=120),
#     Period(name='6 месяцев', abr='180', days=180),
    
# ]

# with open(PERIODS_PATH, 'wb') as file:
#     pickle.dump(periods, file)


# with open(ACTIVITY_LEVELS_PATH, 'wb') as file:
#     pickle.dump(activity_levels, file)

# with open(GOALS_PATH, 'wb') as file:
#     pickle.dump(goals, file)

    # self.code = code
    # self.name = name
    # self.link = link

    # self.type_ = type_

    # self.category = category
    # self.country = country
    # self.menu = menu

    # self.calories = calories
    # self.protein = protein
    # self.fat = fat
    # self.corb = corb

    # self.time = time
    # self.rating = rating

#   convertion = {
#     'Завтраки': ['Завтрак'],
#     'Супы': ['Обед'],
#     'Основные блюда': ['Обед', 'Ужин'],
#     'Выпечка и десерты': ['Перекус'],
#     'Салаты': ['Перекус'],
#     'Сэндвичи': ['Перекус']
# }
# with open(UPDATE_PATH, 'wb') as file:
#             pickle.dump(False, file)

# t1 = time.time()
# with open(RECIPES_PATH, 'rb') as f:
#     recipes = pickle.load(f)

# columns=['Завтрак', 'Обед', 'Перекус', 'Ужин', 'Калории', 'Белки', 'Жиры', 'Углеводы']

# day_menu = pd.DataFrame([], columns=columns)

# day_menu = day_menu.astype({
#         'Завтрак': 'int32',
#         'Обед': 'int32',
#         'Перекус': 'int32',
#         'Ужин': 'int32',
#         'Калории': 'float16',
#         'Белки': 'float16',
#         'Жиры': 'float16',
#         'Углеводы': 'float16',
# })

# breakfasts = []
# lunchs = []
# snackes = []
# dinners = []

# for r in recipes:
#     if r.recipe_type.name == 'Завтрак':
#         breakfasts.append(r)
#     elif r.recipe_type.name == 'Обед':
#         lunchs.append(r)
#     elif r.recipe_type.name== 'Перекус':
#         snackes.append(r)
#     elif r.recipe_type.name == 'Ужин':
#         dinners.append(r)

# i = 0
# for b in breakfasts:
#     for l in lunchs:
#         for s in snackes:
#             for d in dinners:
#                 i += 1
#                 if not len({b.code, l.code, s.code, d.code}) == 4:
#                     continue
#                 row = [
#                     b.code,
#                     l.code,
#                     s.code,
#                     d.code,
#                     b.calories + l.calories + s.calories + d.calories,
#                     b.protein + l.protein + s.protein + d.protein,
#                     b.fat + l.fat + s.fat + d.fat,
#                     b.corb + l.corb + s.corb + d.corb,
#                 ]


#                 print(f'{int(i * 100 / (len(breakfasts) * len(lunchs) * len(snackes) * len(dinners)))}%, {int(day_menu.memory_usage().sum() / 1000000)} MB')
#                 day_menu = day_menu.append(pd.DataFrame([row], columns=columns))


# day_menu.to_pickle(DAY_MENU_PATH)

# print(f'time: {int(time.time() - t1)} sec')

# with open(CODES_AMOUNTS_LINKS_INGS_CATS_PATH, 'rb') as f:
#     codes_amounts_links_ings_cats = pickle.load(f)

# recipes = []
# for code, amount, link, _, cat in codes_amounts_links_ings_cats:
#     # recipes.append(Recipe(code=c))
#     num = recipes_old['Номер'].index(code)

#     code = recipes_old['Номер'][num]
#     name = recipes_old['Название'][num]
#     link = recipes_old['Ссылка'][num]

#     category = recipes_old['Категория'][num]
#     country = recipes_old['Страна'][num]
#     menu = recipes_old['Меню'][num]

#     calories = recipes_old['Калорийность, ккал'][num]
#     protein = recipes_old['Белки, г'][num]
#     fat = recipes_old['Жиры, г'][num]
#     corb = recipes_old['Углеводы, г'][num]

#     time = recipes_old['Время приготовления'][num]
#     rating = recipes_old['Рейтинг'][num]

#     row = (
#         code, 
#         name, 
#         link, 
#         category, 
#         country, 
#         menu,
#         calories,
#         protein,
#         fat,
#         corb,
#         time,
#         int(rating)
#     )
#     recipes.append(row)

# with open(RECIPES_RAW_PATH, 'wb') as f:
#     pickle.dump(recipes, f)



# with open(CODES_AMOUNTS_LINKS_INGS_CATS_PATH, 'rb') as f:
#     codes_amounts_links_ings_cats = pickle.load(f)

# recipes = []
# for c, _, _, _ ,_ in codes_amounts_links_ings_cats:
#     recipes.append(Recipe(code=c))

# with open(RECIPES_PATH, 'wb') as f:
#     pickle.dump(recipes, f)


# # print(set(t['Категория']))

# cats = [
#     'Завтраки',
#     'Супы',
#     'Основные блюда',
#     'Выпечка и десерты',
#     'Салаты',
#     'Сэндвичи'
# ]

# # ['Номер',
# #  'Название',
# #   'Ссылка', 
# #   'Страна', 
# #   'Категория', 
# #   'Меню', 
# #   'Калорийность, ккал', 
# #   'Белки, г', 
# #   'Жиры, г', 
# #   'Углеводы, г', 
# #   'Время приготовления', 
# #   'Лайки', 
# #   'Дизлайки', 
# #   'Рейтинг']

# code',
# 'Название',
# 'Категории',
# 'Калории, кКал',
# 'Белки, г',
# 'Жиры, г',
# 'Углеводы, г',
# 'Вода, г',
# 'Зола, г',
# 'Сахара, г',
# 'Клетчаткa, г',
# 'Холестерин, мг',
# 'Трансжиров, г',
# 'Витамин A, мкг',
# 'Бета-каротин, мкг',
# 'Альфа-каротин, мкг',
# 'Витамин D, мкг',
# 'Витамин E, мг',
# 'Витамин K, мкг',
# 'Витамин C, мг',
# 'Витамин B1, мг',
# 'Витамин B2, мг',
# 'Витамин B3, мг',
# 'Витамин B4, мг',
# 'Витамин B5, мг',
# 'Витамин B6, мг',
# 'Витамин B9, мкг',
# 'Витамин B12, мкг',
# 'Триптофан, г',
# 'Треонин, г',
# 'Изолейцин, г',
# 'Лейцин, г',
# 'Лизин, г',
# 'Метионин, г',
# 'Цистин, г',
# 'Фенилаланин, г',
# 'Тирозин, г',
# 'Валин, г',
# 'Аргинин, г',
# 'Гистидин, г',
# 'Аланин, г',
# 'Аспарагиновая, г',
# 'Глутаминовая, г',
# 'Глицин, г',
# 'Пролин, г',
# 'Серин, г',
# 'Кальций, мг',
# 'Железо, мг',
# 'Магний, мг',
# 'Фосфор, мг',
# 'Калий, мг',
# 'Натрий, мг',
# 'Цинк, мг',
# 'Медь, мг',
# 'Марганец, мг',
# 'Селен, мкг

# def get_link_from_code(need_code):
#     for code, link in zip(t['Номер'], t['Ссылка']):
#         if code == need_code:
#             return link

# def get_first(need_cat, max_amount):
#     codes_ratings = []

#     for code, cat, rating in zip(t['Номер'], t['Категория'], t['Рейтинг']):
#         if cat == need_cat:
#             codes_ratings.append((code, rating))

#     if len(codes_ratings) < max_amount:
#         return [n for n, r in codes_ratings]
#     else:
#         sorted(codes_ratings, key=lambda ing: ing[1], reverse=True)
#         return [n for n, r in codes_ratings[:max_amount]]


# # <span class="info-text js-portions-count-print" itemprop="recipeYield">3 порции</span>

# all_ings = set()
# codes_amounts_links_ings_cats = []
# for c in cats:

#     codes_of_cat = get_first(c, 200)
    
#     i = 0
#     for code in codes_of_cat:
#         cute_ = ''
#         for cs in cats:
#             if cs == c:
#                 cute_ += '\u0332'.join(c) + ', '
#             else:
#                 cute_ += cs + ', '
#         print(f'{i}/200 : {cute_}')
#         i += 1
#         link = get_link_from_code(code)
#         soup = BeautifulSoup(requests.get(link).text, 'html.parser')
#         amount = 0
#         for porc in soup.select('span.info-text.js-portions-count-print'):  
#             for am in re.findall(r'([\d]+) пор', porc.text):
#                 amount = int(am)

        
#         ings_names = []
#         for ing_name in soup.select('span.js-tooltip.js-tooltip-ingredient'):
#             ings_names.append(ing_name.text.strip())


#         ings_meas = []
#         for ing_meas in soup.select('span.content-item__measure.js-ingredient-measure-amount'):
#             ings_meas.append(ing_meas.text.strip())


#         ings = [(n, m) for n, m in zip(ings_names, ings_meas)]

#         codes_amounts_links_ings_cats.append((code, amount, link, ings, c))
    
# with open('codes_amounts_links_ings_cats.pck', 'wb') as f:
#     pickle.dump(codes_amounts_links_ings_cats, f)

# codes_amounts_links_ings_cats = []
# with open('codes_amounts_links_ings_cats.pck', 'rb') as f:
#     codes_amounts_links_ings_cats = pickle.load(f)

# all_ings = []
# for _, _, _, ing, _ in codes_amounts_links_ings_cats:
#     for n, v in ing:
#         if n not in all_ings:
#             # print(n, v)
#             all_ings.append(n)

# print(len(all_ings))

# with open(INGREDIENTS_PATH, 'rb') as f:
#     t = pickle.load(f)
# names = t['Название']


# convert = {}

# i = 0
# goods = 0
# with open('convert.pck', 'rb') as f:
#     convert = pickle.load(f)

# for ing in all_ings:
#     i += 1
#     found = False
#     if ing not in convert.keys():
    
        
#         for n in names:
#             if n == ing:
#                 convert[ing] = n
#                 found = True
#                 break

#         if not found:
#             for n in names:
#                 if list(set(ing.lower().split()) & set(n.lower().split())):
#                     print(ing, n, sep='?=')
#                     ans = input()
#                     if ans == '1':
#                         convert[ing] = n
#                         found = True
#                         break
#                     elif ans == 's':
#                         with open('convert.pck', 'wb') as f:
#                             pickle.dump(convert, f)
#     else:
#         found = True
#     if found:
#         goods += 1
#     print(f'{i}/{len(all_ings)}, {goods}')

# with open('convert.pck', 'wb') as f:
#     pickle.dump(convert, f)
# <div class="ingredients-list__content" cellpadding="0" cellspacing="0">
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13418, &quot;name&quot;: &quot;Яйцо куриное&quot;, &quot;amount&quot;: &quot;2 штуки&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13418">
#         Яйцо куриное
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13418">2 штуки</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13421, &quot;name&quot;: &quot;Соль&quot;, &quot;amount&quot;: &quot;1 чайная ложка&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13421">
#         Соль
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13421">1 чайная ложка</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13410, &quot;name&quot;: &quot;Сахар&quot;, &quot;amount&quot;: &quot;3 столовые ложки&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13410">
#         Сахар
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13410">3 столовые ложки</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13453, &quot;name&quot;: &quot;Молоко&quot;, &quot;amount&quot;: &quot;2 стакана&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13453">
#         Молоко
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13453">2 стакана</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13458, &quot;name&quot;: &quot;Пшеничная мука&quot;, &quot;amount&quot;: &quot;2 стакана&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13458">
#         Пшеничная мука
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13458">2 стакана</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 15321, &quot;name&quot;: &quot;Гашеная сода&quot;, &quot;amount&quot;: &quot;1 чайная ложка&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="15321">
#         Гашеная сода
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="15321">1 чайная ложка</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13423, &quot;name&quot;: &quot;Растительное масло&quot;, &quot;amount&quot;: &quot;¼ стакана&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13423">
#         Растительное масло
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13423">¼ стакана</span>
#   </p>
# </div>


