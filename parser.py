# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

def parse(resp):
    #f = open(path, 'r', encoding='cp1251')
    soup = BeautifulSoup(resp.text, 'html.parser') #.text
    #msg_text = soup.find_all("div", class_="messageText")
    msg_text = soup.find_all("div", class_="messageText")
    #print(msg_text)
    msgs = []
    msgs = [x.find_all("p") for x in msg_text]
    #print(msgs)
    #exit(0)
    msg_answ = soup.find_all("p", class_="of-green")
    msg_theme = soup.find_all("div", class_="themeText bold")
    #print(msg_answ)
    print(msg_theme)
    #exit(0)
    inner_theme = [x.text for x in msg_theme]
    for i in range (0, len(inner_theme)):
        inner_theme[i] = inner_theme[i].replace('   ', '')        
        inner_theme[i] = inner_theme[i].replace('\n', ' ')
        inner_theme[i] = inner_theme[i].replace('  ', ' ')
        inner_theme[i] = inner_theme[i].strip()
    final_text = []
    print(str(msgs[1]))
    #exit(0)
    for i in range(0, len(msgs)):
        tmp = str(msgs[i])
        print(tmp)
        tmp = tmp.replace('[<p>', '')
        tmp = tmp.replace('</p>]', '')
        tmp = tmp.replace('\n', ' ')
        tmp = tmp.replace('  ', ' ')
        final_text.append(tmp)
    #print(final_text, len(final_text))
    #print(msg_theme)
    #print(inner_text , len(inner_text))
    #file_contents = f.read()
    #print(file_contents)
    return inner_theme, final_text

def main():
    res_data  = pd.DataFrame(columns = ['Локальная тема', 'Описание'])   
    for i in range(1, 6):
        q = str(i)
        print(i)
        if i != 0:
            add='&page='+q
        else:
            add=''
        resp = requests.get('https://gorod.mos.ru/?show=problem&id_theme=4'+add)
        #resp = open('C:/Users/user/Documents/programs/hackaton/qwa.html')
        #print(resp.text)
        #exit(0)
        res_theme, res_text = parse(resp)
        temp_data = pd.DataFrame(columns = ['Локальная тема', 'Описание'])
        temp_data['Локальная тема'] = res_theme
        temp_data['Описание'] = res_text
        res_data = pd.concat([res_data, temp_data], ignore_index=True)
    print(res_data)
    res_data.to_csv('C:/Users/user/Documents/programs/hackaton/medical_v2.csv', sep=';', encoding='cp1251')
    print('\n\n\n\n\n\n\n\n\n\n')
    return 0

if __name__=="__main__":
    main()