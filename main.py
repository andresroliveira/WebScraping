# http://teledramaturgia.com.br/trilhas-sonoras-globo-1980-a-1984/

import pandas as pd
import json
from SoundtrackList import get_soudtrack_list


def main():
    with open('inputs/novelas_1985_1989.json', encoding="UTF-8") as file:
        data = json.load(file)

    for d in data:  # get all form data
        # for d in list(data)[-4:]:  # get the las t 4 in data
        print(d)
        url = data[d]['URL']
        novel = data[d]['novel']
        year_start = data[d]['year_start']
        year_end = data[d]['year_end']
        time = data[d]['time']
        tv = data[d]['TV']
        d = ''.join(filter(str.isalnum, d))

        dic = get_soudtrack_list(url, novel, year_start, year_end, time, tv)

        df = pd.DataFrame.from_dict(dic)
        df.to_csv('outputs/' + d + '.csv', index=False)
        f = open('outputs/' + d + '.json', 'w', encoding='UTF-8')
        json.dump(dic, f, indent=4, ensure_ascii=False)
        f.close()


if __name__ == "__main__":
    main()