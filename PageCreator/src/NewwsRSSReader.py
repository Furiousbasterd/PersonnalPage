import xml.dom.minidom
from urllib.request import urlopen

RSSTree = xml.dom.minidom.parse(urlopen("http://www.lemonde.fr/rss/une.xml"))
RSS = RSSTree.documentElement

items = RSS.getElementsByTagName("item")

dic = {}
test = []
for item in items:
    titleNode = item.getElementsByTagName('title')[0]
    descriptionNode = item.getElementsByTagName('description')[0]
    title = titleNode.childNodes[0].data
    description = descriptionNode.childNodes[0].data
    
    test.append(title)
    dic.update({title:description})

for s in test[0:10]:
    print(dic.get(s))