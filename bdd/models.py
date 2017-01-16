from django.db import models

class Film(models.Model):
    title = models.TextField()
    release_date = models.TextField()
    video_release_date = models.TextField()
    imdb_url = models.TextField()
    
    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey('User')
    movie = models.ForeignKey('Film')
    rating = models.IntegerField()

    def __str__(self):
        return self.movie.title

class User(models.Model):
    age = models.TextField()
    gender = models.TextField()
    occupation = models.TextField()
    zip_code = models.TextField()

    def __str__(self):
        return self.age
