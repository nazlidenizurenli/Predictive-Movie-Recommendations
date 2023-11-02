import sys
import numpy as np
from similarity import cosine_similarity
from math import sqrt
from output_data import write_to_file2

# Get input test file
test_file = sys.argv[1]
result_file = ''

# Define input and output text files
if test_file == 'test5.txt':
    result_file = 'result5.txt'
elif test_file == 'test10.txt':
    result_file = 'result10.txt'
elif test_file == 'test20.txt':
    result_file = 'result20.txt'
else:
    print 'TEST FILE: not valid!'

""" Parse Data """
print 'Parsing test and training data... '

# Parse training data
# Crate matrix of every training user's rating (200)
# for every movie (1000)
train_movies = [[] for i in range(1000)]

with open('train.txt', 'r') as file:
    for line in file:
        ratings = [int(num) for num in line.split()]

        for i, rating in enumerate(ratings):
            train_movies[i].append(ratings[i])
file.close()

# Parse test data
# Create matrix for every movie to be rated (1000)
# using each test user's rating (200)
test_movies = [[0 for i in range(100)] for j in range(1000)]
test_ratings = [[] for i in range(100)]
target_movies = [[] for i in range(100)]
test_rated_movies = [[] for i in range(100)]

# Find starting index via test_file first line
STARTING_INDEX = 0

with open (test_file, 'r') as file:
    line = file.readline()
    first_row = [int(num) for num in line.split()]
    STARTING_INDEX = first_row[0]
file.close()

# Parse test data
with open(test_file, 'r') as file:
    for line in file:
        test_user = [int(num) for num in line.split()]
        test_user_id = test_user[0]     # TODO: fix 'off by 1' error
        test_movie_id = test_user[1]
        test_rating = test_user[2]

        test_movies[test_movie_id - 1][test_user_id - (STARTING_INDEX)] = test_rating

        if test_rating > 0:
            test_ratings[test_user_id - STARTING_INDEX].append(test_rating)
            test_rated_movies[test_user_id - STARTING_INDEX].append(test_movie_id)
        else:
            target_movies[test_user_id - STARTING_INDEX].append(test_movie_id)

file.close()

""" Peform Cosine Similarity """
print 'Calculating cosine similarities... '

# Calculate averages of each train user
# To beused in adjusted_cosine_similarity function

print '>> Calculating train user average ratings...'

average_user_rating = []
users = zip(*train_movies)

for i, train_user in enumerate(users):
    user_subset = [rating for rating in train_user if rating > 0]
    average_user_rating.append(np.mean(user_subset))

# Fucntion calculates adjusted cosine similarity between two movies
def adjusted_cosine_similarity(movie_1, movie_2):
    numerator = 0
    denomenator_1 = 0
    denomenator_2 = 0
    for i in range(200):
        if movie_1[i] != 0 and movie_2[i] != 0:
            numerator += (movie_1[i] - average_user_rating[i]) * (movie_2[i] - average_user_rating[i])
            denomenator_1 += (movie_1[i] - average_user_rating[i]) ** 2
            denomenator_2 += (movie_2[i] - average_user_rating[i]) ** 2

    if denomenator_1 == 0 or denomenator_2 == 0:
        return 0

    denomenator = sqrt(denomenator_1) * sqrt(denomenator_2)
    return numerator/denomenator

# Perform Cosine Similarity for each test_movie in test_movies
# against each train_movie in train_moives
print '>> Calculating test user cosine similarities...'

cosine_similarities = []
for i in range(100):    # for every test user there is
    cos_sims = []
    for target_movie in target_movies[i]:   # for every target movie in each test user
        sims = []
        for test_rated_movie in test_rated_movies[i]:    # for every rated movie in test user
            val = adjusted_cosine_similarity(train_movies[test_rated_movie -1], train_movies[target_movie - 1])
            sims.append(val)
        cos_sims.append(sims)
    cosine_similarities.append(cos_sims)


all_ratings = []
count = 0
for i, active_user in enumerate(cosine_similarities):   # range 100
    test_user_ratings = []
    for j, target_movie_similarities in enumerate(active_user): # range (however many target movies each test user has)
        numerator = 0
        denomenator = 0
        for k, similarity in enumerate(target_movie_similarities):
            if similarity > 0.3:
                numerator += test_ratings[i][k] * similarity
                denomenator += similarity
        if denomenator == 0: # if 0 then return 3 for rating
            numerator = 3
            denomenator = 1
        rating = numerator/denomenator
        count += 1
        test_user_ratings.append(rating)
    all_ratings.append(test_user_ratings)

write_to_file2(all_ratings, target_movies, STARTING_INDEX, result_file)

# END
print 'END'
