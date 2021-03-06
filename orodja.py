import csv
import os
import requests
import sys
import re


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {}...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf8') as datoteka:
        datoteka.write(r.text)
        print('shranjeno!')


def shrani_stran(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {}...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf8') as datoteka:
        datoteka.write(r.text)
        print('shranjeno!')


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf8') as datoteka:
        vsebina = datoteka.read()
    return vsebina


def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]


def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf8', newline='') as csv_dat:  # newline je zato da ni vmes praznih vrstic
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj,
                                delimiter=';')  # delimiter pove po čem ločujem namesto vejice
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


def pocisti_niz(niz):
    v_znacki = False
    nov_niz = ''
    for x in niz:
        if x == '<':
            v_znacki = True
        elif x == '>':
            v_znacki = False
            if nov_niz != '' and nov_niz[-1] != ' ':
                nov_niz += ' '
        elif x == ' ':
            if nov_niz != '' and nov_niz[-1] != ' ':
                nov_niz += x
        else:
            if not v_znacki:
                nov_niz += x
    return nov_niz.strip() # strip odstrani začetne in končne presledke
