# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os, shutil, re
import sys, csv
import hashlib
from datetime import date, time, datetime, timedelta

def main(fcmd, ftxt, fres='res.csv'):
    country = {'France': 'base.fr', 'Belgique': 'base.be', 'Allemagne': 'base.de', 'Italie': 'base.it',
               'Esapgne': 'base.es', 'Monaco': 'base.mc'}
    with open(fcmd, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        po_key = reader.fieldnames[0]
        po_list = [row[po_key] for row in reader]
    po_list.sort(reverse=True)
    cmd_cli = {}
    print(po_list)
    with open(fres, 'w') as fres:
        # header = '"' + '";"'.join(['PO', 'Date', 'Nom', 'Prenom', 'CP', 'Ville', 'Pays','UID']) + '"\n'
        # "id","name","stripe_checkout_customer_id","child_ids/id","child_ids/name","child_ids/firstname","child_ids/city","child_ids/zip","child_ids/country_id/id"
        # id	name
        #
        header = '"' + '";"'.join(['id', 'child_ids/stripe_checkout_customer_id', 'child_ids/date', 'child_ids/name', 'child_ids/firstname', 'child_ids/zip', 'child_ids/city', 'child_ids/country_id/id','child_ids/ref']) + '"\n'
        fres.write(header)
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
                    cmd_cli[cur_po] = ['__export__.res_partner_1324_ccf30abe', cur_po]
                    cmd_cli[cur_po].append(line_split[2])
                if newcmd and first == 'Client':
                    name = True
                elif newcmd and name:
                    cmd_cli[cur_po].append(line_split[1])
                    cmd_cli[cur_po].append(line_split[0])
                    name, address = False, True
                elif newcmd and address:
                    lp_par = line.split('(')
                    pays = lp_par[1].split(')')[0]
                    cp = first
                    ville = '-'.join(lp_par[0].split(' ')[1:])[:-1]
                    cmd_cli[cur_po].append(cp)  # le CP
                    cmd_cli[cur_po].append(ville)
                    cmd_cli[cur_po].append(country[pays])
                    # cmd_cli[cur_po].append(line_split[0])  # le CP
                    # cmd_cli[cur_po].append(line_split[1])
                    # cmd_cli[cur_po].append(line_split[2][1:-1])
                    address, newcmd = False, False
                    key = ''.join(cmd_cli[cur_po][2] + cmd_cli[cur_po][3] + line_split[0] + line_split[1] + line_split[2])
                    cmd_cli[cur_po].append(hashlib.md5(key.encode('utf-8')).hexdigest())
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
