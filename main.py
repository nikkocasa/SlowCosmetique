# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os, shutil, re
import sys, csv
from datetime import date, time, datetime, timedelta

def main(fcmd, ftxt, fres='res.csv'):
    with open(fcmd, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        po_key = reader.fieldnames[0]
        po_list = [row[po_key] for row in reader]
    po_list.sort(reverse=True)
    cmd_cli = {}
    print(po_list)
    with open(fres, 'w') as fres:
        hearder = '"' + '";"'.join(['PO', 'Date', 'Nom', 'Prenom', 'CP', 'Ville', 'Pays']) + '"\n'
        fres.write(hearder)
        with open(ftxt, 'r') as f2chk:
            newcmd, name, address = False, False, False
            cur_po = ''
            for line in f2chk:
                line = line[:-1] if (len(line) > 1 and ord(line[-1]) == 10) else line
                line_split = [item for sub in [el.split('\t') for el in line.split(' ')] for item in sub]
                first = line_split[0]
                if first in po_list:
                    newcmd = True
                    cur_po = first
                    cmd_cli[cur_po] = [cur_po]
                    cmd_cli[cur_po].append(line_split[2])
                if newcmd and first == 'Client':
                    name = True
                elif newcmd and name:
                    cmd_cli[cur_po].append(line_split[1])
                    cmd_cli[cur_po].append(line_split[0])
                    name, address = False, True
                elif newcmd and address:
                    cmd_cli[cur_po].append(line_split[0])
                    cmd_cli[cur_po].append(line_split[1])
                    cmd_cli[cur_po].append(line_split[2][1:-1])
                    address, newcmd = False, False
                    cmd_line = '"' + '";"'.join(cmd_cli[cur_po]) + '"'
                    print(cmd_line)
                    fres.write(cmd_line + '\n')
        f2chk.close()
    fres.close()
    print('*' * 30 + 'DONE' + "*" * 30)





if __name__ != '__main__':
    main(sys.argv[2], sys.argv[3], sys.argv[3].split('.')[:-1] + '_res.csv' )
else:
    main('commandes_2019.csv','commandes_slow-cosmetiques.txt')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
