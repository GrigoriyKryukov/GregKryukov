import numpy as np
import networkx as nx

def GK(r_real, r_gen, sigma):
    return np.exp(-(r_real - r_gen)**2/(2 * sigma**2))

def score(KS, r, d, AC, GCC, CC): 
    true_AC = 0.005066798238955518
    true_GCC = 11.748410823170731
    answer = (1 - KS) + GK(15, r, 2) + GK(28, d, 4) + GK(true_AC, AC, 0.001) + GK(true_GCC, GCC, 2) + GK(168, CC, 32)
    return answer / 6 * 100

degree_cdf = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 24, 46], 
                      [0.0, 0.6902231668437833, 0.8517534537725824, 0.9086078639744952, 0.9378320935175345, 
                       0.9516471838469713, 0.9654622741764081, 0.9723698193411264, 0.9776833156216791, 
                       0.9808714133900106, 0.9845908607863975, 0.9888416578108395, 0.9893730074388948, 
                       0.9925611052072264, 0.9936238044633369, 0.9952178533475027, 0.9957492029755579, 
                       0.9968119022316685, 0.997874601487779, 0.9989373007438895, 0.9994686503719448, 1.0]]

degree_pdf = [degree_cdf[1][i+1]-degree_cdf[1][i] for i in range(len(degree_cdf[1])-1)]
degree = np.array(degree_pdf) * 1882 # Число вершин с определенной степенью в исходном графе

""" Введем две вспомогательные функции, которые строят связные компоненты с определенными параметрами"""

""" krug(n, s) строит цикл длины n с первой вершиной под номером s"""
""" Имеет все степени вершины равные 2, Clustering coefficients по нулям"""
def krug(n, s):
    for i in range(s, s+n-1):
        edges.append([i, i+1])
    edges.append([s, s+n-1])
    
""" our_gr(u, v, s) строит соединенные друг с другом вершины с большими степенями, и нужное число вершинок для степени"""
""" Имеет одну вершину степени u, одну степени v, u+v-2 вершин степени 1. Clustering coefficients по нулям"""    
def our_gr(u, v, s):
    edges.append([s, s+1])
    for i in range(s+2, s+u+1):
        edges.append([s, i])
    for i in range(s+u+1, s+u+v):
        edges.append([s+1, i])

"""А теперь погнали строить граф"""        
edges = []
"""Фигачим главную компоненту с нужным диаметром, радиусом и средней длиной пути"""
for i in range(28):
    edges.append([i, i+1]) # Основа для диаметра 28
for i in range(29, 43):
    edges.append([i, i+1]) # Доп путь для того, чтобы центральная вершина имела самое дальнее расстояние не 14, а 15
edges.append([7, 29])
edges.append([21, 43])
# Методом проб и ошибок достраиваем так, чтобы средняя длина пути была близка к правде
edges.append([14, 44])
for i in range(44, 57):
    edges.append([i, i+1])
edges.append([49,51])
""" Теперь надо выполнить условие на AC """
""" Needed AC = 0.005066798238955518"""  
""" Needed AC * 1882 = 9.5357..."""  
""" Значит сумма всех Clustering coefficient должна быть близка к 9.53"""  
""" В полученной большой компоненте сумма Clustering coefficient равна 1.6666"""  
""" Добавим графыч с суммой Clustering coefficient 2.8666""" 
edges.append([58, 59])
edges.append([59, 60])
edges.append([58, 60])
edges.append([58, 61])
edges.append([59, 61])
edges.append([59, 62])
edges.append([63, 61])
edges.append([63, 60])
edges.append([61, 64])
edges.append([62, 58])
edges.append([65, 58])
edges.append([65, 61])
edges.append([65, 62])
""" Добавим K_5 с суммой Clustering coefficient 5 """ 
edges.append([66, 67])
edges.append([66, 68])
edges.append([66, 69])
edges.append([66, 70])
edges.append([67, 68])
edges.append([67, 69])
edges.append([67, 70])
edges.append([69, 68])
edges.append([70, 68])
edges.append([69, 70])
""" 1.667 + 2.867 + 5 = 9.534, почти то что надо""" 
"""Теперь наша цель добавить 168-3=165 компонент связности, у каждой сумма Clustering coefficient 0"""
"""Для начала обработаем редкую степень вершины 46 """
for i in range(72, 118):
    edges.append([71, i])
"""Теперь посмотрим, какие степени вершин нам осталось закрыть, используя degree (в этом коде для экономии места опустил)"""
num_deg = [99, 49, 24, 26, 13, 10, 6, 7, 8, 1, 6, 2, 3, 1, 2, 2, 2, 1]
our_deg = degree_cdf[0][3:-1]
"""Идея: доморощенной функцией our_gr() заполняем все вершины со степенью 3 и выше"""
s = 118
k = 0
while k < 18:
    u = our_deg[k]
    num_deg[k] -= 1
    if num_deg[k] == 0:
        k += 1
    v = our_deg[k]
    num_deg[k] -= 1
    if num_deg[k] == 0:
        k += 1
    our_gr(u, v, s)
    s += u + v
""" После этих страшных операций у нас остается 42 неиспользованных вершины степени 1, 253 вершины степени 2"""
""" Надо их распределить на 33 компоненты"""
""" Сделаем 21 цепочку длины 11 (в каждой по две вершины степени 1 и по 9 вершин степени 2)"""
""" Оставшимся вершины степени 2 найдем место в доморощенной функции krug()"""
# Finish him
for i in range(21):
    for j in range(s, s+10):
        edges.append([j, j+1])
    s += 11
for i in range(11):
    krug(5, s)
    s += 5
krug(9, s)
G = nx.Graph(edges)
H = G.subgraph(max(nx.connected_components(G), key=len))
KS = 1
r = nx.radius(H)
d = nx.diameter(H)
AC = nx.algorithms.cluster.average_clustering(G)
GCC = nx.average_shortest_path_length(H)
CC = nx.number_connected_components(G)
print(score(0, r, d, AC, GCC, CC)) # Score
print(len(G)) #Number of nodes
"""Score = 99.9999603286781"""
"""Перемога!"""
