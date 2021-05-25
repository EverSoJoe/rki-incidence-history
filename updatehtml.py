import datetime
import requests
import tempfile
import urllib.parse

import openpyxl

filtered = True
filter = [9777,9190,9762, 9763,9780]

def getrkixlsx(url, path):
    file = '%s/inzidenzen.xlsx' %(path)
    r = requests.get(url, allow_redirects=True)
    open(file, 'wb').write(r.content)
    return file

def getdata(file):
    xlsx = openpyxl.load_workbook(file, read_only=True)
    if 'LK_7-Tage-Fallzahlen (fixiert)' in xlsx:
        sheet = xlsx['LK_7-Tage-Fallzahlen (fixiert)']
    elif 'LK_7-Tage-Inzidenz' in xlsx:
        sheet = xlsx['LK_7-Tage-Inzidenz']
    data = {}
    negCol = -1
    while data == {}:
        if sheet[5][negCol].value == None:
            negCol -= 1
        else:
            data['date'] = sheet[5][(negCol-14):negCol]
    print(data['date'])

    for row in sheet.iter_rows(min_row=6, values_only=True):
        if not row[1] == None and (not filtered or row[2] in filter + ['LKNR']):
            index = row[1]
            data[index] = (row[(negCol-14):negCol])[::-1]
    xlsx.close()
    return data

def generatehtml(data, path):
    html = '%s/index.html' %(path)
    with open(html, 'a') as f:
        f.write('\n'.join([
            '<!DOCTYPE html>',
            '<html lang="de">',
            '   <head>',
            '       <title>RKI Inzidenz Historie</title>',
            '       <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5">',
            '       <style>',
            '           html,body {',
            '               background: #1D1F21;',
            '               color: #C5C8C6;',
            '               font-family: sans-serif;',
            '               text-align: center;',
            '           }',
            '           a {',
            '               text-decoration: none;',
            '               color: #81A2BE;',
            '           }',
            '           table {',
            '               margin: 1em auto;',
            '           }',
            '           .red {',
            '               color: #CC6666;',
            '           }',
            '           .orange {',
            '               color: #F0C674;',
            '           }',
            '           .green {',
            '               color: #b5db68;',
            '           }',
            '       </style>',
            '   </head>',
            '   <body>',
            '       <h1>RKI Inzidenz Historie</h1>', 
            '       <p>RKI Stand: %s' %(data['date'][0].strftime("%d.%m.%Y")), '<br>'
            '       Letztes Update: %s</p>' %(datetime.datetime.now()), ''
        ]))

        for lk in data:
            if lk == 'date': continue
            id = urllib.parse.quote_plus(' '.join(lk.split(' ')[1:]))
            f.write('       <h2 id="%s"><a href="#%s">%s</a></h2>\n' %(id, id, ' '.join(lk.split(' ')[1:])))
            f.write('       <table>\n')
            for i in range(len(data[lk])):
                if data[lk][i] <= 50:
                    color = "green"
                elif data[lk][i] <= 100:
                    color = "orange"
                else:
                    color = "red"
                f.write('           <tr>\n')
                f.write('               <th>%s</th>\n' %(data['date'][i].strftime("%d.%m.")))
                f.write('               <th class="%s">%1.2f</th>\n' %(color, data[lk][i]))
                f.write('           </tr>\n')
            f.write('       </table>\n')

        f.write('\n'.join([
            '   </body>',
            '</html>'
        ]))
    return html

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tempdir:
        file = getrkixlsx("https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Kum_Tab.xlsx?__blob=publicationFile", tempdir)
        data = getdata(file)
        html = generatehtml(data, tempdir)
        open('index.html', 'w').write((open(html).read()))