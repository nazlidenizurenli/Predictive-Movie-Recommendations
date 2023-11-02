import sys

# Write output raitigns to result file
# Parameters:
#
#       ratings = list of ratings for each title
#       test_target_indexes = list of each target users' wanted movie index rating
#       start_id = id number to start output
#       output_file = name of file of which to output data to

def write_to_file2(ratings, test_target_indexes, start_id, output_file):
    file = open(output_file,'w')
    userid = start_id
    for i, target_indexes in enumerate(test_target_indexes):
        for j, target in enumerate(target_indexes):
            file.write('%s ' %userid)
            file.write('%s ' %target)
            file.write('%s \n' %int(round(ratings[i][j])))
        userid += 1
    file.close()

# Write output ratings to results file (not rounded)
# Parameters:
#
#       ratings = list of ratings for each title
#       test_target_indexes = list of each target users' wanted movie index rating
#       start_id = id number to start output
#       output_file = name of file of which to output data to

def write_to_file(ratings, test_target_indexes, start_id, output_file):
    file = open(output_file,'w')
    userid = start_id
    for i, target_indexes in enumerate(test_target_indexes):
        for j, target in enumerate(target_indexes):
            file.write('%s ' %userid)
            file.write('%s ' %target)
            file.write('%s \n' %(ratings[i][j]))
        userid += 1
    file.close()
