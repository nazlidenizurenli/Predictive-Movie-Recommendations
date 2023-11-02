# Self implemented algorithm
# Takes into account both cosine similarity results
# and pearson similarity results
# Gives the better alorithm (cosine simialrity) a higher
# weight than pearson to improve MAE reusults

import sys
from output_data import write_to_file2, write_to_file

# weight that each algorihtm will recieve in
# average of each preduction
cos_weight = 1.2
pea_weight = 0.8

pearson5 = open('pearson_outputs/result5.txt')

pearson_ratings = [[] for i in range(100)]
for line in pearson5:
    line = [float(item) for item in line.split()]
    pearson_ratings[int(line[0]) - 201].append(line[2])

pearson5.close()

cosine_ratings = [[] for i in range(100)]
cosine_5 = open('cosine_outputs/result5.txt')
for line in cosine_5:
    line = [float(item) for item in line.split()]
    cosine_ratings[int(line[0]) - 201].append(line[2])

cosine_5.close()

test5_target_indexes = [[] for i in range(100)]
with open('test5.txt', 'r')  as file:
    for line in file:

        data = [int(num) for num in line.split()]
        user_id = data[0]
        movie_id = data[1]
        movie_rating = data[2]

        if movie_rating is 0:
            test5_target_indexes[user_id - 201].append(movie_id)

file.close()

average_ratings = []

for i, user in enumerate(pearson_ratings):
    user_ratings = []
    for j, rating in enumerate(user):
        user_ratings.append(((pearson_ratings[i][j]*pea_weight)+(cosine_ratings[i][j]*cos_weight))/2)
    average_ratings.append(user_ratings)

print average_ratings

write_to_file2(average_ratings, test5_target_indexes, 201, 'result5.txt')

#########################################################################

pearson10 = open('pearson_outputs/result10.txt')
pearson_ratings = [[] for i in range(100)]
for line in pearson10:
    line = [float(item) for item in line.split()]
    pearson_ratings[int(line[0]) - 301].append(line[2])
pearson10.close()

cosine_ratings = [[] for i in range(100)]
cosine_10 = open('cosine_outputs/result10.txt')
for line in cosine_10:
    line = [float(item) for item in line.split()]
    cosine_ratings[int(line[0]) - 301].append(line[2])
cosine_10.close()

test10_target_indexes = [[] for i in range(100)]
with open('test10.txt', 'r')  as file:
    for line in file:

        data = [int(num) for num in line.split()]
        user_id = data[0]
        movie_id = data[1]
        movie_rating = data[2]

        if movie_rating is 0:
            test10_target_indexes[user_id - 301].append(movie_id)

file.close()

average_ratings = []

for i, user in enumerate(pearson_ratings):
    user_ratings = []
    for j, rating in enumerate(user):
        user_ratings.append(((pearson_ratings[i][j]*pea_weight)+(cosine_ratings[i][j]*cos_weight))/2)
    average_ratings.append(user_ratings)

print average_ratings

write_to_file2(average_ratings, test10_target_indexes, 301, 'result10.txt')

##########################################################################

pearson20 = open('pearson_outputs/result20.txt')
pearson_ratings = [[] for i in range(100)]
for line in pearson20:
    line = [float(item) for item in line.split()]
    pearson_ratings[int(line[0]) - 401].append(line[2])
pearson20.close()

cosine_ratings = [[] for i in range(100)]
cosine_20 = open('cosine_outputs/result20.txt')
for line in cosine_20:
    line = [float(item) for item in line.split()]
    cosine_ratings[int(line[0]) - 401].append(line[2])
cosine_20.close()

test20_target_indexes = [[] for i in range(100)]
with open('test20.txt', 'r')  as file:
    for line in file:

        data = [int(num) for num in line.split()]
        user_id = data[0]
        movie_id = data[1]
        movie_rating = data[2]

        if movie_rating is 0:
            test20_target_indexes[user_id - 401].append(movie_id)
file.close()

average_ratings = []

for i, user in enumerate(pearson_ratings):
    user_ratings = []
    for j, rating in enumerate(user):
        user_ratings.append(((pearson_ratings[i][j]*pea_weight)+(cosine_ratings[i][j]*cos_weight))/2)
    average_ratings.append(user_ratings)

print average_ratings

write_to_file2(average_ratings, test20_target_indexes, 401, 'result20.txt')
