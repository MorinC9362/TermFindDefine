ChemTXT = open("chem7 comp.txt", "r").readlines()
#\text parsing
WrongLineInd = [":", "-", "Page", "Picture", "Definition"]
Terms = []
for ans in ChemTXT:
    if ans.startswith("Word:"):
        Terms.append(ans[5:])
        
    elif ans.startswith("@ S. Carmichael 2015  Word:"):
        Terms.append(ans[27:])
    elif ":" not in ans and "-" not in ans and "Page" not in ans and "Picture" not in ans and "Definition" not in ans: 
        Terms.append(ans)
#Remove \n
z = 0
terms = []
for m in range(len(Terms)):
    terms.append(Terms[z].replace("\n", ""))
    terms.append(Terms[z].replace(' ', '%20'))
    z += 1

print(terms)

#webscraping with terms
from requests_html import HTMLSession
session = HTMLSession()
j = 'https://www.merriam-webster.com/dictionary/' + terms[1]
r = session.get(j)
print(r.text[0:1747])


