from lxml import html
import requests
import re
monthToNumber = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12}


# a changer selon le wiki
wiki = "https://shokugekinosoma.fandom.com"

# si la page reprenant les persos n'est pas /wiki/Characters, il faut changer "page_wiki_charac"
page_wiki_charac = '/wiki/Characters'


page = requests.get(f'{wiki}{page_wiki_charac}')
tree = html.fromstring(page.content)


# il faut trouver une expression xpath qui permet de prendre tout les liens se dirigant vers les pages de perso
table = tree.xpath('//tr/th/a')
chartable = {}
for x in table:
    link = x.xpath('./@href')
    title = x.xpath('./@title')
    if link == [] or re.search("/wiki/*", link[0]) is None or link[0] in chartable:
        continue
    chartable[link[0]] = title[0]


characters = []
used_link = []
i = 0
wikiname = re.search("https://(\w*)(.\w*)+", wiki).group(1)
print(wikiname)
for x in chartable:
    if x in used_link:
        continue
    used_link.append(x)
    p = requests.get(f"{wiki}{x}")
    t = html.fromstring(p.content)

    # il faut trouver une expression xpath qui permet de trouver la date de naissance du personnage
    # il n'est pas forcément nécessaire de le changer
    date = t.xpath('//div[@data-source="birthday"]/div/text()')

    if date == []:
        # mettre continue ne met pas les persos qui n'ont pas de date
        # mettre date = ??? affiche les persos qui n'ont pas de date

        # continue
        date = "???"
    else:
        date = date[0]
        for end in ["st", "nd", "rd", "th"]:
            if date.endswith(end):
                date = date[:-2]
        try:
            day = re.search("\d{1,2}", date).group()
            month = re.search("[\w]+", date).group()
            year = ''
            try:
                year = re.search("\d{4}", date).group()
            except(AttributeError):
                year = '2019'

            date = f"{day}/{monthToNumber[month.lower()]}/{year}"
        except(AttributeError):
            date = date
    characters.append({"name": chartable[x], "date": date})
    print(f'{chartable[x]} : {date}')
    i += 1

txt = ""
for x in characters:
    txt += f"{x['name']},{x['date']}\n"

with open(f"charac_{wikiname}.csv", mode="w+", encoding='utf-8') as f:
    f.truncate(0)
    f.write(txt)
    f.close()
