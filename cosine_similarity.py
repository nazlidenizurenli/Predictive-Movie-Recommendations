# user based collaborative filtering algorithm
#
#
#
import sys
from math import sqrt
from numpy import dot
import numpy as np
from similarity import cosine_similarity
from output_data import write_to_file2, write_to_file
from math import log

""" GLOBAL VARIABLES """
# list where training data is stored from train.txt
users = []

# test users lists starting at index 200, 300, and 400
# indexing continuation of 'users' list
test5_users = [[0 for i in range(1000)] for j in range(100)]      # creates list of lists
test10_users = [[0 for i in range(1000)] for j in range(100)]
test20_users = [[0 for i in range(1000)] for j in range(100)]

test5_rated_indexes = [[] for i in range(100)]
test5_target_indexes = [[] for i in range(100)]

test10_rated_indexes = [[] for i in range(100)]
test10_target_indexes = [[] for i in range(100)]

test20_rated_indexes = [[] for i in range(100)]
test20_target_indexes = [[] for i in range(100)]

"""" GET DATA FROM FILES """

# open and parse numbers from files into lists of user ratings
with open('train.txt', 'r') as file:
    for line in file:
        ratings = [int(num) for num in line.split()]
        users.append(ratings)

file.close()

# open and get data form test5.txt file
with open('test5.txt', 'r')  as file:

    for line in file:

        data = [int(num) for num in line.split()]
        user_id = data[0]
        movie_id = data[1]
        movie_rating = data[2]

        #print user_id, movie_id, movie_rating

        # might cuase indexing error here
        test5_users[user_id - 201][movie_id - 1] = movie_rating      # set movie rating

        if movie_rating is 0:
            test5_target_indexes[user_id - 201].append(movie_id)

        else:
            test5_rated_indexes[user_id - 201].append(movie_id)

file.close()


# open and get data from test10.txt file
with open('test10.txt', 'r') as file:

    for line in file:

        data = [int(num) for num in line.split()]
        user_id = data[0]
        movie_id = data[1]
        movie_rating = data[2]

        test10_users[user_id - 301][movie_id - 1] = movie_rating    # set movie rating

        if movie_rating is 0:
            test10_target_indexes[user_id - 301].append(movie_id)

        else:
            test10_rated_indexes[user_id - 301].append(movie_id)

file.close()

# open and get data from test20.txt file
with open('test20.txt', 'r') as file:

    for line in file:

        data = [int(num) for num in line.split()]
        user_id = data[0]
        movie_id = data[1]
        movie_rating = data[2]

        test20_users[user_id - 401][movie_id - 1] = movie_rating    # set movie rating

        if movie_rating is 0:
            test20_target_indexes[user_id - 401].append(movie_id)

        else:
            test20_rated_indexes[user_id - 401].append(movie_id)

file.close()

#########################################################################################
test_user_averages = []
threshold = 0.84
k_users = 160
#########################################################################################
cosine_similarities = []

for i in range(100):
    test_user_sims = []
    for j in range(200):
        test_user_sims.append(cosine_similarity(users[j], test5_users[i]))

    cosine_similarities.append(test_user_sims)


for i, row in enumerate(cosine_similarities):
    for j, cell in enumerate(row):      # TODO: don't use threshold if only few have non zero weights
        if cell < threshold:
            cosine_similarities[i][j] = 0

all_ratings = []

for k, each_target_user in enumerate(test5_target_indexes):

    final_ratings = []
    for blank_rating in each_target_user:
        weight_sum = 0
        rating = 0
        divisor = 0

        for i, sim in enumerate(cosine_similarities[k]):
            if users[i][blank_rating-1] != 0:
                weight_sum+= sim * users[i][blank_rating - 1]
                divisor += sim

        #print divisor

        if divisor == 0:
            weight_sum = 3
            divisor = 1


        rating = weight_sum / divisor
        print rating
        final_ratings.append(rating)

    all_ratings.append(final_ratings)

write_to_file2(all_ratings, test5_target_indexes, 201,'result5.txt')

# #####################################################################################

cosine_similarities = []

for i in range(100):
    test_user_sims = []
    for j in range(200):
        test_user_sims.append(cosine_similarity(users[j], test10_users[i]))

    cosine_similarities.append(test_user_sims)

#print cosine_similarities
for i, row in enumerate(cosine_similarities):
    for j, cell in enumerate(row):
        if cell < threshold:
            cosine_similarities[i][j] = 0

all_ratings = []

for k, each_target_user in enumerate(test10_target_indexes):

    final_ratings = []
    for blank_rating in each_target_user:
        weight_sum = 0
        rating = 0
        divisor = 0

        for i, sim in enumerate(cosine_similarities[k]):
            if users[i][blank_rating-1] != 0:
                weight_sum+= sim * users[i][blank_rating - 1]
                divisor += sim

        if divisor == 0:
            weight_sum = 3
            divisor = 1


        rating = weight_sum / divisor
        final_ratings.append(rating)

    all_ratings.append(final_ratings)

write_to_file2(all_ratings, test10_target_indexes, 301,'result10.txt')

####################################################################################

cosine_similarities = []

for i in range(100):
    test_user_sims = []
    for j in range(200):
        test_user_sims.append(cosine_similarity(users[j], test20_users[i]))

    cosine_similarities.append(test_user_sims)

#print cosine_similarities
for i, row in enumerate(cosine_similarities):
    for j, cell in enumerate(row):
        if cell < threshold:
            cosine_similarities[i][j] = 0

all_ratings = []
for k, each_target_user in enumerate(test20_target_indexes):

    final_ratings = []
    for blank_rating in each_target_user:
        weight_sum = 0
        rating = 0
        divisor = 0

        for i, sim in enumerate(cosine_similarities[k]):
            if users[i][blank_rating-1] != 0:
                weight_sum+= sim * users[i][blank_rating - 1]
                divisor += sim

        if divisor == 0:
            weight_sum = 3
            divisor = 1

        rating = weight_sum / divisor
        final_ratings.append(rating)

    all_ratings.append(final_ratings)


write_to_file2(all_ratings, test20_target_indexes, 401,'result20.txt')
