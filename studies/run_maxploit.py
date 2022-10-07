"""Test Study for the maxploit model.

A study to test the runner with the maxploit model.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

import numpy as np
from time import time
import datetime as dt
from numpy import random
import argparse
import json
import networkx as nx
import cProfile


import pycopancore.models.maxploit as M
from pycopancore.runners.runner import Runner

#---configuration---

# seed
seed = 1

# runner
timeinterval = 1
timestep = 0.1

# individuals
ni_sust = 50  # number of agents with sustainable behaviour 1
ni_nonsust = 50 # number of agents with unsustainable behaviour 0
nindividuals = ni_sust + ni_nonsust

# cells:
cell_stock=1
cell_capacity=1
cell_growth_rate=1
nc = nindividuals  # number of cells

#groups:
ng_total = 10 # number of total groups
ng_sust = 5 # number of sustainable groups
ng_nonsust = ng_total - ng_sust
group_meeting_interval = 0.1

#networks
acquaintance_network_type = "Erdos-Renyi"
group_membership_network_type = "1-random-Edge"
p = 0.5  # link density for random networks

#---write into dic---
configuration = {
    "seed": seed,
    "timeinterval": timeinterval,
    "timestep" : timestep,
    "ni_sust" : ni_sust,
    "ni_nonsust" : ni_nonsust,
    "nindividuals" : nindividuals,
    "cell_stock": cell_stock,
    "cell_capacity": cell_capacity,
    "cell_growth_rate": cell_growth_rate,
    "nc" : nc,
    "ng_total" : ng_total,
    "ng_sust" : ng_sust,
    "ng_nonsust" : ng_nonsust,
    "group_meeting_interval" : group_meeting_interval,
    "acquaintance_network_type" : acquaintance_network_type,
    "group_membership_network_type" : group_membership_network_type,
    "p" : p
}

# first thing: set seed so that each execution must return same thing:
random.seed(seed)

# instantiate model
model = M.Model()

# instantiate process taxa culture:
culture = M.Culture()

# generate entitites:
world = M.World(culture=culture)
social_system = M.SocialSystem(world=world)
cells = [M.Cell(stock=1, capacity=1, growth_rate=1, social_system=social_system)
         for c in range(nc)]
individuals = [M.Individual(behaviour=0, opinion=0, imitation_tendency=0,
                            rewiring_prob=0.5,
                            cell=cells[i]) for i in range(ni_nonsust)] \
              + [M.Individual(behaviour=1, opinion=1, imitation_tendency=0,
                              rewiring_prob=0.5,
                              cell=cells[i + ni_nonsust])
                 for i in range(ni_sust)]

# instantiate groups
groups = [M.Group(culture=culture, world=world, group_opinion=1,
                  group_meeting_interval=group_meeting_interval) for i in range(ng_sust)] + \
         [M.Group(culture=culture, world=world, group_opinion=0,
                  group_meeting_interval=group_meeting_interval) for i in range(ng_nonsust)]

for (i, c) in enumerate(cells):
    c.individual = individuals[i]


def erdosrenyify(graph, p=0.5):
    """Create a ErdosRenzi graph from networkx graph.

    Take a a networkx.Graph with nodes and distribute the edges following the
    erdos-renyi graph procedure.
    """
    assert not graph.edges(), "your graph has already edges"
    nodes = list(graph.nodes())
    for i, n1 in enumerate(nodes[:-1]):
        for n2 in nodes[i + 1:]:
            if random.random() < p:
                graph.add_edge(n1, n2)


# set the initial graph structure to be an erdos-renyi graph
print("erdosrenyifying the graph ... ", end="", flush=True)
start = time()
erdosrenyify(culture.acquaintance_network, p=p)


GM = culture.group_membership_network
# initialize group_membership network
# interlink_density = 0.5
# for i in individuals:
#     for g in groups:
#         if np.random.uniform() < interlink_density:
#             GM.add_edge(i, g)
# make sure each individual is member of at least one group
#     if not list(i.group_memberships): #i.e. list is empty
#         GM.add_edge(i, np.random.choice(groups))

# group_membership network with only one group membership for now
for i in individuals:
    GM.add_edge(i, np.random.choice(groups))

# color_map = []
# for node in list(GM.nodes):
#     color_map.append(GM.nodes[node]["color"])
# top_nodes = {n for n, d in GM.nodes(data=True) if d["type"] == "Group"}
# bottom_nodes = set(GM) - top_nodes
# nx.draw(GM, node_color=color_map, with_labels=False,
#         pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
# plt.show()

#get a preliminary intergroup network for plotting multilayer
inter_group_network = nx.Graph()
for g in groups:
    inter_group_network.add_node(g) # groups have no interaction so far
# for index, g in enumerate(groups):
#     for j in groups[:index]:
#         inter_group_network.add_edge(g, j)


# try to plot a nice multilayer network
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# LayeredNetworkGraph([culture.acquaintance_network, inter_group_network], [culture.group_membership_network], ax=ax)
# ax.view_init(90, 0)
# plt.show()
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# LayeredNetworkGraph([culture.acquaintance_network, inter_group_network], [culture.group_membership_network], ax=ax)
# ax.view_init(40, 40)
# plt.show()

# color_map = []
# unsust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and n.group_opinion)
#                 or (d["type"] == "Individual" and n.behaviour)}
# sust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and not n.mean_group_opinion)
#               or (d["type"] == "Individual" and not n.opinion)}
# for node in list(GM.nodes):
#     if node in unsust_nodes:
#         color_map.append("red")
#     else:
#         color_map.append("blue")
# nx.draw(GM, node_color=color_map, with_labels=False,
#         pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
# plt.show()

print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print('\n runner starting')



r = Runner(model=model)
start = time()
traj = r.run(t_1=timeinterval, dt=timestep)
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))

import os
os_path = "C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\maxploit"

import datetime
current_time = datetime.datetime.now()
current = [current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second]
time_string = f"{current_time.year}"
parent_directory_name = f"{current_time.year}"
for i in current:
    if i < 10:
        time_string += f"_0{i}"
    else:
        time_string += f"_{i}"

for i in current[:2]:
    if i < 10:
        parent_directory_name += f"_0{i}"
    else:
        parent_directory_name += f"_{i}"
# save_time = f"{current_time.year}_" + f"{current_time.month}_" + f"{current_time.day}_" \
#             + f"{current_time.hour}_" + f"{current_time.minute}_" + f"{current_time.second}"

# Directory
directory = f"Run_{time_string}"

# Path
my_path = os.path.join(os_path, parent_directory_name)

# Create the directory
# 'GeeksForGeeks' in
# '/home / User / Documents'
if not os.path.exists(my_path):
    os.mkdir(my_path)
    print(f"Directory {parent_directory_name} created @ {my_path}")

my_path = os.path.join(my_path, directory)
os.mkdir(my_path)
print(f"Directory {directory} created @ {my_path}")

# import json
# f = open(my_path + "_traj_dic.json", "wb")
# json.dump(traj, f)

# saving things after succesfull run
# saving config
#---save json file---
f = open(my_path+"\\"+"configuration.json", "w+")
json.dump(configuration, f, indent=4)

# saving traj
# load pickle module
from pickle import dump
# create a binary pickle file
f = open(my_path +"\\" + "traj.pickle", "wb")

tosave = {
          v.owning_class.__name__ + "."
          + v.codename: {str(e): traj[v][e]
                         for e in traj[v].keys()
                         }
          for v in traj.keys() if v is not "t"
          }

del tosave["Culture.group_membership_network"]
del tosave["Culture.acquaintance_network"]

tosave["t"] = traj["t"]
dump(tosave, f)
# close file
f.close()

# save networks
os.mkdir(my_path + "\\networks")
print(f"Directory networks created @ {my_path}")
network_list = [culture.acquaintance_network, culture.group_membership_network, inter_group_network]
network_names = ["culture.acquaintance_network", "culture.group_membership_network", "inter_group_network"]
for counter, n in enumerate(network_list):
    f = open(my_path +f"\\networks\\{network_names[counter]}.pickle", "wb")
    save_nx = nx.relabel_nodes(n, lambda x: str(x))
    dump(save_nx, f)

# text file
with open(my_path +"\\" +'readme.txt', 'w') as f:
    f.write('Groups do not change their opinion')