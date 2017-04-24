import sys


# reload(sys)

# sys.setdefaultencoding('utf-8')
import itertools

candid_freq= list()
output_file = open("jitesh_chawla_multihash.txt",'w')

def create_hashfunc1(combination,bucketsize):
    sum1=0
    for item in combination:
        for i in item:
            sum1+= ord(i)
    return sum1%bucketsize

def create_hashfunc2(combination,bucketsize):
    sum2=0
    for item in combination:
        for i in item:
            sum2+= ord(i)+15
    return sum2%bucketsize

def create_hashtable(basket, subset_length):
    for combination in list(itertools.combinations(basket, subset_length)):
        # print(combination)
        hashvalue1 = create_hashfunc1(combination, bucketsize)
        hashvalue2 = create_hashfunc2(combination, bucketsize)
        bitvector1[hashvalue1] += 1
        bitvector2[hashvalue2] += 1

    return bitvector1,bitvector2

if __name__ == '__main__':

    inputfile = sys.argv[1]
    support = int(sys.argv[2])
    bucketsize = int(sys.argv[3])
    item_count_dict = dict()
    item_count_dict2 = dict()
    frequent_singleton = list()
    frequent_items_0 = list()
    frequent_items_1 = list()
    frequent_items_future = list()
    candidate_items1 = dict()
    candidate_items2 = dict()
    subset_length = 2
    c1 = 0
    bitvector1 = list()
    bitvector2 = list()

    flag = True
    bitvector1 = [0] * bucketsize
    bitvector2 = [0] * bucketsize
    for line in open(inputfile):
        line = line.rstrip('\n')
        basket = line.split(',')
        basket.sort()
        #print(basket)
        for item in basket:
            if item in item_count_dict:
                item_count_dict[item] += 1
            else:
                item_count_dict[item] = 1

    for key,value in item_count_dict.iteritems():
        if value>=support:
            c1 += 1
            frequent_singleton.append(key)
            item_count_dict2[key] = c1
    # print("\n")
    output_file.write(str(sorted(frequent_singleton)) + "\n\n" )
    print(sorted(frequent_singleton))
    print("\n")
    # print(item_count_dict2.items())
    # print(item_count_dict2["b"])
    flag=True
    # print(bitvector1)
    # print(bitvector2)

    while flag:

        for line in open(inputfile):
            line = line.rstrip('\n')
            basket = line.split(',')
            basket.sort()
            for item in basket:
                if item in item_count_dict:
                    item_count_dict[item] += 1
                else:
                    item_count_dict[item] = 1
            bitvector1, bitvector2 = create_hashtable(basket, subset_length)
        for i in range(len(bitvector1)):
            candidate_items1[i]=bitvector1[i]
        # print(candidate_items1)
        for i in range(len(bitvector2)):
            candidate_items2[i] = bitvector2[i]
        # print(candidate_items2)
        for index, count in enumerate(bitvector1):
            if count >= support:
                bitvector1[index] = 1
            else:
                bitvector1[index] = 0
        # print(bitvector1)
        for index, count in enumerate(bitvector2):
            if count >= support:
                bitvector2[index] = 1
            else:
                bitvector2[index] = 0
        # print(bitvector2)

        item_count_dict1=dict()
        for combination in list(itertools.combinations(frequent_singleton , subset_length)):
            # print combination
            hashvalue1 = create_hashfunc1(combination, bucketsize)
            hashvalue2 = create_hashfunc2(combination, bucketsize)
            # print(hashvalue1,hashvalue2)
            # print(bitvector2[hashvalue2])
            if bitvector1[hashvalue1] == 1 & bitvector2[hashvalue2] ==1:
                for line in open(inputfile):
                    line = line.rstrip('\n')
                    basket = line.split(',')
                    basket.sort()
                    # print(combination)
                    if set(combination).issubset(basket):

                        if combination in item_count_dict1:
                            item_count_dict1[combination] += 1
                        else:
                            item_count_dict1[combination] = 1
                    frequent_items_1.append(combination)
        # print frequent_items_1
        frequent_double=[]
        for key, value in item_count_dict1.items():
            if value >= support:
                frequent_double.append(sorted(list(key)))

        # print(sorted(frequent_double))
        # print("\n")
        subset_length+=1
        for i in range(len(frequent_double)):
            for j in range(len(frequent_double[i])):
                candid_freq.append(frequent_double[i][j])
        # print(list(set(candid_freq)))
        frequent_singleton=list(set(candid_freq))
        # print(sorted(frequent_singleton))


        if not frequent_double:
            break
        else:
            print(candidate_items1)
            print(candidate_items2)
            print(sorted(frequent_double))
            print("\n")
            output_file.write(str(candidate_items1) + "\n" + str(candidate_items1) + "\n" + str(sorted(frequent_double)) + "\n\n" )
    # print(combination)
    # for line in open(inputfile):
    #     line = line.rstrip('\n')
    #     basket = line.split(',')
    #     basket.sort()
    #     for item_set in list(itertools.combinations(basket, subset_length + 1)):
    #         print(item_set)


    # for combination in list(itertools.combinations(frequent_items_1 , subset_length+1)):
    #     hashvalue1 = create_hashfunc1(combination, bucketsize)
    #     hashvalue2 = create_hashfunc2(combination, bucketsize)
    #     print(hashvalue1, hashvalue2)
    #     # print(bitvector2[hashvalue2])
    #     if bitvector1[hashvalue1] == 1 & bitvector2[hashvalue2] == 1:
    #         frequent_items_future.append(combination)
    # print(frequent_items_future)
    # for line in open(inputfile):
    #     inplist1.append(line.strip())
    #     inplist2.append(line.strip())
    # for i in range(0, len(inplist1)):
    #     inplist3.append(inplist1[i].split(","))
    # print(inplist3)
    # inp_dict = {}
    # for i in range(0, len(inplist1)):
    #     for j in range(0, len(inplist1[i].split(","))):
    #         count = 0
    #         char1 = inplist1[i].split(",")[j]
    #         for s in range(0, len(inplist1)):
    #             for k in range(0, len(inplist1[s].split(","))):
    #                 char2 = inplist2[s].split(",")[k]
    #                 if char1 == char2:
    #                     count += 1
    #                 if count >= support:
    #                     inp_dict[inplist1[i].split(",")[j]] = count
    # for k in inp_dict.keys():
    #     i = inp_dict.keys().index(k)
    #     inp_dict[k] = i + 1
    # print(inp_dict)
    # frequentsingletons = sorted(inp_dict.keys())
    # print(frequentsingletons)
    # multihash(sys.argv[1], int(sys.argv[2]), int(sys.argv