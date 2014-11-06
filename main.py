import codecs
import datetime
import json


from congresovisible import VoteScraper, Votaciones, Votacion


def extract_details_votes(path_to_json_file, path_to_output_file):
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
		print("vote %s out of %s" % (counter, total_number_of_votes))
		counter = counter + 1
		
		detailed_votacion = Votacion(vote['id'], vote)
		detailed_votacion.get_detailed_data()
		output_file.write(json.dumps(detailed_votacion.data, ensure_ascii=False) + "\n")
		
	output_file.close()


# Extracts all voting events(with general information) and save them to a file 
votaciones_extractor = Votaciones()
votaciones_extractor.extract_all()
votaciones_extractor.export("all_votaciones.json")

current_date = datetime.datetime.now()
output_file_name =  "dumps/%s-%s-%s.json" % (current_date.day, current_date.month, current_date.year)
# Once we have all the general events we need to enrich them with the information about the politician votes.
extract_details_votes("all_votaciones.json", output_file_name)