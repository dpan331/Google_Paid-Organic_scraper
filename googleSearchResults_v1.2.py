"""
created by Dimitrios Panourgias
June 2020

This script does not by any means aim
to cause any harm to the online source
that uses to scrap data. It is drafted
only for educational purposes
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re

# Read query list from csv
productCSV = pd.read_csv('./productQueryList.csv', header=None)
productList = productCSV[0].tolist()

driver = webdriver.Chrome('C:/Users/dimpa/Downloads/chromedriver.exe')
dataTable = pd.DataFrame(columns=['product_name', 'ad', 'organic', 'my_shop', 'ad_index', 'org_index'])

"""
Provide your shop's name
"""
my_shop = 'tofarmakeiomou'

def googleSearch(query, shop, ad_index, org_index, df):
    df_add = pd.DataFrame(columns=['product_name', 'ad', 'organic', 'my_shop', 'ad_index', 'org_index'])
    search_bar = driver.find_element(By.NAME, 'q')
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(5)
    ady = driver.find_elements(By.CLASS_NAME, 'ads-visurl')
    organicy = driver.find_elements(By.CLASS_NAME, 'rc')
    for y in range(0, len(ady)):
        if (re.findall(r'\d+', ady[y].text) != []) or (ady[y].text == ""):
            # get rid off shop's telephone number or white space
            print(query + ' || ' + ady[y].text + ' >> dropped')
            continue
        else:
            ad_index += 1
            if (shop or shop.capitalize()) in ady[y].text:
                df_add = df_add.append({'product_name': query,
                                        'ad': ady[y].text,
                                        'organic': 'n/a',
                                        'my_shop': 'ad_yes',
                                        'ad_index': ad_index,
                                        'org_index': 'n/a'},
                                        ignore_index=True)
                print(query + ' || ' + ady[y].text)
            else:
                df_add = df_add.append({'product_name': query,
                                        'ad': ady[y].text,
                                        'organic': 'n/a',
                                        'my_shop': 'ad_no',
                                        'ad_index': 'n/a',
                                        'org_index': 'n/a'},
                                       ignore_index=True)
                print(query + ' || ' + ady[y].text)
    for z in range(0, len(organicy)):
        org_index += 1
        if (shop or shop.capitalize()) in organicy[z].text:
            df_add = df_add.append({'product_name': query,
                                    'ad': 'n/a',
                                    'organic': organicy[z].text,
                                    'my_shop': 'organic_yes',
                                    'ad_index': 'n/a',
                                    'org_index': org_index},
                                    ignore_index=True)
        else:
            df_add = df_add.append({'product_name': query,
                                    'ad': 'n/a',
                                    'organic': organicy[z].text,
                                    'my_shop': 'organic_no',
                                    'ad_index': 'n/a',
                                    'org_index': 'n/a'},
                                   ignore_index=True)
    df = pd.concat([df, df_add], axis=0, ignore_index=True)
    return df


i = 0
for x in productList:
    driver.get('https://www.google.com/')
    time.sleep(5)
    ad_ind = 0
    org_ind = 0
    if i == 0:
        endResult = googleSearch(x, my_shop, ad_ind, org_ind, dataTable)
        i += 1
    else:
        endResult = googleSearch(x, my_shop, ad_ind, org_ind, endResult)
        i += 1

endResult.to_csv('adsOrganicResultsList.csv')
driver.quit()

