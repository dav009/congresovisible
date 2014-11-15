 
from multiprocessing import Process, Pool
import time
import requests
import codecs
import os.path
import re
import itertools

s = requests.Session()

 
def http_get(url, output_path, split_word = "votaciones"):

  try:
      id_ =  re.findall(r'/(\d+)/',url)[0]

      if not os.path.exists(output_path):
          os.makedirs(output_path)

      if not os.path.isfile(output_path+id_):
          r = s.get(url, timeout=20)
          print("fetching..%s"%url)
          f = codecs.open(output_path+id_, 'w', 'utf-8')
          f.write(r.text)
          f.close()
          return url, r.text
  except:
    print("error : %s" %url)


class UrlDumper:

    def __init__(self, list_of_urls, output_path):
        self.list_of_urls = list_of_urls
        self.pool = Pool(processes=10)
        self.output_path = output_path

    def fetch_all_html(self):
        arguments = zip(self.list_of_urls, itertools.repeat(self.output_path))
        results = self.pool.starmap(http_get,  arguments)
 
  