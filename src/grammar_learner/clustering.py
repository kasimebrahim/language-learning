#!/usr/bin/env python3
#language-learning/src/grammar_learner/clustering.py 0.5 80726

def number_of_clusters(vdf, cluster_range, algorithm='kmeans', \
        criteria='silhouette', level=0.9, verbose='none'):
    import numpy as np
    import pandas as pd
    from statistics import mode
    from utl import round1, round2, round3
    from kmeans import cluster_words_kmeans

    if(len(cluster_range) < 2 or cluster_range[2] < 1):
        return cluster_range[0]

    sil_range = pd.DataFrame(columns=['Np','Nc','Silhouette','Inertia'])
    if verbose == 'debug':
        print('clustering/poc.py/number_of_clusters: vdf:\n', \
            vdf.applymap(round2).sort_values(by=[1,2], ascending=[True,True]))

    # Check number of clusters <= word vector dimensionality
    max_clusters = min(cluster_range[1], len(vdf), \
                       max([x for x in list(vdf) if isinstance(x,int)]))
    #?if max([x for x in list(vdf) if isinstance(x,int)]) < cluster_range[0]+1:
    #?    max_clusters = min(cluster_range[1], len(vdf))  #FIXME: hack 80420!
    if max([x for x in list(vdf) if isinstance(x,int)]) == 2:
        if verbose in ['max','debug']: print('2 dim word space -- 4 clusters')
        return 4  #FIXME: hack 80420!

    if verbose in ['max', 'debug']:
        print('number_of_clusters: max_clusters =', max_clusters)
    n_clusters = max_clusters   #80623: cure case max < range.min

    #FIXME: unstable number of clusters #80422
    lst = []
    attempts = 1 #12
    for k in range(attempts):
        for i,j in enumerate(range(cluster_range[0], max_clusters, cluster_range[2])):
            cdf, silhouette, inertia = cluster_words_kmeans(vdf, j)
            if verbose in ['debug']:
                print(j, 'clusters ⇒ silhouette =', silhouette)
            sil_range.loc[i] = [j, len(cdf), round(silhouette,4), round(inertia,2)]
            if level > 0.9999:   # 1 - max Silhouette index
                n_clusters = sil_range.loc[sil_range['Silhouette'].idxmax()]['Nc']
            elif level < 0.0001: # 0 - max number pf clusters
                n_clusters = sil_range.loc[sil_range['Nc'].idxmax()]['Nc']
            else:
                thresh = level * sil_range.loc[sil_range['Silhouette'].idxmax()]['Silhouette']
                n_clusters = min(sil_range.loc[sil_range['Silhouette'] > thresh]['Nc'].tolist())
        lst.append(int(n_clusters))

    dct = dict()
    for n in lst:
        if n in dct:
            dct[n] += 1
        else: dct[n] = 1
    n_clusters = int(round(np.mean(lst),0))
    n2 = list(dct.keys())[list(dct.values()).index(max(list(dct.values())))]
    if n2 != n_clusters:
        if len(list(dct.values())) == len(set(list(dct.values()))):
            n3 = mode(lst)  # Might get error
        else: n3 = n_clusters
        n_clusters = int(round((n_clusters + n2 + n3)/3.0, 0))

    if verbose in ['max', 'debug']:
        if len(dct) > 1:
            print('Clusters:', sorted(lst), '⇒', n_clusters)
    return int(n_clusters)


def clusters2list(clusters):
    categories = []
    for index, row in clusters.iterrows():
        category = []
        category.append(row['cluster'])
        category.append(0)
        category.append(index)
        category.append(0.0)
        category.append(row['cluster_words'])
        category.append([0 for x in row['cluster_words']])
        categories.append(category)
    return categories


def clusters2dict(clusters):
    word_clusters = dict()
    for row in clusters:
        for word in row[4]:
            word_clusters[word] = row[0]
    return word_clusters


#80725 POC 0.1-0.4 deleted, 0.5 restructured. This module was src/clustering/poc05.py