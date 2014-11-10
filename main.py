import codecs
import datetime
import json
import os


from congresovisible import VoteScraper, Votaciones, Votacion

def toCSV(path_to_output_folder, path_to_input_json):

	if not os.path.exists(path_to_output_folder):
	    os.makedirs(path_to_output_folder)

	json_data = codecs.open(path_to_input_json, 'r', 'utf-8')

	session_header = ['camaras','id','mes_dia','procedimiento','estado','acuerdo','desacuerdo','ano','comisiones']
	votes_header = ['session_id', 'party', 'vote']

	lines_sessions = [session_header]
	lines_votes = [votes_header]

	for vote in json_data:
		vote = json.loads(vote)
		session = list()

		for key in session_header:
			if key != "detailed":
				session.append(str(vote[key]))

		for voter_name, voter_data in vote['detailed'].items():
			line_info = [str(vote['id']), voter_name, voter_data['party'], voter_data['vote']]
			lines_votes.append(line_info)

		lines_sessions.append(session)

	votes_output_file = codecs.open(path_to_output_folder+"/votes.csv", 'w', 'utf-8')
	session_output_file = codecs.open(path_to_output_folder+"/session.csv", 'w', 'utf-8')


	for line in lines_sessions:
		session_output_file.write("\t".join(line)+"\n")
	session_output_file.close()

	for line in lines_votes:
		votes_output_file.write("\t".join(line)+"\n")
	votes_output_file.close()



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

# Generates the csv version of the data
toCSV( "dumps/%s-%s-%s/", "dumps/%s-%s-%s.json")
