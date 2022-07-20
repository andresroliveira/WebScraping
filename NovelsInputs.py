from bs4 import BeautifulSoup
from urllib.request import urlopen


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
        tv = list(cont.find('p'))[0].split(' – ')[0].strip()
        time = list(cont.find('p'))[0].split(' – ')[1].strip()
    except IndexError as e:
        tv = cont.contents[0].split(' – ')[0].strip()
        time = cont.contents[0].split(' – ')[1].strip()

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

    return [novel, ty, tv, time]


def main():
    ls_85_89 = get_ids_urls(
        "http://teledramaturgia.com.br/trilhas-sonoras-globo-1985-a-1989/")

    for novel, ty, url in ls_85_89:
        print(get_info(novel, ty, url.split('-trilha-')[0] + '/'))


if __name__ == '__main__':
    main()