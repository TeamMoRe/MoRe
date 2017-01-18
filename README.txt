Works with Django - make sure it is installed - go into your project folder and use the command "python3 manage.py runserver"
Website is fully functionnal : homepage is localhost:8000/bdd/base1
Works with MovieLens 100k database -already imported in db.sqlite3. If need to reimport it : use the command "python3 manage.py importation_bdd" -- If you fully delete database, make sure to recreate a user "default" where all the attributes are set to "default".
To delete informations entered by the user, uncomment line #14 in bdd.views and run the page base1 one time
2 algorithms can be used "fast_cf_new" and "pca_method" however only pca_method is implemented as it is faster
