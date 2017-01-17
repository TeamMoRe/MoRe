__author__ = 'Etienne'
from Lib import statistics
import sys
import os
sys.path.append(os.path.dirname(__file__))
import data_extraction
import numpy as np
import time
t1 = time.clock()
users, movies, ratings = data_extraction.get_data("ua.base")


def double_dict(ratings):
    user_ratings_dict, movie_rating_dict = {}, {}
    for rating in ratings:
        if rating.user_id not in user_ratings_dict:
            user_ratings_dict[rating.user_id] = {}
        if rating.movie_id not in movie_rating_dict:
            movie_rating_dict[rating.movie_id] = {}

        user_ratings_dict[rating.user_id][rating.movie_id] = rating.note
        movie_rating_dict[rating.movie_id][rating.user_id] = rating.note

    return user_ratings_dict, movie_rating_dict

user_ratings_dict, movie_ratings_dict = double_dict(ratings)


def users_who_rated_common_item_with(a):
    a_history = set(user_ratings_dict[a].keys())
    user_list = []
#    for user in user_ratings_dict.keys():
#        if not a_history.isdisjoint(set(user_ratings_dict[a].keys())):
#            user_list.append(user)
    for pic in a_history:
        user_list += movie_ratings_dict[pic].keys()
    return set(user_list) - set([a])


# similitude entre deux utilisateurs
def sim_user(a, b):
    if a == b:
        return 1
    P = set(user_ratings_dict[a].keys()) & set(user_ratings_dict[b].keys())#set of movies seen by both users
    if P == set():
        return 0
    sim = 0
    mean_a, mean_b = 0, 0
    for p in P:
        mean_a += user_ratings_dict[a][p]
        mean_b += user_ratings_dict[b][p]
    mean_a, mean_b = mean_a/len(P), mean_b/len(P)
    stdeviation_a, stdeviation_b = 0, 0
    for p in P:
        sim += (user_ratings_dict[a][p] - mean_a)*(user_ratings_dict[b][p] - mean_b)
        stdeviation_a += (user_ratings_dict[a][p] - mean_a)**2
        stdeviation_b += (user_ratings_dict[b][p] - mean_b)**2
    if stdeviation_a * stdeviation_b == 0:
        return 0
    return sim/((stdeviation_a*stdeviation_b)**.5)



def predict(a, p):
    assert p not in user_ratings_dict[a].keys()
    prediction, sum_of_sim = 0, 0
    try:
        N = set(movie_ratings_dict[p]) & users_who_rated_common_item_with(a)
    except:
        return 3
    for user in N:
        sim_a_user = similitude[a-1][user-1] #sim_user(a, user)
        prediction += sim_a_user*(user_ratings_dict[user][p] - statistics.mean(user_ratings_dict[user].values()))
        sum_of_sim += abs(sim_a_user)
    if sum_of_sim == 0:
        return 0
    return statistics.mean(user_ratings_dict[a].values()) + prediction/sum_of_sim


# tests
# print(sim_user(1, 2))
# a_pas_vu = set(ratings_by_movies.keys()) - set(id_movie_list(ratings_by_users[2]))
# print(predict(2, list(a_pas_vu)[0]))



def ranking(a):

    not_watched = list(set(movie_ratings_dict.keys()) - set(user_ratings_dict[a].keys()))
    rank = {}
    for p in not_watched:
        rank[p] = predict(a, p)
    pred_max, pred_min = max(rank.values()), min(rank.values())
    factor = 4/(pred_max - pred_min)
    return [(movies[pic].title, 1 - pred_min + rank[pic] * factor) for pic in sorted(rank, key=rank.__getitem__, reverse=True)]

def similitude_func():
    nb_users = len(users)
    similitude = []
    for i in range(nb_users):
        similitude.append([])
        for j in range(nb_users):
            if i <= j:
                similitude[i].append((sim_user(i+1, j+1)))
            else:
                similitude[i].append(similitude[j][i])
    return similitude


similitude = similitude_func()
# print(predict(3, 1))
print(ranking(1)[:20])
print("temps pour calculer un ranking :  " + str(time.clock() - t1))

# precision test
from sklearn.metrics import mean_absolute_error, mean_squared_error
true_ratings = data_extraction.get_data("ua.test")[2]
predicted_grades = []
true_grades = []
for rating in true_ratings:
    p = predict(rating.user_id, rating.movie_id)
    predicted_grades.append(p*(1 <= p <= 5) + 1*(p < 1) + 5*(5 < p))
    true_grades.append(rating.note)

print("mean absolute error :  " + str(mean_absolute_error(true_grades, predicted_grades)))
print("root mean squared error :  " + str(np.sqrt(mean_squared_error(true_grades, predicted_grades))))
