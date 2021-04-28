import copy
import random
from model import *


def input_data():
    adjacency_list = []
    checkin_time_list = []
    check_loc_list = []

    edges_file = '../brightkite/Brightkite_edges.txt'
    checkin_file = '../brightkite/Brightkite_totalCheckins.txt'

    f1 = open(edges_file, "r")
    lines = f1.readlines()
    curr = -1
    for line in lines:
        node1, node2 = map(int, line.strip().split())
        if node1 != curr:
            curr = node1
            adjacency_list.append([])
        adjacency_list[curr].append(node2)

    f2 = open(checkin_file, "r")
    lines = f2.readlines()
    curr_usr = 0
    curr_time_list = []
    curr_loc_list = []
    for line in lines:
        line0 = line.strip().split()
        if len(line0) == 5 and line0[2] != '0.0':
            usr_id, time, _, _, loc_id = line.strip().split()
            if int(usr_id) == curr_usr:
                curr_time_list.append(time)
                curr_loc_list.append(loc_id)
            else:
                checkin_time_list.append(copy.deepcopy(curr_time_list))
                check_loc_list.append(copy.deepcopy(curr_loc_list))
                curr_usr += 1
                while int(usr_id) != curr_usr:
                    checkin_time_list.append([])
                    check_loc_list.append([])
                    curr_usr += 1
                curr_time_list = [time]
                curr_loc_list = [loc_id]
    checkin_time_list.append(copy.deepcopy(curr_time_list))
    check_loc_list.append(copy.deepcopy(curr_loc_list))
    print("Reading Data Complete")
    return adjacency_list, checkin_time_list, check_loc_list


def random_remove(adjacency_list, frac):
    usr_num = len(adjacency_list)
    remove_num, target_usr = 0, 0
    usr_friend = []
    while remove_num <= 10:
        target_usr = random.randint(0, usr_num - 1)
        usr_friend = adjacency_list[target_usr]
        friend_num = len(usr_friend)
        remove_num = int(frac * friend_num)
    target_friend = random.sample(usr_friend, remove_num)
    print("Target user is user", target_usr, ", Removing ", remove_num, "edges")
    for i in target_friend:
        adjacency_list[target_usr].remove(i)
        adjacency_list[i].remove(target_usr)
    return target_usr, adjacency_list


if __name__ == '__main__':
    adjacency_list, checkin_time_list, check_loc_list = input_data()
    tar, adj = random_remove(adjacency_list, 0.1)
    model = Model(tar)
    model.input_data(adj, checkin_time_list, check_loc_list)
    model.filtering()
    recomm_list = model.run()
    print(recomm_list)
