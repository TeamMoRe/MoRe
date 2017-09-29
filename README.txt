This project was made by Nicolas Pougeade, Anthony Andolfo, Etienne Gautier, Pierre-Marie Becoulet, Alexandre Calnibalosky, Alexandre Ollivier, Guillaume Morel and Thibaud Leclaire.
Works with Django - make sure it is installed - go into your project folder and use the command "python3 manage.py runserver"
Website is fully functionnal : homepage is localhost:8000/bdd/base1
Works with MovieLens 100k database - already imported in db.sqlite3. If need to reimport it : use the command "python3 manage.py importation_bdd".
To delete informations entered by the user, uncomment line #14 in bdd.views and run the page base1 one time
2 algorithms can be used "fast_cf_new" and "pca_method" however only pca_method is implemented as it is faster
