from Lib import statistics
from bdd.models import Film, User, Rating
from operator import itemgetter


def double_dict(ratings):
    user_ratings_dict, movie_rating_dict = {}, {}
    for rating in ratings:
        if rating.user.id not in user_ratings_dict:
            user_ratings_dict[rating.user.id] = {}
        if rating.movie.id not in movie_rating_dict:
            movie_rating_dict[rating.movie.id] = {}
        user_ratings_dict[rating.user.id][rating.movie.id] = rating.rating
        movie_rating_dict[rating.movie.id][rating.user.id] = rating.rating
    return user_ratings_dict, movie_rating_dict



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
def sim_user(a, b, user_ratings_dict, movie_ratings_dict):
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

def similitude_func(users, user_ratings_dict, movie_ratings_dict):
    nb_users = len(users)
    similitude = []
    for i in range(nb_users):
        similitude.append([])
        for j in range(nb_users):
            if i <= j:
                similitude[i].append((sim_user(i+1, j+1, user_ratings_dict, movie_ratings_dict)))
            else:
                similitude[i].append(similitude[j][i])
    return similitude


def predict(a, p, similitude, user_ratings_dict, movie_ratings_dict):
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


def ranking(a, similitude, user_ratings_dict, movie_ratings_dict, movies):
    not_watched = list(set(movie_ratings_dict.keys()) - set(user_ratings_dict[a].keys()))
    rank = [predict(a, p, similitude, user_ratings_dict, movie_ratings_dict) for p in not_watched]
    not_watched = [movies[p-1].title for p in not_watched]
    pred_max, pred_min = max(rank), min(rank)
    factor = 4/(pred_max - pred_min)
    rank = [(1-pred_min + p*factor) for p in rank]
    return sorted(zip(not_watched, rank), key=lambda x: x[1], reverse = True)



