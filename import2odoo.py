# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys, csv
import hashlib


# header = ['PO', 'Date', 'Nom', 'Prenom', 'CP', 'Ville', 'Pays','UID']
# header = ['id', 'child_ids/stripe_checkout_customer_id', 'child_ids/date', 'child_ids/name', 'child_ids/firstname',
# 'child_ids/zip', 'child_ids/city', 'child_ids/country_id/id','child_ids/ref']

def slowCosmetiqueImport2odoo(fcmd, ftxt, fres='res.csv', header=None):
    country = {'France': 'base.fr', 'Belgique': 'base.be', 'Allemagne': 'base.de', 'Italie': 'base.it',
               'Esapgne': 'base.es', 'Monaco': 'base.mc'}
    header = header if header is not None else ['id', 'child_ids/stripe_checkout_customer_id', 'child_ids/date',
                                                'child_ids/name', 'child_ids/firstname', 'child_ids/zip',
                                                'child_ids/city', 'child_ids/country_id/id','child_ids/ref']
    cmd_cli = {}

    with open(fcmd, newline='') as in_csvfile:
        reader = csv.DictReader(in_csvfile, delimiter=';', quotechar='"')
        po_key = reader.fieldnames[0]
        po_list = [row[po_key] for row in reader]
        in_csvfile.close()
    po_list.sort(reverse=True)
    # print(po_list)

    with open(fres, 'w', newline='') as out_csvfile:
        o_write = csv.writer(out_csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        o_write.writerow(header)
        print(header)
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
                    ville = '-'.join(line_split[1:-1])
                    pays = line.split('(')[1].split(')')[0]
                    # match = re.search(r'\(.*?\)', line) ; match.group(0)[1:-1] if match else ""
                    cmd_cli[cur_po].append(first)  # CP
                    cmd_cli[cur_po].append('-'.join(line_split[1:-1]))  # ville
                    cmd_cli[cur_po].append(country[line.split('(')[1].split(')')[0]])  # base.xx[pays]
                    key = ''.join(cmd_cli[cur_po][2] + cmd_cli[cur_po][3] + line_split[0] + line_split[1] + line_split[2])
                    cmd_cli[cur_po].append(hashlib.md5(key.encode('utf-8')).hexdigest())
                    # cmd_line = '"' + '";"'.join(cmd_cli[cur_po]) + '"'
                    print(cmd_cli[cur_po])
                    o_write.writerow(cmd_cli[cur_po])
                    address, newcmd = False, False
        f2chk.close()
    out_csvfile.close()
    print('*' * 30 + 'DONE' + "*" * 30)


if __name__ == '__main__':
    # print(sys.argv)
    slowCosmetiqueImport2odoo(sys.argv[1], sys.argv[2], sys.argv[2].split('.')[:-1][0] + '_res.csv' )
    # print("if yes")
else:
    slowCosmetiqueImport2odoo('slow/commandes_2019.csv','slow/commandes_slow-cosmetiques.txt')
    # print("if no")

