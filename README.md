# Dumps congresovisible.org

[Congresovisible.org](http://www.congresovisible.org) is a great project which provides information about :

- Colombian law projects
- How are those projects voted
- Votes made by Senators and Congressmen

Sadly they don't provide an API for this valuable information.  So this repo provides :

- code to scrape their website in order to extract valuable information
- data dumps (in json format)


## How is the data structured

The data is structured as a list of vote events, each event consists of the data shown below:

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

# How to use it?

- If you just want to use the date, clone this repo and go to the folder `dumps`, pick your file ^^.

- If you want to generate a new dump: 

   1. Create a virtualenv with python3.4
   2. `pip install -r requirements.txt`
   3. `python main.py`

## Contact

dav.alejandro@gmail.com