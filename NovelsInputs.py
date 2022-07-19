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
        # print('a: ', a)
        # print(type(a))
        url = a.attrs['href']
        novel = a.contents[0].split('trilha')[0].strip()
        ty = a.contents[0].split('trilha')[1].strip()
        ls.append([novel, ty, url])

    return ls


def get_info(novel: str, URL: str):
    print(novel, URL)

    with urlopen(URL) as f:
        web_string = f.read().decode("UTF-8")

    soup = BeautifulSoup(web_string, 'html.parser')
    cont = list(soup.find_all('div', class_='content-container'))

    for c in cont:
        print(c)

    print()


def main():
    ls_85_89 = get_ids_urls(
        "http://teledramaturgia.com.br/trilhas-sonoras-globo-1985-a-1989/")

    for novel, ty, url in ls_85_89[2:8]:
        get_info(novel, url.split('-trilha-')[0] + '/')


if __name__ == '__main__':
    main()