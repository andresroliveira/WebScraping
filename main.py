from email import charset
import pandas as pd
import json
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_soudtrack_list(URL):
    with urlopen(URL) as f:
        web_string = f.read().decode("UTF-8")

    soup = BeautifulSoup(web_string, 'html.parser')

    cont = soup.find("div", class_='post-content')

    itens = list(list(cont.children)[2].children)

    # print(len(itens))

    dic = {}
    music_number = 0

    for i in range(1, len(itens)):
        structure = str(itens[i]).split('<br/>')
        if structure != ['', '']:
            if structure[0].find('<i>') == -1:
                music_number += 1

                structure = structure[0].split('.')[1]
                # print(structure)
                name = structure.split(' – ')[0]
                composer = structure.split(' – ')[1]
                # print(music_number, name, composer)
                dic[music_number] = {
                    "name": name.strip(),
                    "composer": composer.strip(),
                    "obs": ''
                }
            else:
                # print(structure[0])
                obs = re.search('<i>\((.*)\)</i>', structure[0]).group(1)
                # print(obs)
                dic[music_number]["obs"] = obs.strip()

    return dic


URL = [
    "http://teledramaturgia.com.br/olhai-os-lirios-do-campo-trilha-sonora/",
    "http://teledramaturgia.com.br/agua-viva-trilha-nacional/",
    "http://teledramaturgia.com.br/chega-mais-trilha-internacional/"
]

for url in URL:
    dic = get_soudtrack_list(url)
    f = open(url.split('/')[3] + '.json', 'w', encoding='UTF-8')
    json.dump(dic, f, indent=4, ensure_ascii=False)
    f.close()