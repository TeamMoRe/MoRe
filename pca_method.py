import sys
import numpy as np
from bdd.models import Film, User, Rating


def precision_level_to_rank(eigen_values, precision=0.95):
    abs_values = abs(eigen_values)
    goal, k = sum(abs_values) * precision, 0
    somme = 0
    while somme < goal:
        somme += eigen_values[k]
        k += 1
    return k+1


def predict_all(M):
    column_moy_vect = np.array([[np.sum(movie_rating) / (np.count_nonzero(movie_rating)+1*(np.count_nonzero(movie_rating)==0))] for movie_rating in M.transpose()])
    M_std = np.copy(M)
    M_std.flags.writeable = True
    for j in range(M_std.shape[1]):
        column = M_std[:, j]
        column[column == 0] = column_moy_vect[j]
    moy_vect = np.array([[np.sum(user_rating) / np.count_nonzero(user_rating)] for user_rating in M_std])
    # moyenne = np.mean(M)
    M_std = (M - moy_vect)
    cov_mat = np.cov(M_std)
    eig_vals, eig_vects = np.linalg.eigh(cov_mat)
    eig_vals, eig_vects = np.fliplr([eig_vals])[0], np.fliplr([eig_vects])[0]
    V = np.array(eig_vects[:precision_level_to_rank(eig_vals, precision=0.2)]).transpose()
    M_prime = (V.transpose()).dot(M_std)
    M_pred = V.dot(M_prime)
    M_pred += moy_vect - np.mean(M_pred)
    M_pred[M_pred > 5] = 5
    M_pred[M_pred < 1] = 1
    return M_pred


def ranking(a, movies, M):
    grades = predict_all(M)[a - 1, :]
    not_watched = [movie_index for movie_index in range(len(M[a - 1])) if M[a - 1, movie_index] == 0]
    grades = [grades[i] for i in not_watched]
    titles_not_watched = [movies[i].title for i in not_watched]
    return sorted(zip(titles_not_watched, grades), key=lambda x: x[1], reverse=True)

