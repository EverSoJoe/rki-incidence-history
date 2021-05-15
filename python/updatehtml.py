import openpyxl
import requests
import tempfile
import urllib.parse

filter = [9777,9190,9762]

def getrkixlsx(url, path):
    file = '%s/inzidenzen.xlsx' %(path)
    r = requests.get(url, allow_redirects=True)
    open(file, 'wb').write(r.content)
    return file

def getdata(file):
    xlsx = openpyxl.load_workbook(file, read_only=True)
    sheet = xlsx['LK_7-Tage-Inzidenz']
    data = {}
    for row in sheet.iter_rows(min_row=6, values_only=True):
        if not row[1] == None and row[2] in filter:
            data[row[1]] = row[-14:-1]
    xlsx.close()
    return data

def generatehtml(data, path):
    html = '%s/index.html' %(path)
    with open(html, 'a') as f:
        f.write('\n'.join([
            '<html>',
            '   <head>',
            '       <title>RKI Inzidenz Historie</title>',
            '   </head>',
            '   <body>',
            '       <content>',
            '           <h1>RKI Inzidenz Historie nach Landkreisen und Städten</h1>', ''
        ]))

        for lk in data:
            id = urllib.parse.quote_plus(lk)
            f.write('           <h2 id="%s"><a href="#%s">%s</a></h2>\n' %(id, id, lk))
            f.write('           <ul>')
            for iz in data[lk]:
                if iz <= 50:
                    color = "green"
                elif iz <= 100:
                    color = "orange"
                else:
                    color = "red"
                f.write('               <li class="%s">%1.2f</li>' %(color, iz))
            f.write('           </ul>')

        f.write('\n'.join([
            '       </content>',
            '   </body>',
            '</html>'
        ]))
    return html

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tempdir:
        file = getrkixlsx("https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Kum_Tab.xlsx?__blob=publicationFile", tempdir)
        data = getdata(file)
        html = generatehtml(data, tempdir)
        open('html.html', 'w').write((open(html).read()))