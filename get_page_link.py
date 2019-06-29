import json
import requests

def get_single_page_link(page):
  api_url = "https://fr.wikipedia.org/w/api.php"
  params = {
  "action": "parse",
  "format": "json",
  "page": page,
  "prop": "links",
  }
  print("requesting : " + page)
  res = requests.Session().get(url=api_url, params=params)
  res_json = res.json()
  links = res_json["parse"]["links"]
  page_list = []
  for link in links:
    if "exists" in link.keys():
      page_list.append(link["*"])
  return page_list

def dummy_check(start, end):
  page_start = get_single_page_link(start)
  page_end = get_single_page_link(end)
  for link in page_start:
    if link in page_end:
      return [start, link, end]
  return []

def from_page_to_page(start, end):
  dummy_res = dummy_check(start, end)
  if dummy_res != []:
    return dummy_res
  page_done = set()
  page_todo = [start]
  total_request = 0
  parent_pages = {}
  while end not in page_todo and len(page_done) < 1000:
    current_page = page_todo.pop(0)
    if current_page in page_done:
      continue
    page_next = get_single_page_link(current_page)
    total_request += 1
    for page in page_next:
      parent_pages.setdefault(page, []).append(current_page)
      page_todo.append(page)
    page_done.add(current_page)
    print("total requests = " + str(total_request))
  if end in parent_pages.keys():
    #For now we assume we don't have collision or loops
    current_parent = parent_pages[end][0]
    res = [end]
    while current_parent != start:
      res.insert(0, current_parent)
      current_parent = parent_pages[current_parent][0]
    res.insert(0, start)
    return res
  else:
    return ['Error']


print(from_page_to_page("Emmanuel Macron", "Lille"))
print(from_page_to_page("Obama", "Lille"))