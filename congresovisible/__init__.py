import requests
import json
import codecs

from lxml import html
from lxml.cssselect import CSSSelector


class VoteScraper:
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
		title_project = self.extract_project_title(parsed_tree)
		votes = self.extract_votes(parsed_tree)
		return votes

	def extract_project_title(self, parsed_tree):
		'''
		Extracts the description of a vote event from the html
		@param parsed_tree lxml parsed tree 
		'''
		title_project =""
		project_title_selector = CSSSelector('meta[name=description]')
		for title in project_title_selector(parsed_tree):
			title_project = title.get("content")
		return title_project

	def extract_votes(self, parsed_tree):
		'''
		Extracts the politcians and their votes
		@param parsed_tree lxml parsed tree 
		'''
		votes = dict()
		detailed_info_selector = CSSSelector('table#tabla-reporte-detallado,tbody')
		for el in detailed_info_selector(parsed_tree):
			tr_tags = el.getchildren()
			for tr in tr_tags:
				name = ""
				party = ""
				vote = ""
				tds = tr.getchildren()

				try:

					if(len(tds)==3):

						name = tds[0].getchildren()[0].text
						party = tds[1].getchildren()[0].text
						vote = tds[2].getchildren()[0].getchildren()[0].text
					
					if name and vote and party:
						votes[name] = {"vote": vote, 'party': party}
				except:
					pass
		return votes


s = requests.Session()

class Votaciones:
	'''
	Extracts all the voting events (just general information) from congreso visible
	'''

	def __init__(self):
		# Getting the number of pages which we have to fetch
		self.number_of_pages = self.make_request(1)['pags']
		self.all_data = list()

	def make_request(self, page_number):
		'''
		makes a request to congreso visible getting the information about voting events for a given page
		'''
		try:
			url = "http://www.congresovisible.org/votaciones/search/votaciones/?q=%20&page="+str(page_number)
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

class Votacion:
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
			
			scrapper = VoteScraper()
			scrapped_data = scrapper.extract(html_content.encode('utf-8'))
			self.data['detailed'] = scrapped_data
		except Exception as e:
			print("error, get_detailed_data: ", e)
