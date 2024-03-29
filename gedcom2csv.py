#!/usr/bin/env python3

import sys

from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

def formatGedcomDate(date_string):
    return (date_string.lower()
            .replace('abt abt', 'abt')
            .replace('abt', 'ca.')
            .replace('bef bef', 'bef')
            .replace('bef ', 'before ')
            .replace('aft aft', 'aft')
            .replace('aft ', 'after')
            .replace('bet', '')
            .replace('and', '-')
            .replace('jan', 'Jan')
            .replace('feb', 'Feb')
            .replace('mar', 'Mar')
            .replace('apr', 'Apr')
            .replace('may', 'May')
            .replace('jun', 'Jun')
            .replace('jul', 'Jul')
            .replace('aug', 'Aug')
            .replace('sep', 'Sep')
            .replace('oct', 'Oct')
            .replace('nov', 'Nov')
            .replace('dec', 'Dec'))

def get_titles(element):
    titles = []

    if not element.is_individual():
        return titles

    for child in element.get_child_elements():
        if child.get_tag() == 'NOBI':
            titles.append(child.get_value())

    return titles

try: infile_path = sys.argv[1]
except IndexError: sys.exit("No gedcom defined!")

outfile_path = infile_path + '.csv'

gedcom_parser = Parser()

gedcom_parser.parse_file(infile_path)

root_child_elements = gedcom_parser.get_root_child_elements()

outfile_contents = []

outfile_contents.append(','.join(["id", "name", "gender", "birth date", "birth place", "death date", "place of death", "title"]))

for element in root_child_elements:

    if isinstance(element, IndividualElement):

        row = []

        name = element.get_name()

        if name[0] == 'Unnamed':
            continue

        record_id = element.get_pointer().replace('@', '').lower()

        row.append(record_id)
        row.append(' '.join(filter(None, name)))

        gender = element.get_gender()

        row.append(gender)

        birth_data = element.get_birth_data()

        row.append(formatGedcomDate(birth_data[0]))
        if birth_data[1] and birth_data[1].strip():
            row.append(format("\"%s\"" % birth_data[1]))
        else:
            row.append('')

        death_data = element.get_death_data()

        row.append(formatGedcomDate(death_data[0]))
        if death_data[1] and death_data[1].strip():
            row.append(format("\"%s\"" % death_data[1]))
        else:
            row.append('')

        titles = get_titles(element)
        titles_str = ','.join(filter(None, titles))
        if titles_str and titles_str.strip():
            row.append(format("\"%s\"" % titles_str))
        else:
            row.append('')

        outfile_contents.append(','.join(row))

#print('\n'.join(outfile_contents))

with open(outfile_path, 'w') as f:
    f.write('\n'.join(outfile_contents))
