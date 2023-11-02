from __future__ import division
import sys
from math import sqrt
import numpy as np
from output_data import write_to_file2, write_to_file
from math import log

""" getting training data """
test_file = sys.argv[1]
print test_file


print 'Parsing training data...'
# all training data stored here
# 2-D Matrix
users = []
# open and parse numbers from files into lists of user ratings
with open('train.txt', 'r') as file:
    for line in file:
        ratings = [int(num) for num in line.split()]
        users.append(ratings)

file.close()

""" Get starting test user index """
starting_index = 0

with open(test_file, 'r') as file:
    line = file.readline()
    first_line = [int(num) for num in line.split()]
    starting_index = first_line[0]

#print 'start user index: ', starting_index
file.close()

users_non_rated_movie_indexes = [[] for i in range(100)]
test_users = [[0 for i in range(1000)] for j in range(100)]      # creates list of lists


with open(test_file, 'r')  as file:

    for line in file:

        data = [int(num) for num in line.split()]
        user_id = data[0]
        movie_id = data[1]
        movie_rating = data[2]

        test_users[user_id - starting_index][movie_id - 1] = movie_rating      # set movie rating

        if movie_rating is 0:
            users_non_rated_movie_indexes[user_id - starting_index].append(movie_id)
        #else:
            #test5_rated_indexes[user_id - 201].append(movie_id)

file.close()

""" Calculate IUF """
print 'Calculating IUF...'

counts = [0 for i in range(1000)]
iuf = [1 for i in range(1000)]

for user in users:
    for i, rating in enumerate(user):
        if rating > 0:
            counts[i] += 1

#print counts

for i, count in enumerate(counts):
    if count == 0:
        continue
    else:
        iuf[i] = log(200/count)

for i, user in enumerate(users):          # IUF Implemented
    for j, rating in enumerate(user):
        users[i][j] *= iuf[j]


""" Calculating average of each training user """
print 'Calculating Average Rating of each training user...'

# Returns the average of a user vector
def get_average_of_user(user):
    subset_of_user = [rating for rating in user if rating > 0]
    average = np.mean(subset_of_user)
    return average

# create list of an average for every user in training data
# populate with an average for every training user
# 1-D list of size 200 (one average for every training user)
train_user_averages = []

for user in users:
    train_user_averages.append(get_average_of_user(user))


""" Calculating weights """
print 'Calculating Weights of Each Test User Against Each Training User...'

def get_weight(test_user, train_user):
    num = 0
    den_1 = 0
    den_2 = 0

    test_user_average = get_average_of_user(test_user)
    train_user_average = get_average_of_user(train_user)

    for i, movie_rating in enumerate(test_user):

        if movie_rating > 0 and train_user[i] > 0:
            num += (movie_rating - test_user_average) * (train_user[i] - train_user_average)
            den_1 += ((movie_rating - test_user_average) ** 2)
            den_2 += ((train_user[i] - train_user_average) ** 2)

    den  = sqrt(den_1) * sqrt(den_2)
    if den == 0:
        return 0

    weight = num / den
    return weight

# should be height: 100. width: 200
all_weights = []

for i, test_user in enumerate(test_users):
    weights_per_user = []

    for user in users:
        weight = get_weight(test_user, user)
        # weight *= abs(weight)** 1.5     # CASE AMPLIFICATION
        weights_per_user.append(weight)

    all_weights.append(weights_per_user)


""" Predict ratings """
print 'Predicting Ratings... '

all_ratings = []

for i, test_user in enumerate(test_users):
    user_ratings = []
    for j, nonrated_movie_index in enumerate(users_non_rated_movie_indexes[i]):

        top = 0
        bot = 0

        for k, weight in enumerate(all_weights[i]):
            if users[k][nonrated_movie_index -1] != 0 :
                top += ((users[k][nonrated_movie_index - 1] - get_average_of_user(users[k])) * weight)
                bot += abs(weight)

        rating = get_average_of_user(test_user)
        # print 'numerator: ', top
        # print 'denomenator: ', bot
        if bot > 0:
            rating = get_average_of_user(test_user) + (top/bot)
            if rating > 5:
                rating = 5
            elif rating < 1:
                rating = 1

        # print get_average_of_user(test_user), '+', '(', top, ' / ', bot, ')', '=', rating
        user_ratings.append(rating)

    # print '----- end of test_user ', i,  '-----'
    all_ratings.append(user_ratings)


result_file = ''
if test_file == 'test5.txt':
    result_file = 'result5.txt'
if test_file == 'test10.txt':
    result_file = 'result10.txt'
if test_file == 'test20.txt':
    result_file = 'result20.txt'

print 'Writing to output file... '
write_to_file2(all_ratings, users_non_rated_movie_indexes, starting_index, result_file)
print 'Done!'
