from pyquery import PyQuery as pq
import re

QUERY_URL = 'https://arxiv.org/search/advanced?advanced=&terms-0-term=SUSY&terms-0-operator=AND&terms-0-field=all&classification-physics=y&classification-physics_archives=hep-ph&date-filter_by=specific_year&date-year=%d&abstracts=show&size=200'

def get_absts(year):
    d = pq(url=QUERY_URL % year)
    absts = [pq(el).text() for el in d('span.abstract-full')]
    return absts

def take_avg(ns):
    if ns[2]:
        return (float(ns[0]) + float(ns[2])) / 2.0
    else:
        return float(ns[0])

REGEV = re.compile(r'[^\^\d]+(\d+(\.\d+)?)[^a-zA-Z0-9\}\.\^]*(\d+(\.\d+)?)?[^\}A-Z0-9\.]*GeV')
RETEV = re.compile(r'[^\^\d]+(\d+(\.\d+)?)[^a-zA-Z0-9\}\.\^]*(\d+(\.\d+)?)?[^\}A-Z0-9\.]*TeV')
def extract_energies(abst):
    gevs = [take_avg(gev) for gev in REGEV.findall(abst)]
    tevs = [take_avg(tev) * 1000. for tev in RETEV.findall(abst)]
    return gevs + tevs


ENERGY_BLACKLIST = [7000.0, 8000.0, 7500.0, 13000.0, 14000.0, 13500.0, 100000.0, 750.0, 125.0, 126.0, 125.5]
LEP_ENERGY = 200
def filter_energy(e):
    return 2 * e > LEP_ENERGY and all(be != e for be in ENERGY_BLACKLIST)


def energies(year):
    absts = get_absts(year)
    ess = [extract_energies(abst) for abst in absts]
    efss = [[e for e in es if filter_energy(e)] for es in ess]

    return efss


def energy_avg(year):
    ess = energies(year)
    es = sum(ess, [])
    e = sum(es) / len(es)
    return e

def main():
    eas = [energy_avg(y) for y in range(1992, 2019)]
    print(eas)


if __name__ == '__main__':
    main()

