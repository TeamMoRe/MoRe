from bdd.models import Film, User, Rating
from django.core.management.base import BaseCommand
import sys
sys.path.append('C:/Users/Anthony Andolfo/Downloads/more/bdd/management/commands')
import data_extraction


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'
    def _create_tags(self):
        dictionnaire_movie = {}
        dictionnaire_user = {}
        data = data_extraction.get_data()
        L = data[1]
        for i in L:
            movie = Film(title = L[i].title, release_date = L[i].release_date, video_release_date = L[i].video_release_date, imdb_url = L[i].imdb_url)
            movie.save()
            dictionnaire_movie[L[i].id] = movie.id
        print("Importation des films reussie")

        H = data[0]
        for h in H:
            user = User(age = H[h].age, gender = H[h].gender, occupation = H[h].occupation, zip_code = H[h].zip_code)
            user.save()
            dictionnaire_user[H[h].id] = user.id
        print("Importation des users reussie")

        K = data[2]
        for k in K:
            movie = Film.objects.get(id = dictionnaire_movie[k.movie_id])
            user = User.objects.get(id = dictionnaire_user[k.user_id])
            note = Rating(user = user, movie = movie, rating = k.note)
            note.save()
        print("Importation des notes reussie")
    
    def handle(self, *args, **options):
        self._create_tags()

    
