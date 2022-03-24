#%%
from base64 import urlsafe_b64decode
from urllib import request
import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd
# %%
url = "https://portalcafebrasil.com.br/todos/podcasts/"

# %%
ret = requests.get(url)
# %%
ret.text
# %%
soup = bs(ret.text)
# %%
soup.find('h5')
# %%
soup.find('h5').text

# %%
soup.find('h5').a["href"]

# %%
lst_podcasts = soup.find_all("h5")
# %%
for item in lst_podcasts:
    print(f"EP: {item.text} - Link: {item.a['href']} ")
# %%
url = "https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true"

# %%
url.format(5)
# %%
def get_podcasts(url):
    ret = requests.get(url)
    soup = bs(ret.text)
    return soup.find_all('h5')
# %%
get_podcasts(url.format(5))

# %%
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)
# %%
i = 1
lst_podcasts = []

lst_get = get_podcasts(url.format(i))
log.debug(f"Coletando {len(lst_get)} episódios do link : {url.format(i)}")
while len(lst_get) > 0:
    lst_podcasts = lst_podcasts + lst_get
    i += 1
    lst_get = get_podcasts(url.format(i))

# %%
len(lst_podcasts)
# %%
df = pd.DataFrame(columns=['nome', 'link'])

# %%
for item in lst_podcasts:
    df.loc[df.shape[0]] = [item.text, item.a['href']]
# %%
df.shape
# %%
df.to_csv('banco_de_podcast.csv', sep=';', index=False)

