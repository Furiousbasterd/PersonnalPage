# -*-coding:Utf-8 -*

import re,json,datetime
import pprint,quickstart
from urllib.request import urlopen

meteoJson = urlopen('http://www.infoclimat.fr/public-api/gfs/json?_ll=43.611617,1.443825&_auth=BR8FElQqXH4EKQA3UiQFLAJqDzpbLQEmA38LaFw5Ui8GbVIzBWUAZl4wAH1QfwQyU34PbAoxVWUEbwZ%2BWigDYgVvBWlUP1w7BGsAZVJ9BS4CLA9uW3sBJgNoC2pcL1IzBmZSNQV4AGNeMQBgUH4EMlNjD2gKKlVyBGYGZVoxA2kFZAVpVDRcOQRvAGFSfQUuAjQPaFttAToDZws4XDhSZwZnUmAFZgA2XjUAZFB%2BBDZTYQ9mCjFVbgRuBmVaPgN%2FBXkFGFREXCMEKwAgUjcFdwIsDzpbOgFt&_c=5b2527339f90d5977d760a122004061f')

d = json.loads(meteoJson.read().decode("utf-8"))
now = datetime.datetime.now()
date = str(now).split(" ")[0]
dict_date = {}
for key in d:
    hourOfDay = key.split(" ")
    if date == key.split(" ")[0]:
        dict_date.update({hourOfDay[1]:key})
for sKey in sorted(dict_date.keys()):
    value = d.get(dict_date.get(sKey))
    
var = quickstart.main()
for s in var:
    print(s)