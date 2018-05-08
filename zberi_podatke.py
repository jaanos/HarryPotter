import requests
import re
import orodja
from delamo_csv import slovar_url_avtorjev, slovar_url_serij
from delamo_csv_serija import urlji_knjig_iz_serij

vzorec_linka = re.compile("""<td width="100%" valign="top">\s*?<a class="bookTitle" itemprop="url" href="(?P<link_knjige>.*?)">\s*?<span itemprop='name'>(?P<naslov>.*?)</span>\s*?</a>\s*?<br/>\s*?<span class='by smallText'>by</span>""")

def zajemi_knjige():
    """Iz spletnega seznama "What to read after Harry Potter" zajamemo url-je vseh knjig na sznamu.
    Seznam je trenutno dolg 15 strani."""
    for stran in range(1, 2):
        r = requests.get('https://www.goodreads.com/list/show/559.What_To_Read_After_Harry_Potter?page={}'.format(stran))
        page_source = r.text
        linki = [] # tu se nabirajo vsi linki do spletnih strani, ki jih moramo prebrati.
        for zadetek in re.finditer(vzorec_linka, page_source):
            # če je v naslovu dvopičje, pride do napake,
            if ':' in zadetek.groupdict()['naslov']:
                popravljen_naslov = zadetek.groupdict()['naslov']
                linki += [('https://www.goodreads.com' + zadetek.groupdict()['link_knjige'], popravljen_naslov.replace(':','-'))]
            #če je v naslovu slash pride do napake
            elif '/' in zadetek.groupdict()['naslov']:
                popravljen_naslov = zadetek.groupdict()['naslov']
                ###TODO če ima obe napaki, se nama bo naslov dvakrat vnesel v seznam
                linki += [('https://www.goodreads.com' + zadetek.groupdict()['link_knjige'], popravljen_naslov.replace('/','-'))] ###pazit morva da če ima serija 2 imeni jih ločiva
            else:
                linki += [('https://www.goodreads.com' + zadetek.groupdict()['link_knjige'], zadetek.groupdict()['naslov'])]
        for link in linki:
            # Vse html datoteke shranimo v mapo knjige
            orodja.shrani_stran(link[0], 'knjige/{}.html'.format(link[1]))
# TODO: Na git ne smeva nalagat stvari ki se same generirajo => v končni verziji ne smeva mape knjige gor loadat i guess??

def zajemi_avtorje(): ###TODO za nekatere strani piše not found (6244,8164) - neka čudna napaka, jst sm še enkrat probala in zdej dela, pa nism nč popravlala
    for avtor in slovar_url_avtorjev.items():
        print(avtor)
        orodja.shrani_stran(avtor[1], 'avtorji/{}.html'.format(avtor[0]))

def zajemi_serije():
    for serija in slovar_url_serij.items():
        print(serija)
        orodja.shrani_stran('https://www.goodreads.com' + serija[1], 'serije/{}.html'.format(serija[0]))

def zajemi_dodatne_knjige():
    for knjiga in urlji_knjig_iz_serij:
        print(knjiga)
        orodja.shrani_stran('https://www.goodreads.com' + knjiga[0], 'knjige/dodatne/{}.html'.format(knjiga[1])) # tko bova laži vedle kere so ble naknadno