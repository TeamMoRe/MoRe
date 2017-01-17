import numpy as np
import sys
import os
sys.path.append(os.path.dirname(__file__))
import time
import data_extraction
t1= time.clock()
users, movies, ratings = data_extraction.get_data("ua.base")

M = np.zeros((len(users), len(movies)))
for rating in ratings:
    M[rating.user_id - 1][rating.movie_id - 1] = rating.note


def precision_level_to_rank(eigen_values, precision=0.95):
    abs_values = abs(eigen_values)
    goal, k = sum(abs_values) * precision, 0
    somme = 0
    while somme < goal:
        somme += eigen_values[k]
        k += 1
    return k+1


def predict_all():
    # 1
    column_moy_vect = np.array([[np.sum(movie_rating) / (np.count_nonzero(movie_rating)+1*(np.count_nonzero(movie_rating)==0))] for movie_rating in M.transpose()])
    M_std = np.copy(M)
    M_std.flags.writeable = True
    for j in range(M_std.shape[1]):
        column = M_std[:, j]
        column[column == 0] = column_moy_vect[j]
    # 2
    moy_vect = np.array([[np.mean(user_rating)] for user_rating in M_std])
    # moyenne = np.mean(M)
    M_std = (M - moy_vect)
    # 3
    cov_mat = np.cov(M_std)
    eig_vals, eig_vects = np.linalg.eigh(cov_mat)
    eig_vals, eig_vects = np.fliplr([eig_vals])[0], np.fliplr([eig_vects])[0]
    V = np.array(eig_vects[:precision_level_to_rank(eig_vals, precision=.19)]).transpose()
    # 4
    M_prime = (V.transpose()).dot(M_std)
    M_pred = V.dot(M_prime)
    # 5
    M_pred += moy_vect - np.mean(M_pred)
    M_pred[M_pred > 5] = 5
    M_pred[M_pred < 1] = 1
    return M_pred


def ranking(a):
    grades = predict_all()[a - 1, :]
    not_watched = [i for i in range(len(M[a - 1])) if M[a - 1, i] == 0]
    grades = [grades[i] for i in not_watched]
    titles_not_watched = [movies[i].title for i in not_watched]
    return sorted(zip(titles_not_watched, grades), key=lambda x: x[1], reverse=True)

print(ranking(1)[:20])
print("temps pour calculer un ranking : " + str(time.clock() - t1))

from sklearn.metrics import mean_absolute_error, mean_squared_error
true_ratings = data_extraction.get_data("ua.test")[2]
predicted_grades = predict_all()
print(np.std(predicted_grades))
predicted_list = []
true_grades = []
for rating in true_ratings:
    predicted_list.append(predicted_grades[rating.user_id - 1, rating.movie_id - 1])
    true_grades.append(rating.note)
print("mean absolute error :  " + str(mean_absolute_error(true_grades, predicted_list)))
print("root mean squared error :  " + str(np.sqrt(mean_squared_error(true_grades, predicted_list))))



