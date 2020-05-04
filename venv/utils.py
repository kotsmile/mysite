
import pickle
import requests
import time
import re
from bs4 import BeautifulSoup
import pandas as pd
from suggest_tool.models import *
from suggest_tool.paths import *
from suggest_tool.parser import noty

links = '''b https://eda.ru/recepty/zavtraki/yachnevaya-kasha-na-mindalnom-moloke-91833
b https://www.edimdoma.ru/retsepty/135705-tselnozernovye-blinchiki
b https://www.edimdoma.ru/retsepty/134059-domashniy-yogurt-s-medom-i-orehami
b https://www.edimdoma.ru/retsepty/134058-ovsyanaya-kasha-s-fruktovym-salatom
b https://www.edimdoma.ru/retsepty/132702-pita-s-kuritsey
b https://www.edimdoma.ru/retsepty/131902-kruassan-s-semgoy
b https://www.edimdoma.ru/retsepty/133296-zapechennoe-avokado-s-yaytsom-i-syrom
b https://www.edimdoma.ru/retsepty/131535-tortilya-s-kuritsey-i-ovoschami
b https://www.edimdoma.ru/retsepty/130555-omlet-s-vetchinoy-i-ovoschami
b https://www.edimdoma.ru/retsepty/130006-brusketta-s-tuntsom
b https://www.edimdoma.ru/retsepty/130499-yaichnitsa-s-ovoschami
b https://www.edimdoma.ru/retsepty/127401-ovsyanoblin-s-lososem
b https://www.edimdoma.ru/retsepty/126316-salat-kapri
b https://www.edimdoma.ru/retsepty/126319-salat-s-tvorogom
b https://www.edimdoma.ru/retsepty/126199-yaytso-pashot-s-avokado
b https://www.edimdoma.ru/retsepty/125989-syrnyy-sandvich
b https://www.edimdoma.ru/retsepty/125546-salat-s-tuntsom-i-domashnim-mayonezom
b https://www.edimdoma.ru/retsepty/125631-salat-lyumier-s-forelyu
b https://www.edimdoma.ru/retsepty/125269-vesenniy-zavtrak
b https://www.edimdoma.ru/retsepty/125131-sandvich-iz-avokado-i-semgi
b https://www.edimdoma.ru/retsepty/125057-brusketta-s-avokado-i-krevetkami
b https://www.edimdoma.ru/retsepty/122544-tost-zlakovyy-s-avokado
b https://www.edimdoma.ru/retsepty/113564-tosty-so-shpinatom-yaytsami-i-parmezanom
b https://www.edimdoma.ru/retsepty/76990-salat-s-lososem-i-yaytsami-pashot
b https://www.edimdoma.ru/retsepty/77255-draniki-iz-tykvy
b https://www.edimdoma.ru/retsepty/137178-salat-s-krevetkami-sladkim-pertsem-i-zapravkoy-iz-avokado
b https://www.edimdoma.ru/retsepty/137265-pankeyki-bliny-dlya-stroynosti
b https://www.edimdoma.ru/retsepty/133871-karamelnaya-gerkulesovaya-kasha
b https://www.edimdoma.ru/retsepty/133544-pitstsa-na-rimskom-teste-s-syrom-buratta-i-proshutto
b https://www.edimdoma.ru/retsepty/133699-pshennaya-kasha-s-tykvoy-i-izyumom
b https://www.edimdoma.ru/retsepty/132586-frittata-s-gribami
b https://www.edimdoma.ru/retsepty/132806-brusketta-s-tvorogom-krasnoy-ryboy-i-perepelinym-yaytsom
s https://www.edimdoma.ru/retsepty/135705-tselnozernovye-blinchiki
s https://www.edimdoma.ru/retsepty/134059-domashniy-yogurt-s-medom-i-orehami
s https://www.edimdoma.ru/retsepty/134058-ovsyanaya-kasha-s-fruktovym-salatom
s https://www.edimdoma.ru/retsepty/132702-pita-s-kuritsey
s https://www.edimdoma.ru/retsepty/131902-kruassan-s-semgoy
s https://www.edimdoma.ru/retsepty/133296-zapechennoe-avokado-s-yaytsom-i-syrom
s https://www.edimdoma.ru/retsepty/131535-tortilya-s-kuritsey-i-ovoschami
s https://www.edimdoma.ru/retsepty/130555-omlet-s-vetchinoy-i-ovoschami
s https://www.edimdoma.ru/retsepty/130006-brusketta-s-tuntsom
s https://www.edimdoma.ru/retsepty/130499-yaichnitsa-s-ovoschami
s https://www.edimdoma.ru/retsepty/127401-ovsyanoblin-s-lososem
s https://www.edimdoma.ru/retsepty/126316-salat-kapri
s https://www.edimdoma.ru/retsepty/126319-salat-s-tvorogom
s https://www.edimdoma.ru/retsepty/126199-yaytso-pashot-s-avokado
s https://www.edimdoma.ru/retsepty/125989-syrnyy-sandvich
s https://www.edimdoma.ru/retsepty/125546-salat-s-tuntsom-i-domashnim-mayonezom
s https://www.edimdoma.ru/retsepty/125631-salat-lyumier-s-forelyu
s https://www.edimdoma.ru/retsepty/125269-vesenniy-zavtrak
s https://www.edimdoma.ru/retsepty/125131-sandvich-iz-avokado-i-semgi
s https://www.edimdoma.ru/retsepty/125057-brusketta-s-avokado-i-krevetkami
s https://www.edimdoma.ru/retsepty/122544-tost-zlakovyy-s-avokado
s https://www.edimdoma.ru/retsepty/113564-tosty-so-shpinatom-yaytsami-i-parmezanom
s https://www.edimdoma.ru/retsepty/76990-salat-s-lososem-i-yaytsami-pashot
s https://www.edimdoma.ru/retsepty/77255-draniki-iz-tykvy
s https://www.edimdoma.ru/retsepty/137178-salat-s-krevetkami-sladkim-pertsem-i-zapravkoy-iz-avokado
s https://www.edimdoma.ru/retsepty/137265-pankeyki-bliny-dlya-stroynosti
s https://www.edimdoma.ru/retsepty/133871-karamelnaya-gerkulesovaya-kasha
s https://www.edimdoma.ru/retsepty/133544-pitstsa-na-rimskom-teste-s-syrom-buratta-i-proshutto
s https://www.edimdoma.ru/retsepty/133699-pshennaya-kasha-s-tykvoy-i-izyumom
s https://www.edimdoma.ru/retsepty/132586-frittata-s-gribami
s https://www.edimdoma.ru/retsepty/132806-brusketta-s-tvorogom-krasnoy-ryboy-i-perepelinym-yaytsom
s https://eda.ru/recepty/salaty/salat-iz-lososja-seldereja-morkovi-31111
s https://eda.ru/recepty/zakuski/ruletiki-s-semgoj-sirom-filadelfija-30444
s https://eda.ru/recepty/vypechka-deserty/lvovskiy-syrnik-137289
s https://eda.ru/recepty/zakuski/inzhir-s-balzamiko-29858
s https://eda.ru/recepty/vypechka-deserty/morkovnaya-halva-57047
s https://eda.ru/recepty/vypechka-deserty/jogurtovoe-morozhenoe-s-avokado-ogurcom-28448
s https://eda.ru/recepty/vypechka-deserty/zapechennye-yabloki-s-tvorogom-i-yagodami-138702
s https://eda.ru/recepty/vypechka-deserty/dieticheskoe-bananovoe-morozhenoe-27592
s https://eda.ru/recepty/vypechka-deserty/jablochno-bananovij-chizkejk-bez-zapekanija-24955
s https://eda.ru/recepty/vypechka-deserty/dieticheskaja-sharlotka-24685
s https://eda.ru/recepty/vypechka-deserty/tvorozhno-bananovij-muss-dlja-hudejushhih-44461
s https://eda.ru/recepty/zavtraki/tropicheskij-chia-puding-55392
l https://www.edimdoma.ru/retsepty/135793-salat-s-fasolyu-avokado-i-syrom-feta
l https://www.edimdoma.ru/retsepty/135306-tykvennyy-sup-pyure
l https://www.edimdoma.ru/retsepty/135242-ryba-s-ovoschami-na-paru
l https://www.edimdoma.ru/retsepty/136332-postnyy-gamburger
l https://www.edimdoma.ru/retsepty/137888-sochnaya-kurinaya-grudka-v-folge
l https://www.edimdoma.ru/retsepty/137656-azu-iz-indeyki
l https://www.edimdoma.ru/retsepty/137496-kurinyy-sup-s-lapshoy
l https://www.edimdoma.ru/retsepty/137708-ovoschnoy-sup-s-treskoy
l https://www.edimdoma.ru/retsepty/137408-salat-iz-pomidorov-i-rukoly
l https://www.edimdoma.ru/retsepty/137320-zapekanka-s-brokkoli-syrom-i-sousom-beshamel
l https://www.edimdoma.ru/retsepty/137032-domashnyaya-pasta-s-moreproduktami
l https://www.edimdoma.ru/retsepty/137002-azu-iz-kurinoy-grudki
l https://www.edimdoma.ru/retsepty/136678-salat-s-krevetkami-i-balzamicheskim-kremom
l https://www.edimdoma.ru/retsepty/136865-teplyy-salat-s-govyadinoy-i-rukoloy
l https://www.edimdoma.ru/retsepty/134574-kurinaya-grudka-s-tykvoy
l https://www.edimdoma.ru/retsepty/134157-salat-s-risom-i-seldereem
l https://www.edimdoma.ru/retsepty/133988-tykvennyy-sup-pyure-s-nutom
l https://www.edimdoma.ru/retsepty/133648-zelenoe-rizotto-s-krevetkami
l https://www.edimdoma.ru/retsepty/133575-kabachkovaya-zapekanka
l https://www.edimdoma.ru/retsepty/132581-penne-s-tykvoy-i-indeykoy
l https://www.edimdoma.ru/retsepty/133297-talyatelle-s-ovoschami-i-soevym-sousom
l https://www.edimdoma.ru/retsepty/132281-pasta-s-kalmarami-v-tomatnom-souse
l https://www.edimdoma.ru/retsepty/132303-fuzilli-s-mintaem
l https://www.edimdoma.ru/retsepty/132810-zapechennye-ruletiki-iz-baklazhanov-s-parmezanom
l https://www.edimdoma.ru/retsepty/131979-slivochno-kurinyy-sup
l https://www.edimdoma.ru/retsepty/132749-nezhnaya-kuritsa-s-kartoshkoy-v-banke
l https://www.edimdoma.ru/retsepty/131970-teplyy-ovoschnoy-salat-s-bekonom-i-yaytsom-pashot
l https://www.edimdoma.ru/retsepty/132501-teplyy-salat-s-shampinonami-i-kedrovymi-oreshkami
l https://www.edimdoma.ru/retsepty/131973-losos-s-sousom-pesto
l https://www.edimdoma.ru/retsepty/132410-zapekanka-iz-kabachkov-s-syrom-i-pomidorami
l https://www.edimdoma.ru/retsepty/132003-kurinoe-file-kapreze
l https://www.edimdoma.ru/retsepty/131385-gribnoy-sup-pyure
l https://www.edimdoma.ru/retsepty/131461-krem-sup-iz-tsvetnoy-kapusty-s-gorgonzoloy
l https://www.edimdoma.ru/retsepty/131390-zapekanka-iz-tsvetnoy-kapusty-i-kuritsy
l https://www.edimdoma.ru/retsepty/131469-lukovyy-krem-sup
l https://www.edimdoma.ru/retsepty/131468-ravioli-s-rikottoy-i-shpinatom
l https://www.edimdoma.ru/retsepty/130224-salat-s-tuntsom-i-gorgonzoloy
l https://www.edimdoma.ru/retsepty/130063-kesadilya-s-krevetkami
l https://www.edimdoma.ru/retsepty/130062-sup-s-krevetkami
l https://www.edimdoma.ru/retsepty/130797-kurinye-kotlety-s-motsarelloy-i-bazilikom
l https://www.edimdoma.ru/retsepty/130616-teplyy-salat-s-tuntsom-i-tselnozernovymi-makaronami
l https://www.edimdoma.ru/retsepty/130534-salat-s-tuntsom-il-faro
l https://www.edimdoma.ru/retsepty/130153-fuzilli-s-ovoschami-pod-sousom-ayoli
l https://www.edimdoma.ru/retsepty/129894-grechka-po-kupecheski
l https://www.edimdoma.ru/retsepty/129378-kotlety-iz-molodoy-morkovi-s-fetoy-i-orehami
l https://www.edimdoma.ru/retsepty/129044-tomatnyy-sup-pyure
l https://www.edimdoma.ru/retsepty/128945-tomatnyy-gaspacho-s-paprikoy-i-motsarelloy
l https://www.edimdoma.ru/retsepty/127386-salat-s-krevetkami-i-motsarelloy
l https://www.edimdoma.ru/retsepty/127539-kuritsa-s-tomatami-i-shpinatom-v-hrustyaschem-lavashe
l https://www.edimdoma.ru/retsepty/127350-vesennie-ovoschnye-kotletki
l https://www.edimdoma.ru/retsepty/126477-salat-iz-shampinonov-i-avokado
l https://www.edimdoma.ru/retsepty/125841-rolly-iz-omleta-s-avokado-pomidorami-i-zelenyu
l https://www.edimdoma.ru/retsepty/125760-ovoschi-s-bulgurom
l https://www.edimdoma.ru/retsepty/53475-kurinye-rublenye-kotletki-s-tsvetnoy-kapustoy-i-paprikoy
l https://www.edimdoma.ru/retsepty/136509-shashlychki-iz-lososya-s-ovoschami
d https://www.edimdoma.ru/retsepty/135793-salat-s-fasolyu-avokado-i-syrom-feta
d https://www.edimdoma.ru/retsepty/135306-tykvennyy-sup-pyure
d https://www.edimdoma.ru/retsepty/135242-ryba-s-ovoschami-na-paru
d https://www.edimdoma.ru/retsepty/136332-postnyy-gamburger
d https://www.edimdoma.ru/retsepty/137888-sochnaya-kurinaya-grudka-v-folge
d https://www.edimdoma.ru/retsepty/137656-azu-iz-indeyki
d https://www.edimdoma.ru/retsepty/137496-kurinyy-sup-s-lapshoy
d https://www.edimdoma.ru/retsepty/137708-ovoschnoy-sup-s-treskoy
d https://www.edimdoma.ru/retsepty/137408-salat-iz-pomidorov-i-rukoly
d https://www.edimdoma.ru/retsepty/137320-zapekanka-s-brokkoli-syrom-i-sousom-beshamel
d https://www.edimdoma.ru/retsepty/137032-domashnyaya-pasta-s-moreproduktami
d https://www.edimdoma.ru/retsepty/137002-azu-iz-kurinoy-grudki
d https://www.edimdoma.ru/retsepty/136678-salat-s-krevetkami-i-balzamicheskim-kremom
d https://www.edimdoma.ru/retsepty/136865-teplyy-salat-s-govyadinoy-i-rukoloy
d https://www.edimdoma.ru/retsepty/134574-kurinaya-grudka-s-tykvoy
d https://www.edimdoma.ru/retsepty/134157-salat-s-risom-i-seldereem
d https://www.edimdoma.ru/retsepty/133988-tykvennyy-sup-pyure-s-nutom
d https://www.edimdoma.ru/retsepty/133648-zelenoe-rizotto-s-krevetkami
d https://www.edimdoma.ru/retsepty/133575-kabachkovaya-zapekanka
d https://www.edimdoma.ru/retsepty/132581-penne-s-tykvoy-i-indeykoy
d https://www.edimdoma.ru/retsepty/133297-talyatelle-s-ovoschami-i-soevym-sousom
d https://www.edimdoma.ru/retsepty/132281-pasta-s-kalmarami-v-tomatnom-souse
d https://www.edimdoma.ru/retsepty/132303-fuzilli-s-mintaem
d https://www.edimdoma.ru/retsepty/132810-zapechennye-ruletiki-iz-baklazhanov-s-parmezanom
d https://www.edimdoma.ru/retsepty/131979-slivochno-kurinyy-sup
d https://www.edimdoma.ru/retsepty/132749-nezhnaya-kuritsa-s-kartoshkoy-v-banke
d https://www.edimdoma.ru/retsepty/131970-teplyy-ovoschnoy-salat-s-bekonom-i-yaytsom-pashot
d https://www.edimdoma.ru/retsepty/132501-teplyy-salat-s-shampinonami-i-kedrovymi-oreshkami
d https://www.edimdoma.ru/retsepty/131973-losos-s-sousom-pesto
d https://www.edimdoma.ru/retsepty/132410-zapekanka-iz-kabachkov-s-syrom-i-pomidorami
d https://www.edimdoma.ru/retsepty/132003-kurinoe-file-kapreze
d https://www.edimdoma.ru/retsepty/131385-gribnoy-sup-pyure
d https://www.edimdoma.ru/retsepty/131461-krem-sup-iz-tsvetnoy-kapusty-s-gorgonzoloy
d https://www.edimdoma.ru/retsepty/131390-zapekanka-iz-tsvetnoy-kapusty-i-kuritsy
d https://www.edimdoma.ru/retsepty/131469-lukovyy-krem-sup
d https://www.edimdoma.ru/retsepty/131468-ravioli-s-rikottoy-i-shpinatom
d https://www.edimdoma.ru/retsepty/130224-salat-s-tuntsom-i-gorgonzoloy
d https://www.edimdoma.ru/retsepty/130063-kesadilya-s-krevetkami
d https://www.edimdoma.ru/retsepty/130062-sup-s-krevetkami
d https://www.edimdoma.ru/retsepty/130797-kurinye-kotlety-s-motsarelloy-i-bazilikom
d https://www.edimdoma.ru/retsepty/130616-teplyy-salat-s-tuntsom-i-tselnozernovymi-makaronami
d https://www.edimdoma.ru/retsepty/130534-salat-s-tuntsom-il-faro
d https://www.edimdoma.ru/retsepty/130153-fuzilli-s-ovoschami-pod-sousom-ayoli
d https://www.edimdoma.ru/retsepty/129894-grechka-po-kupecheski
d https://www.edimdoma.ru/retsepty/129378-kotlety-iz-molodoy-morkovi-s-fetoy-i-orehami
d https://www.edimdoma.ru/retsepty/129044-tomatnyy-sup-pyure
d https://www.edimdoma.ru/retsepty/128945-tomatnyy-gaspacho-s-paprikoy-i-motsarelloy
d https://www.edimdoma.ru/retsepty/127386-salat-s-krevetkami-i-motsarelloy
d https://www.edimdoma.ru/retsepty/127539-kuritsa-s-tomatami-i-shpinatom-v-hrustyaschem-lavashe
d https://www.edimdoma.ru/retsepty/127350-vesennie-ovoschnye-kotletki
d https://www.edimdoma.ru/retsepty/126477-salat-iz-shampinonov-i-avokado
d https://www.edimdoma.ru/retsepty/125841-rolly-iz-omleta-s-avokado-pomidorami-i-zelenyu
d https://www.edimdoma.ru/retsepty/125760-ovoschi-s-bulgurom 
d https://www.edimdoma.ru/retsepty/53475-kurinye-rublenye-kotletki-s-tsvetnoy-kapustoy-i-paprikoy
d https://www.edimdoma.ru/retsepty/136509-shashlychki-iz-lososya-s-ovoschami
d https://eda.ru/recepty/osnovnye-blyuda/pajelja-s-krevetkami-kuricej-17276
d https://eda.ru/recepty/osnovnye-blyuda/kastrjulja-s-semju-kapustami-15672
d https://eda.ru/recepty/salaty/salat-iz-teljachego-jazika-15681
d https://eda.ru/recepty/osnovnye-blyuda/kurinaja-pechen-s-medovim-lukom-26064
d https://eda.ru/recepty/osnovnye-blyuda/kurica-po-italjanski-31323
d https://eda.ru/recepty/osnovnye-blyuda/gorbusha-zapechennaja-v-folge-31079
d https://eda.ru/recepty/pasta-picca/picca-bez-testa-21471
d https://eda.ru/recepty/zakuski/tushenie-kalmari-19085
d https://eda.ru/recepty/osnovnye-blyuda/zapekanka-s-kurinym-file-ovoschami-i-fasolyu-29964
d https://eda.ru/recepty/osnovnye-blyuda/kurinie-ruletiki-s-gorchichnim-sousom-21721
b https://eda.ru/recepty/zavtraki/omlet-so-shpinatom-15198
b https://eda.ru/recepty/zavtraki/ovsyanka-s-mindalnymi-molokom-114790
b https://eda.ru/recepty/zavtraki/dieticheskaya-grechnevaya-molochnaya-kasha-s-godzhi-91911
b https://eda.ru/recepty/zavtraki/tvorozhnie-sirniki-na-kokosovoj-muke-51553
b https://eda.ru/recepty/zavtraki/syrniki-iz-rikotty-s-yagodami-93108
b https://eda.ru/recepty/zavtraki/sirniki-s-kukuruznoj-mukoj-i-varenem-31209
b https://eda.ru/recepty/vypechka-deserty/blinchiki-iz-otrubej-29844
b https://eda.ru/recepty/zavtraki/jablochnie-mjusli-21739
b https://eda.ru/recepty/zavtraki/zapekanka-iz-jaichnih-belkov-kalmarov-brokkoli-31569
b https://eda.ru/recepty/zavtraki/dieticheskie-pankeyki-bez-sahara-s-shokoladnym-sousom-49305
b https://eda.ru/recepty/zavtraki/ovsjanij-zavtrak-s-zernami-granata-v-banke-53229
b https://eda.ru/recepty/zavtraki/bulochka-s-tvorogom-avokado-27139
b https://eda.ru/recepty/zavtraki/shakshuka-jaichnica-s-pomidorami-52383
b https://eda.ru/recepty/zavtraki/tost-s-avokado-i-rikottoy-79855
b https://eda.ru/recepty/zavtraki/ovsjanij-blin-s-sirom-51919
b https://eda.ru/recepty/zavtraki/nutovo-lnyanye-blinchiki-92229
b https://eda.ru/recepty/zavtraki/zapechennaya-ovsyanka-s-yablokami-i-orehami-68603
b https://eda.ru/recepty/zavtraki/smuzi-v-tarelke-125251
b https://eda.ru/recepty/zavtraki/kuskus-s-mango-i-kokosovymi-slivkami-81340'''


def build_recipes(links):

    recipes = {
        'b': [],
        'l': [],
        'd': [],
        's': []
    }

    code_recipes = {}
    i = 0
    at_all = len(links)
    for rt, link in links:
        time_one = time.time()

        
        i += 1

        recipe = Recipe(recipe_type=abr_rt[rt], link=link, code=i)
        recipes[rt].append(recipe)
        code_recipes[recipe.code] = recipe

        time_one = time.time() - time_one
        print(f'{int(i * 100 / at_all)}% {i} / {at_all}')

    save_pck(recipes['b'], BREAKFASTS_PATH)
    save_pck(recipes['l'], LUNCHS_PATH)
    save_pck(recipes['d'], DINNERS_PATH)
    save_pck(recipes['s'], SNACKES_PATH)

    save_pck(code_recipes, CODE_RECIPES_PATH)

# noty('START!')
# build_recipes(links=load_pck(CAT_REF_EDA_PATH))
# noty('DONE!')

breakfasts = load_pck(BREAKFASTS_PATH)
lunchs = load_pck(LUNCHS_PATH)
dinners = load_pck(DINNERS_PATH)
snackes = load_pck(SNACKES_PATH)

new_breakfasts = []
new_lunchs = []
new_dinners = []
new_snackes = []

p = [
    (breakfasts, new_breakfasts),
    (lunchs, new_lunchs),
    (dinners, new_dinners),
    (snackes, new_snackes),
]
for old, new in p:
    for r in old:
        if r.calories == -1.0 or r.protein == -1.0 or r.fat == -1.0 or r.corb == -1.0:
            continue
        new.append(r)
        
save_pck(new_breakfasts, BREAKFASTS_PATH)
save_pck(new_lunchs, LUNCHS_PATH)
save_pck(new_dinners, DINNERS_PATH)
save_pck(new_snackes, SNACKES_PATH)

# количество порций 
# <span class="info-text js-portions-count-print" itemprop="recipeYield">6 порций</span>

# ингредиенты
# <div class="ingredients-list__content" cellpadding="0" cellspacing="0">
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 14797, &quot;name&quot;: &quot;Темный шоколад&quot;, &quot;amount&quot;: &quot;100 г&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="14797" data-hasqtip="1">
#         Темный шоколад
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="14797">100 г</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13412, &quot;name&quot;: &quot;Сливочное масло&quot;, &quot;amount&quot;: &quot;180 г&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13412" data-hasqtip="2">
#         Сливочное масло
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13412">180 г</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 14339, &quot;name&quot;: &quot;Коричневый сахар&quot;, &quot;amount&quot;: &quot;200 г&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="14339" data-hasqtip="3">
#         Коричневый сахар
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="14339">200 г</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13418, &quot;name&quot;: &quot;Яйцо куриное&quot;, &quot;amount&quot;: &quot;4 штуки&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13418" data-hasqtip="4">
#         Яйцо куриное
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13418">4 штуки</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13458, &quot;name&quot;: &quot;Пшеничная мука&quot;, &quot;amount&quot;: &quot;100 г&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13458" data-hasqtip="5">
#         Пшеничная мука
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13458">100 г</span>
#   </p>
#   <p class="ingredients-list__content-item content-item js-cart-ingredients" data-ingredient-object="{&quot;id&quot;: 13580, &quot;name&quot;: &quot;Грецкие орехи&quot;, &quot;amount&quot;: &quot;100 г&quot;}">
#     <span class="content-item__name tooltip">
#       <span class="js-tooltip js-tooltip-ingredient" data-url="/Ingredient/RecipePreview" data-id="13580" data-hasqtip="6">
#         Грецкие орехи
#       </span>
#     </span>
#     <span class="content-item__measure js-ingredient-measure-amount" data-id="13580">100 г</span>
#   </p>
# </div>


# рецепт
# <ul class="recipe__steps">
#             <li class="instruction clearfix js-steps__parent print-preview" data-counter="1">
#                     <img class="g-print-visible" width="176" src="//img03.rl0.ru/eda/c544x370i/s2.eda.ru/StaticContent/Photos/131113183908/131127174656/p_O.jpg" alt="">
#                     <div class="js-steps" data-index="1">
#                         <div class="instruction__image js-steps__preview print-invisible" data-full-size-src="//s2.eda.ru/StaticContent/Photos/131113183908/131127174656/p_O.jpg">
#                             <div class="lazy-load-container" data-alt="Фото приготовления рецепта: Брауни (brownie) - шаг 1" data-title="Фото приготовления рецепта: Брауни (brownie) - шаг 1" data-src="https://img01.rl0.ru/eda/c434x295i/s2.eda.ru/StaticContent/Photos/131113183908/131127174656/p_O.jpg">
#                                 <svg xmlns="http://www.w3.org/2000/svg" class="js-lazy-loading-svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="434" height="295" viewBox="0 0 434 295">
#                                     <filter id="blur1" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
#                                         <feGaussianBlur stdDeviation="10 10" edgeMode="duplicate"></feGaussianBlur>
#                                         <feComponentTransfer>
#                                             <feFuncA type="discrete" tableValues="1 1"></feFuncA>
#                                         </feComponentTransfer>
#                                     </filter>
#                                     <image filter="url(#blur1)" xlink:href="//img03.rl0.ru/eda/c544x370i/s2.eda.ru/StaticContent/Photos/131113183908/131127174656/p_O.jpg" x="0" y="0" width="100%" height="100%"></image>
#                                 </svg>
#                             <img alt="Фото приготовления рецепта: Брауни (brownie) - шаг 1" title="Фото приготовления рецепта: Брауни (brownie) - шаг 1" src="https://img01.rl0.ru/eda/c434x295i/s2.eda.ru/StaticContent/Photos/131113183908/131127174656/p_O.jpg" class="lazy-load-image --fullwidth"></div>
#                         </div>
#                     </div>
#                 <div class="instruction__wrap">
#                   <span style="white-space: pre-line" class="instruction__description js-steps__description ">
#                     <span>1. </span>Шоколад разломать на кусочки и вместе со сливочным маслом растопить на водяной бане, не переставая все время помешивать лопаткой или деревянной ложкой. Получившийся густой шоколадный соус снять с водяной бани и оставить остывать.
#                   </span>

#                 </div>
                
#             </li>
#             <li class="instruction clearfix js-steps__parent print-preview" data-counter="2">
#                     <img class="g-print-visible" width="176" src="//img06.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/131127174657/p_O.jpg" alt="">
#                     <div class="js-steps" data-index="2">
#                         <div class="instruction__image js-steps__preview print-invisible" data-full-size-src="//s1.eda.ru/StaticContent/Photos/131113183908/131127174657/p_O.jpg">
#                             <div class="lazy-load-container" data-alt="Фото приготовления рецепта: Брауни (brownie) - шаг 2" data-title="Фото приготовления рецепта: Брауни (brownie) - шаг 2" data-src="https://img03.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/131127174657/p_O.jpg">
#                                 <svg xmlns="http://www.w3.org/2000/svg" class="js-lazy-loading-svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="434" height="295" viewBox="0 0 434 295">
#                                     <filter id="blur1" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
#                                         <feGaussianBlur stdDeviation="10 10" edgeMode="duplicate"></feGaussianBlur>
#                                         <feComponentTransfer>
#                                             <feFuncA type="discrete" tableValues="1 1"></feFuncA>
#                                         </feComponentTransfer>
#                                     </filter>
#                                     <image filter="url(#blur1)" xlink:href="//img06.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/131127174657/p_O.jpg" x="0" y="0" width="100%" height="100%"></image>
#                                 </svg>
#                             <img alt="Фото приготовления рецепта: Брауни (brownie) - шаг 2" title="Фото приготовления рецепта: Брауни (brownie) - шаг 2" src="https://img03.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/131127174657/p_O.jpg" class="lazy-load-image --fullwidth"></div>
#                         </div>
#                     </div>
#                 <div class="instruction__wrap">
#                   <span style="white-space: pre-line" class="instruction__description js-steps__description ">
#                     <span>2. </span>Тем временем смешать яйца со ста граммами коричневого сахара: яйца разбить в отдельную миску и взбить, постепенно добавляя сахар. Взбивать можно при помощи миксера или вручную — как больше нравится, — но не меньше двух с половиной-трех минут.
#                   </span>

#                       <span class="linked-content clearfix print-invisible">

#                           <span class="linked-content__image">
#                               <img src="//s2.eda.ru/StaticContent/Photos/110801145258/1205042115583/p_O.jpg" alt="">

#                           </span>
#                           <span class="linked-content__info">
#                               <a href="/wiki/instrumenty/mikser-63" target="_blank" class="linked-content__link">Инструмент</a>
#                               <span class="linked-content__name js-popup-name">Миксер</span>
#                           </span>
#                           <a href="/wiki/instrumenty/mikser-63" target="_blank" class="block-link js-popup-link"></a>
#                           <span class="linked-content__description js-popup-description" data-url="//s1.eda.ru/StaticContent/Photos/120214160714/120304023554/p_O.jpg">Взбивать яичные белки, а также замешивать прочие субстанции вроде фарша или теста удобно не вручную (так как это требует сил и времени), а с помощью миксера вроде KitchenAid. Например, у модели Artisan десять скоростных режимов и три разные насадки для работы с любыми консистенциями, к тому же это одновременно и универсальный кухонный комбайн.</span>
#                       </span>
#                 </div>
                
#             </li>
#             <li class="instruction clearfix js-steps__parent print-preview" data-counter="3">
#                     <img class="g-print-visible" width="176" src="//img08.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/1311271746570/p_O.jpg" alt="">
#                     <div class="js-steps" data-index="3">
#                         <div class="instruction__image js-steps__preview print-invisible" data-full-size-src="//s1.eda.ru/StaticContent/Photos/131113183908/1311271746570/p_O.jpg">
#                             <div class="lazy-load-container" data-alt="Фото приготовления рецепта: Брауни (brownie) - шаг 3" data-title="Фото приготовления рецепта: Брауни (brownie) - шаг 3" data-src="https://img07.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/1311271746570/p_O.jpg">
#                                 <svg xmlns="http://www.w3.org/2000/svg" class="js-lazy-loading-svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="434" height="295" viewBox="0 0 434 295">
#                                     <filter id="blur1" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
#                                         <feGaussianBlur stdDeviation="10 10" edgeMode="duplicate"></feGaussianBlur>
#                                         <feComponentTransfer>
#                                             <feFuncA type="discrete" tableValues="1 1"></feFuncA>
#                                         </feComponentTransfer>
#                                     </filter>
#                                     <image filter="url(#blur1)" xlink:href="//img08.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/1311271746570/p_O.jpg" x="0" y="0" width="100%" height="100%"></image>
#                                 </svg>
#                             <img alt="Фото приготовления рецепта: Брауни (brownie) - шаг 3" title="Фото приготовления рецепта: Брауни (brownie) - шаг 3" src="https://img07.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/1311271746570/p_O.jpg" class="lazy-load-image --fullwidth"></div>
#                         </div>
#                     </div>
#                 <div class="instruction__wrap">
#                   <span style="white-space: pre-line" class="instruction__description js-steps__description ">
#                     <span>3. </span>Острым ножом на разделочной доске порубить грецкие орехи. Предварительно их можно поджарить на сухой сковороде до появления аромата, но это необязательная опция.
#                   </span>

#                       <span class="linked-content clearfix print-invisible">

#                           <span class="linked-content__image">
#                               <img src="//s1.eda.ru/StaticContent/Photos/110801145258/1205042116019/p_O.jpg" alt="">

#                           </span>
#                           <span class="linked-content__info">
#                               <a href="/wiki/instrumenty/nozh-keramicheskij-94" target="_blank" class="linked-content__link">Инструмент</a>
#                               <span class="linked-content__name js-popup-name">Нож керамический</span>
#                           </span>
#                           <a href="/wiki/instrumenty/nozh-keramicheskij-94" target="_blank" class="block-link js-popup-link"></a>
#                           <span class="linked-content__description js-popup-description" data-url="//s1.eda.ru/StaticContent/Photos/120214160714/120304023859/p_O.jpg">Японские керамические ножи делают из оксида циркона — материала, занимающего на шкале твердости место посередине между сталью и алмазом. Притом они легче металлических, не окисляют продукты, не впитывают запахи и не требуют заточки минимум три года. </span>
#                       </span>
#                 </div>
                
#             </li>
#             <li class="instruction clearfix js-steps__parent print-preview" data-counter="4">
#                     <img class="g-print-visible" width="176" src="//img02.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/131127174659/p_O.jpg" alt="">
#                     <div class="js-steps" data-index="4">
#                         <div class="instruction__image js-steps__preview print-invisible" data-full-size-src="//s1.eda.ru/StaticContent/Photos/131113183908/131127174659/p_O.jpg">
#                             <div class="lazy-load-container" data-alt="Фото приготовления рецепта: Брауни (brownie) - шаг 4" data-title="Фото приготовления рецепта: Брауни (brownie) - шаг 4" data-src="https://img05.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/131127174659/p_O.jpg">
#                                 <svg xmlns="http://www.w3.org/2000/svg" class="js-lazy-loading-svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="434" height="295" viewBox="0 0 434 295">
#                                     <filter id="blur1" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
#                                         <feGaussianBlur stdDeviation="10 10" edgeMode="duplicate"></feGaussianBlur>
#                                         <feComponentTransfer>
#                                             <feFuncA type="discrete" tableValues="1 1"></feFuncA>
#                                         </feComponentTransfer>
#                                     </filter>
#                                     <image filter="url(#blur1)" xlink:href="//img02.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/131127174659/p_O.jpg" x="0" y="0" width="100%" height="100%"></image>
#                                 </svg>
#                             <img alt="Фото приготовления рецепта: Брауни (brownie) - шаг 4" title="Фото приготовления рецепта: Брауни (brownie) - шаг 4" src="https://img05.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/131127174659/p_O.jpg" class="lazy-load-image --fullwidth"></div>
#                         </div>
#                     </div>
#                 <div class="instruction__wrap">
#                   <span style="white-space: pre-line" class="instruction__description js-steps__description ">
#                     <span>4. </span>В остывший растопленный со сливочным маслом шоколад аккуратно добавить оставшийся сахар, затем муку и измельченные орехи и все хорошо перемешать венчиком.
#                   </span>

#                 </div>
                
#             </li>
#             <li class="instruction clearfix js-steps__parent print-preview" data-counter="5">
#                     <img class="g-print-visible" width="176" src="//img03.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/1311271746590/p_O.jpg" alt="">
#                     <div class="js-steps" data-index="5">
#                         <div class="instruction__image js-steps__preview print-invisible" data-full-size-src="//s1.eda.ru/StaticContent/Photos/131113183908/1311271746590/p_O.jpg">
#                             <div class="lazy-load-container" data-alt="Фото приготовления рецепта: Брауни (brownie) - шаг 5" data-title="Фото приготовления рецепта: Брауни (brownie) - шаг 5" data-src="https://img05.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/1311271746590/p_O.jpg">
#                                 <svg xmlns="http://www.w3.org/2000/svg" class="js-lazy-loading-svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="434" height="295" viewBox="0 0 434 295">
#                                     <filter id="blur1" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
#                                         <feGaussianBlur stdDeviation="10 10" edgeMode="duplicate"></feGaussianBlur>
#                                         <feComponentTransfer>
#                                             <feFuncA type="discrete" tableValues="1 1"></feFuncA>
#                                         </feComponentTransfer>
#                                     </filter>
#                                     <image filter="url(#blur1)" xlink:href="//img03.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/1311271746590/p_O.jpg" x="0" y="0" width="100%" height="100%"></image>
#                                 </svg>
#                             <img alt="Фото приготовления рецепта: Брауни (brownie) - шаг 5" title="Фото приготовления рецепта: Брауни (brownie) - шаг 5" src="https://img05.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/1311271746590/p_O.jpg" class="lazy-load-image --fullwidth"></div>
#                         </div>
#                     </div>
#                 <div class="instruction__wrap">
#                   <span style="white-space: pre-line" class="instruction__description js-steps__description ">
#                     <span>5. </span>Затем влить сахарно-яичную смесь и тщательно смешать с шоколадной массой. Цвет у теста должен получиться равномерным, без разводов.
#                   </span>

#                 </div>
                
#             </li>
#             <li class="instruction clearfix js-steps__parent print-preview" data-counter="6">
#                     <img class="g-print-visible" width="176" src="//img09.rl0.ru/eda/c544x370i/s2.eda.ru/StaticContent/Photos/131113183908/131127174700/p_O.jpg" alt="">
#                     <div class="js-steps" data-index="6">
#                         <div class="instruction__image js-steps__preview print-invisible" data-full-size-src="//s2.eda.ru/StaticContent/Photos/131113183908/131127174700/p_O.jpg">
#                             <div class="lazy-load-container" data-alt="Фото приготовления рецепта: Брауни (brownie) - шаг 6" data-title="Фото приготовления рецепта: Брауни (brownie) - шаг 6" data-src="https://img07.rl0.ru/eda/c434x295i/s2.eda.ru/StaticContent/Photos/131113183908/131127174700/p_O.jpg">
#                                 <svg xmlns="http://www.w3.org/2000/svg" class="js-lazy-loading-svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="434" height="295" viewBox="0 0 434 295">
#                                     <filter id="blur1" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
#                                         <feGaussianBlur stdDeviation="10 10" edgeMode="duplicate"></feGaussianBlur>
#                                         <feComponentTransfer>
#                                             <feFuncA type="discrete" tableValues="1 1"></feFuncA>
#                                         </feComponentTransfer>
#                                     </filter>
#                                     <image filter="url(#blur1)" xlink:href="//img09.rl0.ru/eda/c544x370i/s2.eda.ru/StaticContent/Photos/131113183908/131127174700/p_O.jpg" x="0" y="0" width="100%" height="100%"></image>
#                                 </svg>
#                             <img alt="Фото приготовления рецепта: Брауни (brownie) - шаг 6" title="Фото приготовления рецепта: Брауни (brownie) - шаг 6" src="https://img07.rl0.ru/eda/c434x295i/s2.eda.ru/StaticContent/Photos/131113183908/131127174700/p_O.jpg" class="lazy-load-image --fullwidth"></div>
#                         </div>
#                     </div>
#                 <div class="instruction__wrap">
#                   <span style="white-space: pre-line" class="instruction__description js-steps__description ">
#                     <span>6. </span>Разогреть духовку до 200 градусов. Дно небольшой глубокой огнеупорной формы выстелить листом бумаги для выпечки или калькой. Перелить тесто в форму. Поставить в духовку и выпекать двадцать пять — тридцать минут до появления сахарной корочки.
#                   </span>

#                       <span class="linked-content clearfix print-invisible">

#                           <span class="linked-content__image">
#                               <img src="//s1.eda.ru/StaticContent/Photos/110801145258/1205042116013/p_O.jpg" alt="">

#                           </span>
#                           <span class="linked-content__info">
#                               <a href="/wiki/instrumenty/termometr-dlja-duhovki-89" target="_blank" class="linked-content__link">Инструмент</a>
#                               <span class="linked-content__name js-popup-name">Термометр для духовки</span>
#                           </span>
#                           <a href="/wiki/instrumenty/termometr-dlja-duhovki-89" target="_blank" class="block-link js-popup-link"></a>
#                           <span class="linked-content__description js-popup-description" data-url="//s1.eda.ru/StaticContent/Photos/110825150222/120304025725/p_O.jpg">Как на самом деле разогревается духовка, даже если устанавливаешь конкретную температуру, понять можно только с опытом. Лучше иметь под рукой маленький градусник, который ставится в духовой шкаф или просто вешается на решетку. И лучше, чтобы он показывал градусы по Цельсию и Фаренгейту одновременно и точно — как швейцарские часы. Термометр важен, когда надо строго соблюдать температурный режим: скажем, в случае выпечки. </span>
#                       </span>
#                 </div>
                
#             </li>
#             <li class="instruction clearfix js-steps__parent print-preview" data-counter="7">
#                     <img class="g-print-visible" width="176" src="//img05.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/131127174701/p_O.jpg" alt="">
#                     <div class="js-steps" data-index="7">
#                         <div class="instruction__image js-steps__preview print-invisible" data-full-size-src="//s1.eda.ru/StaticContent/Photos/131113183908/131127174701/p_O.jpg">
#                             <div class="lazy-load-container" data-alt="Фото приготовления рецепта: Брауни (brownie) - шаг 7" data-title="Фото приготовления рецепта: Брауни (brownie) - шаг 7" data-src="https://img01.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/131127174701/p_O.jpg">
#                                 <svg xmlns="http://www.w3.org/2000/svg" class="js-lazy-loading-svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="434" height="295" viewBox="0 0 434 295">
#                                     <filter id="blur1" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
#                                         <feGaussianBlur stdDeviation="10 10" edgeMode="duplicate"></feGaussianBlur>
#                                         <feComponentTransfer>
#                                             <feFuncA type="discrete" tableValues="1 1"></feFuncA>
#                                         </feComponentTransfer>
#                                     </filter>
#                                     <image filter="url(#blur1)" xlink:href="//img05.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/131127174701/p_O.jpg" x="0" y="0" width="100%" height="100%"></image>
#                                 </svg>
#                             <img alt="Фото приготовления рецепта: Брауни (brownie) - шаг 7" title="Фото приготовления рецепта: Брауни (brownie) - шаг 7" src="https://img01.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/131127174701/p_O.jpg" class="lazy-load-image --fullwidth"></div>
#                         </div>
#                     </div>
#                 <div class="instruction__wrap">
#                   <span style="white-space: pre-line" class="instruction__description js-steps__description ">
#                     <span>7. </span>Готовый пирог вытащить из духовки, дать остыть и нарезать на квадратики острым ножом или ножом для пиццы — так кусочки получатся особенно ровными.
#                   </span>

#                 </div>
                
#             </li>
#             <li class="instruction clearfix js-steps__parent print-preview" data-counter="8">
#                     <img class="g-print-visible" width="176" src="//img06.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/1311271747010/p_O.jpg" alt="">
#                     <div class="js-steps" data-index="8">
#                         <div class="instruction__image js-steps__preview print-invisible" data-full-size-src="//s1.eda.ru/StaticContent/Photos/131113183908/1311271747010/p_O.jpg">
#                             <div class="lazy-load-container" data-alt="Фото приготовления рецепта: Брауни (brownie) - шаг 8" data-title="Фото приготовления рецепта: Брауни (brownie) - шаг 8" data-src="https://img07.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/1311271747010/p_O.jpg">
#                                 <svg xmlns="http://www.w3.org/2000/svg" class="js-lazy-loading-svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="434" height="295" viewBox="0 0 434 295">
#                                     <filter id="blur1" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
#                                         <feGaussianBlur stdDeviation="10 10" edgeMode="duplicate"></feGaussianBlur>
#                                         <feComponentTransfer>
#                                             <feFuncA type="discrete" tableValues="1 1"></feFuncA>
#                                         </feComponentTransfer>
#                                     </filter>
#                                     <image filter="url(#blur1)" xlink:href="//img06.rl0.ru/eda/c544x370i/s1.eda.ru/StaticContent/Photos/131113183908/1311271747010/p_O.jpg" x="0" y="0" width="100%" height="100%"></image>
#                                 </svg>
#                             <img alt="Фото приготовления рецепта: Брауни (brownie) - шаг 8" title="Фото приготовления рецепта: Брауни (brownie) - шаг 8" src="https://img07.rl0.ru/eda/c434x295i/s1.eda.ru/StaticContent/Photos/131113183908/1311271747010/p_O.jpg" class="lazy-load-image --fullwidth"></div>
#                         </div>
#                     </div>
#                 <div class="instruction__wrap">
#                   <span style="white-space: pre-line" class="instruction__description js-steps__description ">
#                     <span>8. </span>Подавать брауни можно просто так, а можно посыпать сверху сахарной пудрой или разложить квадратики по тарелкам и украсить каждую порцию  шариком ванильного мороженого.
#                   </span>

#                 </div>
                
#             </li>
#     </ul>


