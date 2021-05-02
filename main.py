import copy
import random
from model import *
from DAO import *


def input_data():
    adjacency_list = []

    edges_file = '../brightkite/Brightkite_edges.txt'
    # checkin_file = '../brightkite/Brightkite_totalCheckins.txt'

    f1 = open(edges_file, "r")
    lines = f1.readlines()
    curr = -1
    for line in lines:
        node1, node2 = map(int, line.strip().split())
        if node1 != curr:
            curr = node1
            adjacency_list.append([])
        adjacency_list[curr].append(node2)

    # f2 = open(checkin_file, "r")
    # lines = f2.readlines()
    # curr_usr = 0
    # curr_time_list = []
    # curr_loc_list = []
    # for line in lines:
    #     line0 = line.strip().split()
    #     if len(line0) == 5 and line0[2] != '0.0':
    #         usr_id, time, _, _, loc_id = line.strip().split()
    #         if int(usr_id) == curr_usr:
    #             curr_time_list.append(time)
    #             curr_loc_list.append(loc_id)
    #         else:
    #             checkin_time_list.append(copy.deepcopy(curr_time_list))
    #             check_loc_list.append(copy.deepcopy(curr_loc_list))
    #             curr_usr += 1
    #             while int(usr_id) != curr_usr:
    #                 checkin_time_list.append([])
    #                 check_loc_list.append([])
    #                 curr_usr += 1
    #             curr_time_list = [time]
    #             curr_loc_list = [loc_id]
    # checkin_time_list.append(copy.deepcopy(curr_time_list))
    # check_loc_list.append(copy.deepcopy(curr_loc_list))
    print("Reading Data Complete")
    return adjacency_list


def random_remove(adjacency_list, frac):
    usr_num = len(adjacency_list)
    remove_num, target_usr = 0, 0
    usr_friend = []
    while remove_num <= 10:
        # target_usr = random.randint(0, usr_num - 1)
        target_usr = 30
        usr_friend = adjacency_list[target_usr]
        friend_num = len(usr_friend)
        remove_num = int(frac * friend_num)
    target_friend = random.sample(usr_friend, remove_num)
    print("Target user is user", target_usr, ", Removing ", remove_num, "edges:")
    print(target_friend)

    for i in target_friend:
        adjacency_list[target_usr].remove(i)
        adjacency_list[i].remove(target_usr)
    return target_usr, target_friend, adjacency_list

def remove_all_mobility_friends(adjacency_list, target):
    result_5_min = query_database(build_sql(target, 5))
    count = 0
    for i in result_5_min:
        if i[0] in adjacency_list[target]:
            adjacency_list[i].remove(i[0])
            count += 1
    print("Removing",count)
    return adjacency_list




if __name__ == '__main__':

    baseline = True

    adjacency_list = input_data()
    tar, friend, adj = random_remove(adjacency_list, 0.1)
    adj = remove_all_mobility_friends(adj, tar)

    model = Model(tar)
    model.input_data(adj)
    model.filtering()
    recomm_list, recomm_list_baseline = model.run()

    cnt = 0
    for i in recomm_list:
        if i in friend:
            cnt += 1
    print('Recommendation friends', recomm_list)
    print('Find', cnt, 'friends')

    if baseline:
        cnt = 0
        for i in recomm_list_baseline:
            if i in friend:
                cnt += 1
        print('Baseline - Recommendation friends', recomm_list_baseline)
        print('Baseline - Find', cnt, 'friends')

