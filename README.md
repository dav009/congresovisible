# Dumps congresovisible.org

[Congresovisible.org](http://www.congresovisible.org) is a great project which provides information about :

- Colombian law projects
- How are those projects voted
- Votes made by Senators and Congressmen

Sadly they don't provide an API for this valuable information.  So this repo provides :

- code to scrape their website in order to extract valuable information
- data dumps (in json format)


## How is the data structured

### Json Dump 

Every line of the json dump corresponds to a json dictionary representing a voting event, every event contains the following data: 

```json
[
  { 
     "camara" : "Cámara de Representantes",
     "estado" : "aprobado",
     "id": 3014,
     "ano": "2014",
     "mes_dia": "Sep 03",
     "desacuerdo": "1%",
     "comisiones": "",
     "acuerdo": "99%",
     "procedimiento": "Descripcion proyecto de ley",

     "detailed" : {
     	   {"Álvaro  Uribe": {"party": "Centro Democratico", "vote": "Aprobado"},
     	    ....
     	    ....
      }

   }

]
```

- `camara`: Which Legislature voted
- `id`: Congresovisible.org database identifier
- `ano`: Year in which the voting took place
- `mes_dia`: month, day in which the voting took place
- `detailed`: dictionary containing the name of politicians as keys, and a json object describing their party and vote as a value.

Each line of the file should be a parsable json object.

### CSV Data

The csv data is split in two files:

- `votes.csv`: contains the votes of politicians in sessions, each session is an identifier referencing a session description in `sessions.csv`
- `sessions.csv`: contains a session description, date, and legislature.

# How to use it?

- If you just want to use the data, clone this repo and go to the folder `dumps`, pick your file ^^.

- If you want to generate a new dump: 

   1. Create a virtualenv with python3.4
   2. `pip install -r requirements.txt`
   3. `python main.py`

## Contact

dav.alejandro@gmail.com
