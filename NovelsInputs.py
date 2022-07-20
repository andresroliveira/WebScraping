import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def get_ids_urls(URL: str):
    with urlopen(URL) as f:
        web_string = f.read().decode("UTF-8")

    soup = BeautifulSoup(web_string, 'html.parser')
    cont = list(soup.find_all("h4", class_='entry-title'))

    ls = []

    for c in cont:
        a = c.find('a')
        url = a.attrs['href']
        novel = a.contents[0].split('trilha')[0].strip()
        ty = a.contents[0].split('trilha')[1].strip()
        ls.append([novel, ty, url])

    return ls


def get_info(novel: str, ty, URL: str):
    with urlopen(URL) as f:
        web_string = f.read().decode("UTF-8")

    soup = BeautifulSoup(web_string, 'html.parser')
    cont = list(soup.find_all('div', class_='content-container'))[0]

    try:
        info = list(cont.find('p'))
        tv = info[0].split(' – ')[0].strip()
        time = info[0].split(' – ')[1].strip()

        info = info[2:]
    except IndexError as e:
        tv = cont.contents[0].split(' – ')[0].strip()
        time = cont.contents[0].split(' – ')[1].strip()

        info = cont.contents[2:]

    year = []

    for i in info:
        if not isinstance(i, str):
            continue
        if i == '\n' or i == '' or i.find('capítulos') >= 0 or i.find(
                '<p>') >= 0:
            break

        nums = [n for n in map(int, re.findall('[0-9]+', i)) if n > 1950]
        for n in nums:
            year.append(n)

        if len(year) >= 2:
            break

    if len(year) == 0:
        year.append(0)
    if len(year) == 1:
        year.append(year[0])
    year = sorted(year)

    if ty.find('internacional') >= 0:
        ty = 'Internacional'
    elif ty.find('nacional') >= 0:
        ty = 'Nacional'
    elif ty.find('sonora') >= 0:
        ty = ty.split('sonora')[1].strip()
        if ty != '':
            ty = list(ty)
            ty[0] = ty[0].upper()
            ty = ''.join(ty)

    return novel, ty, year[0], year[1], tv, time


def main():
    ls_85_89 = get_ids_urls(
        "http://teledramaturgia.com.br/trilhas-sonoras-globo-1985-a-1989/")

    dic = {}
    for novel, ty, url in ls_85_89:
        novel, ty, year_start, year_end, tv, time = get_info(
            novel, ty,
            url.split('-trilha-')[0] + '/')
        # print(get_info(novel, ty, url.split('-trilha-')[0] + '/'))

        d = {}
        d['URL'] = url
        d['novel'] = novel
        d['year_start'] = year_start
        d['year_end'] = year_end
        d['TV'] = tv
        d['time'] = time
        dic[novel + ' ' + ty] = d

    f = open('inputs/novelas_1985_1989.json', 'w', encoding='UTF-8')
    json.dump(dic, f, ensure_ascii=False, indent=4)
    f.close()


if __name__ == '__main__':
    main()