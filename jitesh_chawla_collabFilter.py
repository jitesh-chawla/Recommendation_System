import pandas as pd
import numpy as nm
import operator
import csv
import sys  # used for passing in the argument
pd.set_option('max_columns', 50)

output_file = open("jitesh_chawla_collabFilter.txt",'w')

# Initializations
list_of_users = []
list_of_movies = []
dict_user_movie = {}
avg_ratings_dict = {}
sorted_dict= {}
l1 = []
pearson_correlation_value = 0
inputfile = str(sys.argv[1])

file_name = inputfile  # filename is argument 1
with open(file_name, 'rU') as f:  # opens PW file
    reader = csv.reader(f)
    data = list(list(rec) for rec in csv.reader(f, delimiter='\t'))  # reads csv into a list of lists

for i in range(len(data)):
    for j in range(len(data[i])):
        list_of_users.append(data[i][0])
        list_of_movies.append(data[i][2])
        dict_user_movie[data[i][0]] = data[i][2]

list_of_users = list(set(list_of_users))
list_of_movies = list(set(list_of_movies))

pd.set_option('display.width', 1000)
utility_matrix1 = pd.DataFrame(index=list_of_users, columns=list_of_movies)
utility_matrix2 = pd.DataFrame(index=list_of_users, columns=list_of_movies)
utility_matrix3 = pd.DataFrame(index=list_of_users, columns=list_of_movies)
utility_matrix4 = pd.DataFrame(index=list_of_users, columns=list_of_movies)

for x in data:
    utility_matrix1[x[2]][x[0]] = float(x[1])
    if utility_matrix1[x[2]][x[0]] != 'NaN':
        l1.append(x[2])

avg_ratings_dict = dict(utility_matrix1.mean(axis=1)).copy()
# print(avg_ratings_dict)

for x in data:
    utility_matrix3[x[2]][x[0]] = float(utility_matrix1[x[2]][x[0]]) - avg_ratings_dict[x[0]]
# print(utility_matrix3)

#  Determining the Pearson correlation between two users.
def pearson_correlation(user1,user2):
    corated_movie_set = set()
    pearson_num = 0
    pearson_denom1 = 0
    pearson_denom2 = 0
    pearson_denom3 = 0
    user1_list = []
    user2_list = []
    for x in data:
        if not nm.isnan(utility_matrix1[x[2]][user1]):
            user1_list.append(x[2])
        if not nm.isnan(utility_matrix1[x[2]][user2]):
            user2_list.append(x[2])
    corated_movie_set = set(user1_list) & set(user2_list)
    # print(corated_movie_set)
    utility_matrix2 = utility_matrix1.loc[[user1,user2],corated_movie_set]
    utility_matrix2['avg'] = utility_matrix2.mean(axis=1)
    for movie in corated_movie_set:
        pearson_num += float(utility_matrix2[movie][user1]-utility_matrix2['avg'][user1]) * float(utility_matrix2[movie][user2]-utility_matrix2['avg'][user2])
        pearson_denom1 += float(utility_matrix2[movie][user1]-utility_matrix2['avg'][user1]) ** 2.0
        pearson_denom2 += float(utility_matrix2[movie][user2]-utility_matrix2['avg'][user2]) ** 2.0
    pearson_denom3 += float(nm.sqrt(pearson_denom1)) * float(nm.sqrt(pearson_denom2))
    pearson_correlation_value = float(pearson_num/pearson_denom3)
    # print(pearson_correlation_value)
    return pearson_correlation_value

# Finding the K nearest neighbors for user1.
def K_nearest_neighbors(user1,k):
    k_nearest_list = []
    user_pearson_dict = {}
    for user in list_of_users:
        if user != user1:
            # print(user1, user)
            var_pearson_correlation = pearson_correlation(user1, user)
            # print(var_pearson_correlation)
            user_pearson_dict[user] = var_pearson_correlation
    k_filtered_dict = {}
    for user in user_pearson_dict.keys():
        if not nm.isnan(utility_matrix1[item][user]):
            k_filtered_dict[user] = user_pearson_dict[user]
    k_nearest_list = sorted(dict(sorted(k_filtered_dict.items(), key=operator.itemgetter(0), reverse=False)).items(), key=operator.itemgetter(1), reverse= True)
    # print(k_nearest_list[:k])
    for element in k_nearest_list[:k]:
        print(element[0] + '  ' + str(element[1]))
        output_file.write(element[0] + ' ' + str(element[1]) + "\n")
    Predict(user1, item, k_nearest_list[:k])


#  Predicting the ratings on the basis of the K-nearest-neighbor list obtained.
def Predict(user1, item, k_nearest_list):
    predict_num = 0
    predict_denom = 0
    k_filtered_dict = dict(k_nearest_list)

    for kuser in k_filtered_dict:
        user1_list = []
        user2_list = []
        for x in data:
            if not nm.isnan(utility_matrix1[x[2]][user1]):
                user1_list.append(x[2])
            if not nm.isnan(utility_matrix1[x[2]][kuser]):
                user2_list.append(x[2])
        corated_movie_set = set(user1_list) & set(user2_list)
        # print(corated_movie_set)
        utility_matrix4 = utility_matrix1.loc[[user1, kuser], corated_movie_set]
        utility_matrix4['avg'] = utility_matrix4.mean(axis=1)
        # print(utility_matrix4)
        predict_num +=  k_filtered_dict[kuser] * (utility_matrix1[item][kuser]-utility_matrix4['avg'][kuser])
        predict_denom += abs(k_filtered_dict[kuser])

    prediction= avg_ratings_dict[user1] + (predict_num/predict_denom)
    # print(k_filtered_dict)
    print(prediction)
    output_file.write(str(prediction))
    return k_nearest_list

# Input Parameters
if __name__ == '__main__':
    user1=str(sys.argv[2])
    item = str(sys.argv[3])
    k= int(sys.argv[4])
    K_nearest_neighbors(user1,k)