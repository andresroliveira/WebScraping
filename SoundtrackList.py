import re
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_soudtrack_list(URL: str, novel: str, year_star: int, year_end: int,
                       time: str, tv: str):
    with urlopen(URL) as f:
        web_string = f.read().decode("UTF-8")

    soup = BeautifulSoup(web_string, 'html.parser')

    cont = soup.find("div", class_='post-content')

    itens = list(list(cont.children)[2].children)

    dic = {
        'novel': [],
        'year_star': [],
        'year_end': [],
        'time': [],
        'TV': [],
        'name_music': [],
        'artist_music': [],
        'obs': []
    }
    music_number = -1

    for i in range(1, len(itens)):
        structure = str(itens[i]).split('<br/>')
        if structure != ['', '']:
            if structure[0].find('<i>') == -1:
                music_number += 1
                structure = structure[0].split('.')[1]
                name = structure.split(' – ')[0]
                artist = structure.split(' – ')[1]
                dic['novel'].append(novel.strip())
                dic['year_star'].append(year_star)
                dic['year_end'].append(year_end)
                dic['time'].append(time.strip())
                dic['TV'].append(tv.strip())
                dic['name_music'].append(name.strip())
                dic['artist_music'].append(artist.strip())
                dic['obs'].append('')
            else:
                obs = re.search('<i>\((.*)\)</i>', structure[0]).group(1)
                dic['obs'][music_number] = obs.strip()

    return dic
