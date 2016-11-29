# -*- coding: utf-8 -*-
"""
Created on Mon Feb 08 19:49:08 2016

parse search results for a car search in san francisco and generate a summarized web page using jinja.

Can be used with task scheduler or chron to refresh.

@author: Drew
"""

import BeautifulSoup as bs
import urllib as ur
import jinja2

# points to the jinja template to be rendered
TEMPLATE_DIR = r'C:\Users\###\Documents\html pages'
env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

# list of models i'm interested in
models = ['Rogue','Trax','Tuscon','RAV4','CRV','Forester','Patriot','Cherokees','Crosstrek','Sportage','Outlander','Outback','Tiguan','Santa Fe','Escape','CX-5','CX-3','Trailhawk','Highlander']

# base search with optional url queries
BASE_HTML = 'https://sfbay.craigslist.org/search/cto?is_paid=all&search_distance_type=mi&min_auto_year=2005&min_auto_miles=250&max_auto_miles=100000&auto_drivetrain=3&auto_title_status=1&query='

#parsing function
def parse_results(model):
    results = []
    url = BASE_HTML + model.replace(' ','+')
    soup = bs.BeautifulSoup(ur.urlopen(url).read())
    rows = soup.find('span','rows').findAll('p','row')
    if len(rows) > 0:
        for row in rows:
            if 'sacramento' in row.a['href'] or 'modesto' in row.a['href'] or 'goldcountry' in row.a['href']:
                url = 'http:' + row.a['href']
            else:
                url = 'https://sfbay.craigslist.org' + row.a['href']
            create_date = row.find('time')['datetime']
            title = row.find('span', 'pl').a.getText()
            if not model in title:
                continue
            else:
                if row.find('span','price'):              
                    price = row.find('span','price').getText()
                else:
                    price = 'no price'
                results.append({'model': model, 'url':url, 'time': create_date, 'title': title, 'price': price})
        return results

# list results
results={}
for model in models:
    results[model] = parse_results(model)
    if not results[model]:
        results.pop(model, None)

# generate the new webpage
z=env.get_template('20160209 Craigslist Template.html').render(models=[key[0] for key in results.iteritems()], results=results)

# save the new webpage
outfile = r'C:\Users\###\Documents\html pages\Craigslist Cars.html'
with open(outfile, 'w') as f:
    f.write(z)