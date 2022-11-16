#make txt document for easy parsing
#parse to get the Chemistry terms to be defined\
#format all of the definitions and mark the new lines
#merriam webster api to get definitions
#format definitions with linebreaks for the pdf
#make a new pdf with a new water mark - AFTER  PAGE 0 THERE IS AN ISSUE WITH THE PYPDF 2 NXT PG
# #TO BE ADDED#Layer all of those edited pdfs
#TO BE ADDED#DO THE SAME WITH IMAGES AND KEY TERMS AND LINKS

from PyPDF2 import PdfFileReader, PdfFileWriter
import re
#NAME PDF chem.pdf
file_path = 'chem.pdf'
pdf = PdfFileReader(file_path)
#create and format chem comp.txt
with open('chem comp.txt', 'w') as f:
    for page_num in range(pdf.numPages):
        pageObj = pdf.getPage(page_num)

        try: 
            txt = pageObj.extractText()
            print(''.center(100, '-'))
        except:
            pass
        else:
            f.write('Page {0}\n'.format(page_num+1))
            f.write(''.center(100, '-'))
            f.write(txt)
    f.close()

#PARSING-find definitions and new pages
ChemTXT = open("chem comp.txt", "r").readlines()
Terms = ["FILL"]#Vocab to be defined
ParseIND = [":", "-", "Page", "Picture", "Definition", "Key"]#ADD ANY EXCEPTIONS HERE
#characters in lines that mess up the terms LINES THAT ARE NOT IN THE TERMS
for ans in ChemTXT:
    if ans.startswith("Word:"):
        Terms.append(ans[5:])    
    elif 'Week' in ans and len(Terms) != 0:
        Terms[-1] += "~"
        #IS THE NEW{PAGE}
    #find the term lines
del Terms[0]#remove filler
print(Terms)
NP = []#new page mark index list
#FORMATTING TERM LINES
for z in  range(len(Terms)):
    Terms[z] = Terms[z].replace("\n", "")
    #remove \n
    if Terms[z].count("~") == 1 and "Key" not in Terms[z]:
        NP.append(z)
        Terms[z]= Terms[z][:-1]
        #Remove tilde and mark index
    while Terms[z].endswith(" "):
        Terms[z] = Terms[z][:-1]
    while Terms[z].startswith(" "):
        Terms[z] = Terms[z][1:]
    Terms[z] = Terms[z].replace(' ', '%20')
    #change space into %20 for merriam formatting
    Terms[z] = Terms[z].replace("’", '%27')
    #replace the '
    if Terms[z].islower() is True and Terms[z].startswith(" polar") is False:
        Terms[z] = Terms[z - 1] + "%20" + Terms[z]
        #remove those pesky 2 line definitions
for i in NP:
    Terms[i+1] = Terms[i+1]+'~'

print(Terms)

links = []
for i in Terms:
    i = i.replace("~", "")
    links.append("https://www.merriam-webster.com/dictionary/" + i)
for i in links:
    print(i, '\n')

#MERRIAM WEBSSTER API
defs = [] 
import requests
wordnum = 1
for i in Terms:
    i = i.replace("~", "")

    link = 'https://dictionaryapi.com/api/v3/references/sd4/json/'+ i +'?key=097ffc46-e2c1-462e-9e74-d2fcef820b85'
    r = requests.get(link)
    j = r.text
    q = j.split(',')

    if '"shortdef"' in j: 
        defnum = 0
        for a in q:
            if a.startswith('"shortdef"'):
                defs.append(a[12:])
                defnum += 1
        #temporary number of definitions
        tdefnum = defnum
        if tdefnum > 1:
            while tdefnum >= 1:
                print(tdefnum, defs[-tdefnum])
                tdefnum -= 1#MAYBE CLEAN THIS whole SECTION LATER XDDDDDDDDDDDDDDD
                #print the definitons from the most recent word
            print("Word: ", i)
            whichdef  = int(input("(1 - 9) Which definiton most fits the word: "))

            for i in defs[-defnum:]:
                if i != defs[len(defs) - whichdef]:
                    defs.remove(i)
                #remove the definitions you didnt choose
    else:
        defs.append("NA")
    wordnum += 1
n = "NA"#Format line breaks after a space before 30 chars ####REALLY NEEDS CLEANING
defs2 = []
for i in defs:
    for m in range(len(i)//30):
        x = re.findall("\s", i[:((m+1)*30)])
        LList=len(x) 
        g = re.sub(' ', '\n', i, LList)
        g = re.sub('\n', ' ', g, LList - 1)
        if m == 0 :
            n = g + i[30:]
        else:
            n = n[:(m+1)*30-30] + g[(m+1)*30-30:] + n[:(m+1)*30]
    defs2.append(n)
    n = "NA"
for i in defs2:
    print(i, "\n")
print(defs2)

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import AnnotationBuilder
from PyPDF2 import PdfFileMerger
# Fill the writer with the pages you want
import os
path = 'C:\\programming\\newproject'
RESOURCE_ROOT = 'C:\\programming\\newproject'#FIND SOME WAY TO GET FOLDER LATER
pdf_path = 'C:\\programming\\newproject'
#make a page function

def boxMake(BotY, TopY, PgNum, DEFF, TNum):
    
    pdf_path = os.path.join(RESOURCE_ROOT, "chem.pdf")
    reader = PdfReader(pdf_path)
    page = reader.pages[PgNum]
    writer = PdfWriter() 
    writer.add_page(page)
    annotation = AnnotationBuilder.free_text(
        #after 32 char skip make new linec
        DEFF,
        rect=(30, BotY, 252, TopY),
        #(left)x, (bottom)y, (right)x, (top)y
        font="Arial",
        bold=True,
        italic=True,
        font_size="16pt",
        font_color="000000",
        border_color="000000",
        background_color="cdcdcd",
    )
    writer.add_annotation(page_number=PgNum, annotation=annotation) 
    Temps = "Compchem" + str(TNum) + ".pdf"
    with open(Temps, "wb") as fp:
            writer.write(fp)   


PGN = 0
for i in range(len(defs2)):
    print(i)
    if Terms[i].count("~") == 1 or i == 0:
        n = 1 
        BTY = 535
        TPY = 700
        #if end of page indicator or start
    if n == 2:
        BTY -= 240
        TPY -= 215
    if n == 3:
        BTY -= 220
        TPY -= 240
    if Terms[i].count("~"):
        PGN += 1
    boxMake(BTY, TPY, PGN, defs2[i], i)
    n += 1
    
'''

pdf_merger = PdfFileMerger()



#for n in range(i):#i is num of pages
#    pdf_merger.append("Compchem" + str(n + 1) +".pdf")
pdf_merger.append('Compchem0.pdf')
pdf_merger.append('Compchem1.pdf')
pdf_merger.append('Compchem2.pdf')
pdf_merger.append('Compchem3.pdf')

with open(paths.abspath('FinalChem.pdf'), 'wb') as append_pdf:
    pdf_merger.write(append_pdf)

pdf_merger2 = PdfFileMerger()

files = [file for file in lisdir('.') if path.isfile(file) and file.endswith(".pdf")]

for file in files:
    print(file)
    pdf_merger2.append(file)

with open(path.abspath('FinalChem.pdf'), 'wb') as append_all_pdf:
    pdf_merger2.write(append_all_pdf)
'''


#COPY FROM STACK OVERFLOW IF NOT WORK
'''XDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD:|)
'''

