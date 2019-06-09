from bs4 import BeautifulSoup, SoupStrainer
import requests
import urllib

def get_page_link(url):
  if url.startswith('/wiki/'):
    url = 'https://en.wikipedia.org' + url
  print('requesting ' + url)
  page = requests.get(url)
  data = page.text
  soup = BeautifulSoup(data, 'html.parser')
  url_list = []
  for link in soup.find_all('a'):
    if str(link.get('href')).startswith('/wiki/'):
      url_list.append(urllib.parse.unquote(link.get('href')))
  return url_list


def get_links_from_page_to_page(start, end):
  #TODO do a sanitizing pass on the end input in case it's not an url or not a wiki url
  desired_url = '/wiki/' + end
  if start == end:
    return [start]
  url_done = set()
  url_todo = []
  parent_link = {}
  url_todo.append(start)
  total_request = 0
  while (desired_url not in url_todo and len(url_done) < 1000):
    current_url = url_todo.pop(0)
    if current_url in url_done:
      continue
    url_next = get_page_link(current_url)
    total_request += 1
    for url_next in url_next:
      if url_next not in parent_link.keys():
        parent_link[url_next] = [current_url]
      else:
        parent_link[url_next].append(current_url)
      url_todo.append(url_next)
    url_done.add(current_url)
  print('total_request = ' + str(total_request))
  if desired_url in parent_link.keys():
    #For now we assume we don't have collison or loops
    parent_url = parent_link[desired_url][0]
    res = [desired_url]
    while parent_url != start:
      res.insert(0, parent_url)
      parent_url = parent_link[parent_url][0]
    res.insert(0, parent_url)
    return res
  else:
    return 'error'


print(get_links_from_page_to_page("https://fr.wikipedia.org/wiki/Emmanuel_Macron", "Lille"))
