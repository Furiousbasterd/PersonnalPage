# -*-coding:Utf-8 -*

from tweepy import OAuthHandler
from urllib.request import urlopen
from random import randint
import tweepy,re,json,datetime,quickstart,xml.dom.minidom

'''

Twitter feed bloc: this will build the twitter bloc. Don't forget to edit the key with your credentials. If you don't already have those, go to "https://apps.twitter.com/"
and create a new app. Then follows the step to obtain the credentials.

'''
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

last_tweet = ""
for status in tweepy.Cursor(api.home_timeline).items(1):
    last_tweet = status.text
#print(last_tweet)

s = re.split('\s', last_tweet)
tweetos = '<div id="twitter">'
for word in s:
    if re.search('#.+',word):
        m = re.search('#.+',word)
        #print(m.group(0))
        tweetos= tweetos+" <b>"+m.group(0)+"</b>"
    
    elif re.search('@.+', word):
        m = re.search('(@.+)', word)
        #print(m.group(0))
        tweetos= tweetos+" <b>"+m.group(0)+"</b>"
    elif re.search('http[s]?', word):
        m = re.search('(http[s]?.+)', word)
        tweetos = tweetos+" <a href="+m.group(0)+"> <i><b>Clic pour t'éblouir de belles images</b></i></a>"
    
    else:
        tweetos = tweetos+" "+word

tweetos += "</div>"
print(tweetos)

'''

Meteo Bloc Builder: this will build a table containing meteo data. I use the infoclimat's public API, all you need to do is find the latitude and longitude
(you can do it with google maps) of your city, and edit the meteoJson url. It works for french cities, but i don't know if it works for other country, I higly doubt it.
If you can find a public API giving you json meteo information, try it with this scripts. If the output follows the same structure it would work (you may try to edit the keys though).

'''
meteoJson = urlopen('http://www.infoclimat.fr/public-api/gfs/json?_ll=43.611617,1.443825&_auth=BR8FElQqXH4EKQA3UiQFLAJqDzpbLQEmA38LaFw5Ui8GbVIzBWUAZl4wAH1QfwQyU34PbAoxVWUEbwZ%2BWigDYgVvBWlUP1w7BGsAZVJ9BS4CLA9uW3sBJgNoC2pcL1IzBmZSNQV4AGNeMQBgUH4EMlNjD2gKKlVyBGYGZVoxA2kFZAVpVDRcOQRvAGFSfQUuAjQPaFttAToDZws4XDhSZwZnUmAFZgA2XjUAZFB%2BBDZTYQ9mCjFVbgRuBmVaPgN%2FBXkFGFREXCMEKwAgUjcFdwIsDzpbOgFt&_c=5b2527339f90d5977d760a122004061f')
d = json.loads(meteoJson.read().decode("utf-8"))
now = datetime.datetime.now()
date = str(now).split(" ")[0]
dict_date = {}
for key in d:
    hourOfDay = key.split(" ")
    if date == key.split(" ")[0]:
        dict_date.update({hourOfDay[1]:key})

meteoPart = '<div id="meteo"><h3>'+date+'</h3>\n<table>'
meteoPart += '<tr><th>Heure</th><th>Temperature</th><th>Risque de pluie</th><th>Vent Moyen (km/h)</th><th>Rafales (km/h)</th><th>Risque enneigement</th></tr>'

for sKey in sorted(dict_date.keys()):
    value = d.get(dict_date.get(sKey))
    hour = sKey
    pluie = str(value.get('pluie'))
    vent_moyen = str(value.get('vent_moyen').get('10m'))+" km/h"
    vent_rafales = str(value.get('vent_rafales').get('10m'))+" km/h"
    risque_neige = str(value.get('risque_neige'))
    temperature = value.get('temperature').get('sol')-273
    temperature = str(round(temperature,2))+" C°"
    meteoPart += '<tr><td>'+hour+'</td><td>'+temperature+'</td><td>'+pluie+'</td><td>'+vent_moyen+'</td><td>'+vent_rafales+'</td><td>'+risque_neige+'</td></tr>'
    
    
meteoPart +='</table></div>'

'''

Events Bloc Builder: we create a table containing every events for the present day. To be sure it works correctly, be sure to follow this tutorial: https://developers.google.com/google-apps/calendar/quickstart/python
and follow all the steps, execpt the fourth. I slightly modified the script to meet my needs, I just added a return statement and 2 variables.

'''

eventsOfTheDay='<div id="calendar"><h3>Ce qui t\'attend aujourd\'hui</h3>\n<table>\n'\
            '<tr><th>Debut</th><th>Fin</th><th>Résumé</th></tr>'
eventsFromCalendar= quickstart.main()
for events in eventsFromCalendar:
    events = events.split("|")
    if date == events[0]:
        if(re.search("\d+:\d+:\d+.+", events[1])):
            rg = re.search("(\d+):\d+:\d+\+(\d+):\d+", events[1])
            startHour = rg.group(1)+"h"
            endHour = int(rg.group(1))+int(rg.group(2))
            endHour = str(endHour)+"h"
            eventsOfTheDay+='<tr><td>'+startHour+'</td><td>'+endHour+'</td><td>'+events[2]+'</td></tr>\n'
    elif events[0] == 'No upcoming events found.':
        eventsOfTheDay+='<tr><td></td><td></td><td> Rien de prévu aujourd\'hui</td></tr>'
eventsOfTheDay+="\n</table>\n</div>"




RSSTree = xml.dom.minidom.parse(urlopen("http://www.lemonde.fr/rss/une.xml"))
RSS = RSSTree.documentElement

rssbloc ='<div id="rss">\n<table>'

items = RSS.getElementsByTagName("item")

lastFeed = []
rssDict = {}

for item in items:
    titleNode = item.getElementsByTagName('title')[0]
    descriptionNode = item.getElementsByTagName('description')[0]
    title = titleNode.childNodes[0].data
    description = descriptionNode.childNodes[0].data
    lastFeed.append(title)
    rssDict.update({title:description})

for keys in lastFeed[0:10]:
    rssbloc += '<tr><td><tr><td>'+keys+'</td></tr><tr><td>'+rssDict.get(keys)+'</td></tr></td></tr>'

rssbloc +='\n</table>'
'''

Random pokemon of the day: this bloc was to add some fun to the page

'''
try:
    pokemons = ["Bulbizarre","Herbizarre","Florizarre","Salamèche","Reptincel","Dracaufeu","Carapuce","Carabaffe","Tortank","Chenipan","Chrysacier","Papilusion","Aspicot","Coconfort","Dardargnan","Roucool","Roucoups","Roucarnage","Rattata","Rattatac","Piafabec","Rapasdepic","Abo","Arbok","Pikachu","Raichu","Sabelette","Sablaireau","Nidoran♀","Nidorina","Nidoqueen","Nidoran♂","Nidorino","Nidoking","Mélofée","Mélodelfe","Goupix","Feunard","Rondoudou","Grodoudou","Nosferapti","Nosferalto","Mystherbe","Ortide","Rafflésia","Paras","Parasect","Mimitoss","Aéromite","Taupiqueur","Triopikeur","Miaouss","Persian","Psykokwak","Akwakwak","Férosinge","Colossinge","Caninos","Arcanin","Ptitard","Têtarte","Tartard","Abra","Kadabra","Alakazam","Machoc","Machopeur","Mackogneur","Chétiflor","Boustiflor","Empiflor","Tentacool","Tentacruel","Racaillou","Gravalanch","Grolem","Ponyta","Galopa","Ramoloss","Flagadoss","Magnéti","Magnéton","Canarticho","Doduo","Dodrio","Otaria","Lamantine","Tadmorv","Grotadmorv","Kokiyas","Crustabri","Fantominus","Spectrum","Ectoplasma","Onix","Soporifik","Hypnomade","Krabby","Krabboss","Voltorbe","Électrode","Nœunœuf","Noadkoko","Osselait","Ossatueur","Kicklee","Tygnon","Excelangue","Smogo","Smogogo","Rhinocorne","Rhinoféros","Leveinard","Saquedeneu","Kangourex","Hypotrempe","Hypocéan","Poissirène","Poissoroy","Stari","Staross","M. Mime","Insécateur","Lippoutou","Élektek","Magmar","Scarabrute","Tauros","Magicarpe","Léviator","Lokhlass","Métamorph","Évoli","Aquali","Voltali","Pyroli","Porygon","Amonita","Amonistar","Kabuto","Kabutops","Ptéra","Ronflex","Artikodin","Électhor","Sulfura","Minidraco","Draco","Dracolosse","Mewtwo","Mew"]
    pokerand = pokemons[randint(0,len(pokemons)-1)]
    pokurl = urlopen('http://www.pokepedia.fr/Fichier:'+pokerand+'-RFVF.png').read()
    pokurl = str(pokurl)
    if re.search('.+/images/.{1,2}/.{1,2}/'+pokerand+'-RFVF.png', pokurl):
        url = re.search('.+(/images/.{1,2}/.{1,2}/'+pokerand+'-RFVF.png)', pokurl)
        pokebloc = '\n<h3>Le pokemon du jour: '+pokerand+'</h3>\n<img src="http://www.pokepedia.fr'+url.group(1)+'"/>'
        print(pokebloc)
except Exception:
    if Exception:
        pokebloc = "<h3> Pas de pokemon, too bad!</h3>"
'''

Page Builder: here, the html page will be generated. It means that everybloc we built will be inserted at his proper place in the page.
 edit Filepath to point to the file where the page will be stored and accessed through internet. On linux it's often /var/www/html

'''
print('Creation de la page')
#
fichier = open("", "w", encoding = 'utf8')
fichier.write('<!doctype html>\n'\
              '\t<html lang="fr">\n'\
              '\t<head>\n'\
              '\t<meta charset="utf-8">\n'\
              '\t\t<title>Titre de la page</title>\n'\
              '\t\t<link rel="stylesheet" href="style.css">\n'\
              '\t\t<script src="script.js"></script>\n'\
              '\t</head>\n'\
              '\t<body>\n<h3>Ton twitter du jour</h3>\n')
fichier.write(tweetos)
fichier.write(meteoPart)
fichier.write(eventsOfTheDay)
fichier.write(rssbloc)
fichier.write(pokebloc)
fichier.write('\n\t</body>\n'\
                '</html>')
print('Page creee')

