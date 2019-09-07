import pandas as pd
from copy import deepcopy
from itertools import combinations
from copy import deepcopy
from sortedcollections import SortedSet

def get_tuple_indices(ind1):
    return [((str(item),)) for item in ind1]

def generate_possible_ln(candidates_list, level):
    temp = []
    for item in candidates_list: temp+=item
    possible_ls = list(SortedSet(temp))
    #print(possible_ls)
    return list(combinations(possible_ls,level))

    
def candidate_query_generator(ln_index_tuple, data_str):
    temp = list(ln_index_tuple)
    int_query = " ==1 )& ".join('( data["{0}"]'.format(w) for w in temp)+" == 1)"
    return data_str+"["+int_query+"]"

def get_candidates(ln_list, data,support_in_cnt=50, level=2):
    candidates_n = []
    countk  = 0
    for item in generate_possible_ln(ln_list,level):
        if(eval(candidate_query_generator(item,"data")).shape[0])>=support_in_cnt:
            countk+=1
            candidates_n += [item]
#     print(countk)
    return candidates_n, countk

def get_candidates_and_count(filename, support_in_num=50):
    data = pd.read_csv(filename, sep="\t", header=None)
    data = pd.get_dummies(data)
    ctmain = data.shape[0]
    ct = data.sum(axis=0)
    ct2 = ct.shape[0]
    l1 =ct[ct>=support_in_num]
    df1=l1.to_frame()
    df1=df1.T
    ind1=df1.columns
    c1 = get_tuple_indices(ind1)
    cn = deepcopy(c1)
    
    final_candidate_keys = []
    final_candidate_keys += deepcopy(c1)
    candidates_count = {"1":len(c1)}
    level_count = 2  # Intended next level count
    print("Level "+str(1)+" Candidates count "+str(candidates_count["1"]))
    while len(cn) > 1:
        ln = generate_possible_ln(cn, level_count)
        cn, cn_count = get_candidates(ln, data,support_in_num,level_count)
        print("Level "+str(level_count)+" Candidates count "+str(cn_count))
        candidates_count[str(level_count)] = cn_count
        final_candidate_keys += cn
        level_count += 1
    print("Total candidates count "+str(sum(candidates_count.values())))
    return final_candidate_keys, candidates_count

def convert_candidate_tuples(candidates_in_tuples):
    candidates_list = []
    for item in candidates_in_tuples:
        candidates_list += [list(item)]
    return candidates_list
