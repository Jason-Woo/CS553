def input_data():
    edges_file = '../data/Brightkite_edges.txt'
    checkin_file = '../data/Brightkite_totalCheckins.txt'

    adjacency_list = []
    checkin_usr_list = []
    checkin_time_list = []
    check_loc_list = []

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
    for line in lines:
        line0 = line.strip().split()
        if len(line0) == 5:
            usr_id, time, _, _, loc_id = line.strip().split()
            checkin_usr_list.append(usr_id)
            checkin_time_list.append(time)
            check_loc_list.append(loc_id)
