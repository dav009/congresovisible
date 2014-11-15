import codecs
import datetime
import json
import requests
import re
from lxml import html
from lxml.cssselect import CSSSelector

import logging

from utils import *

s = requests.Session()

class LawTextIndex:

    def __init__(self):
        # Getting the number of pages which we have to fetch
        self.number_of_pages = self.make_request(1)['pags']
        self.all_data = list()

    def make_request(self, page_number):
        '''
        makes a request to congreso visible getting the information about voting events for a given page
        '''
        try:
            url = "http://www.congresovisible.org/proyectos-de-ley/search/proyectos-de-ley/?q=%20&page="+str(page_number)
            r = s.get(url)
            return json.loads(r.text)
        except Exception as e:
            print(e)

    def extract_all(self):
        '''
        Gets all the voting events from congresovisible.org
        '''
        for i in range(1, self.number_of_pages):
            extracted_data = self.make_request(i)
            if extracted_data:
                for votacion in extracted_data['elementos']:
                    self.all_data.append(votacion)
            print("done with.. page %s out of %s" % (i, self.number_of_pages))

    def export(self, path_to_output_file):
        '''
        save all the voting events to a file
        '''
        print("dumping extracted data to file...")
        output_file = codecs.open(path_to_output_file, 'w', 'utf-8')
        output_file.write(json.dumps(self.all_data))
        output_file.close()

class LawScraper:

    '''
    Given a page like : http://www.congresovisible.org/votaciones/10872/
    it will extract the vote information in a dictionary format
    '''
    def __init__(self):
        pass

    def extract(self, html_content):
        '''
        @param html_content html content of a vote page
        @returns vote information of a porject

        '''
        parsed_tree = html.fromstring(html_content)
        extract_vote_ids = self.extract_vote_ids(html_content)
        law_text = self.extract_law_text(parsed_tree)
        return {'law_text': law_text, 'votes': list(extract_vote_ids)}

    def extract_law_text(self, parsed_tree):
        '''
        Extracts the description of a vote event from the html
        @param parsed_tree lxml parsed tree 
        '''
        law_text = ""
        content_container = "div.block.c div.content-block div.module6 div.tab.primero div.without-padding-bottom.contenido-tab div.module7 p"
        law_text_selector = CSSSelector(content_container)
        for law_container in law_text_selector(parsed_tree):
            law_text = law_container.text
            return law_text
        return law_text

    def extract_vote_ids(self, html_content):
        '''
        Extracts the politcians and their votes
        @param parsed_tree lxml parsed tree 
        '''
        set_of_votes_ids = set()
        pattern = re.compile(b'votaciones/(\d+)')
        matches = re.finditer( pattern, html_content)
        for match in matches:
            set_of_votes_ids.add(int(match.group(1).decode()))
        return set_of_votes_ids


class Ley:
    '''
    Represents a vote Event
    '''

    def __init__(self, identifier, data, dump_path = None):
        '''
        @param identifier identifier in congresovisible's database
        @param data general data about a vote event
        @param dump_path path to the html dump of the vote pages
        '''
        self.id = identifier
        self.data = data
        self.dump_path = dump_path
        self.get_detailed_data()

    def get_html_from_dump(self, id_vote):
        '''
        @param id_vote id of the voting event
        Gets the html content of the vote with given id from the dump_path
        '''
        html =""
        try:
            path_to_file = '%s/%s' %(self.dump_path, id_vote)
            html  = " ".join(codecs.open(path_to_file,'r','utf-8').readlines())
        except Exception as e:
            print("error : %s" % page_number)
        return html

    def fetch_page(self, id_vote):
        '''
        @param id_vote id of the voting event
        Gets the html content of the vote with given id by making a request to congresovisible
        '''
        url = "http://www.congresovisible.org/votaciones/%s/" % self.id
        html = ""
        try:
            response = requests.get(url)
            html = response.text
        except e as Exception:
            print("error : fetching page %s" % url)
        return html

    def get_detailed_data(self):
        '''
        Gets the detailed data of a voting event( who voted yes and who voted No)
        '''
        try:
            html_content = self.get_html_from_dump(self.id) if self.dump_path else  self.fetch_page(self.id)
            
            scrapper = LawScraper()
            scrapped_data = scrapper.extract(html_content.encode('utf-8'))
            self.data['detailed'] = scrapped_data
        except Exception as e:
            logging.exception("Something awful happened!")
            print("error, get_detailed_data: ", e)
#lawIndexExtractor = LawTextIndex()
#lawIndexExtractor.extract_all()
#lawIndexExtractor.export("all_laws")

# read extracted laws urls
#list_of_urls = list()
#f = codecs.open("all_laws", 'r', 'utf-8')
#json_file = json.load(f)
#for item in json_file:
#    list_of_urls.append("http://www.congresovisible.org/"+item['url'])
#
#dumper = UrlDumper(list_of_urls, "html_law_texts/")
#dumper.fetch_all_html()
# fetch their html
# scrape them


def extract_details_law(path_to_json_file, path_to_output_file):
    '''
    @param path_to_json_file path to json file containing json infomration about voting events (ids)
    @param path_to_output_file path to output file which will contain detailed information about each voting event
    '''
    output_file = codecs.open(path_to_output_file, 'w', 'utf-8')
    json_data = open(path_to_json_file)
    votes = json.load(json_data)
    total_number_of_votes = len(votes)
    counter = 0
    for vote in votes:
        # loop through each voting event and get its detailed data
        print("law %s out of %s" % (counter, total_number_of_votes))
        counter = counter + 1
        
        detailed_votacion = Ley(vote['id'], vote, dump_path="html_law_texts/")
        detailed_votacion.get_detailed_data()
        output_file.write(json.dumps(detailed_votacion.data, ensure_ascii=False) + "\n")
        
    output_file.close()


current_date = datetime.datetime.now()
output_file_name =  "dumps/laws_%s-%s-%s.json" % (current_date.day, current_date.month, current_date.year)
# Once we have all the general events we need to enrich them with the information about the politician votes.
extract_details_law("all_laws", output_file_name)

