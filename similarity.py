import sys
from math import sqrt
from numpy import dot
import numpy as np

# Calculate Cosine Similarity of 2 Vectors
# Only account for titles that both rated

def cosine_similarity(user_1, user_2):
    """
    Return cosine similarity of two users in vector form
    Take into account only non-zero values
    Parameters: user_1 & user_2
    """

    numerator = dot(user_1, user_2)
    #print 'dot: ', numerator

    total1 = 0
    for i, item in enumerate(user_1):
        if (user_1[i] * user_2[i]) != 0:
            total1 += user_1[i]* user_1[i]

    total2 = 0
    for j, item in enumerate(user_2):
        if (user_1[j] * user_2[j]) != 0:
            total2 += user_2[j]* user_2[j]

    if total1 == 0:
        return 0
    if total2 == 0:
        return 0

    num_1 = sqrt(total1)
    #print 'num1: ', num_1

    num_2 = sqrt(total2)
    #print 'num2: ', num_2

    denomenator = num_1 * num_2
    #print 'denomenator: ', denomenator

    return numerator/denomenator

# Calculate Cosine similarity
# Include all titles (not just rated titles)

def cosine_similarity2(user_1, user_2):
    """
    Return cosine simialiry of two users in vector form
    Take into account every value
    Parameters: user_1 & user_2
    """
    dot_product = dot(user_1, user_2)
    num_1 = sqrt(dot(user_1, user_1))
    num_2 = sqrt(dot(user_2, user_2))
    return dot_product/(num_1 * num_2)
