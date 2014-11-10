import codecs
import json

def read_file(path_to_file, year='2014', legislature='Senado'):
    f_ = codecs.open(path_to_file, 'r', 'utf-8')
    dimensions_number = 0
    congresistas = dict()
    lista_de_votaciones = list()
    vectors = dict()
    for line in f_:
        votacion = json.loads(line.strip())
        if 'detailed' in votacion and votacion['ano'] == year and votacion['camaras'] == legislature:
            id_votacion = votacion['id']
            lista_de_votaciones.append(id_votacion)
            
            for congresista, detalles in votacion['detailed'].items():
                if not congresista in congresistas:
                    congresistas[congresista] = dict()
                    congresistas[congresista]['partido'] = detalles['party']
                    congresistas[congresista]['votos'] = dict()
                if detalles['vote']=="Aprobado":
                    congresistas[congresista]['votos'][id_votacion] =  100
                else:
                    congresistas[congresista]['votos'][id_votacion] =  -100

    all_votaciones = set(lista_de_votaciones)


    for name_congresista, congresista in congresistas.items():
        vector =list()
        for votacion in all_votaciones:
            if votacion in congresista['votos']:
                vector.append(congresista['votos'][votacion])
            else:
                vector.append(0)
        dimensions_number = len(vector)
        vectors[name_congresista + " " + congresista['partido']] = { 'vector': vector,
                                                                     'partido':congresista['partido']
                                                                   }

    output_file_name = 'vectors_%s_%s_%s.json' %(legislature, year, dimensions_number)
    out = codecs.open(output_file_name, 'w', 'utf-8')
    out.write(json.dumps(vectors, ensure_ascii=False))
    out.close()

read_file('../../dumps/5-11-2014.json')