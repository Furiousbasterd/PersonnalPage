# -*-coding:Utf-8 -*

from tweepy import OAuthHandler
import tweepy
import re


consumer_key = '[your consumer key]'
consumer_secret = '[your consumer secret key]'
access_token = '[your api access token]'
access_secret = 'your secret api access token]'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

last_tweet = ""
for status in tweepy.Cursor(api.home_timeline).items(1):
    last_tweet = status.text
#print(last_tweet)

s = re.split('\s', last_tweet)
tweetos = ""
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
print(tweetos)
print('Creation de la page')
#Filepath has to point to the file where the page will be stored and accessed through internet. On linux it's often /var/www/html
fichier = open("[filepath]", "w", encoding = 'utf8')
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
fichier.write('\n\t</body>\n'\
                '</html>')
print('Page creee')
