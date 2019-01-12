#!/usr/bin/env python
import sys
import get_info
import pandas as pd
import numpy as np
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from scipy import stats
import math as m
import csv

def prepare_data(conn, curs):
    sql = "SELECT * FROM all_stats2 WHERE weekday_evening != 0 or work_traffic != 0 or weekend_day != 0;"
    X = pd.read_sql(sql, conn)
    X_norm = X[['work_traffic_norm', 'weekday_evening_norm', 'weekend_day_norm', "geom", "zone", "gid"]]

    # X_norm = X_norm[(np.abs(stats.zscore(X_norm)) < 3).all(axis=1)]
    q_max = X_norm.quantile(0.999)
    q_min = X_norm.max() - q_max
    print(type(X_norm))
    X_norm = X_norm[((X_norm['weekday_evening_norm'] < q_max['weekday_evening_norm']) & (
                X_norm['weekday_evening_norm'] > q_min['weekday_evening_norm'])) |
                    ((X_norm['work_traffic_norm'] < q_max['work_traffic_norm']) & (
                                X_norm['work_traffic_norm'] > q_min['work_traffic_norm'])) |
                    ((X_norm['weekend_day_norm'] < q_max['weekend_day_norm']) & (
                                X_norm['weekend_day_norm'] > q_min['weekend_day_norm']))]

    # for i in range(len(X_norm)):
    #    s = m.sqrt(pow(X_norm['weekday_evening_norm'].iloc[i],2) + pow(X_norm['work_traffic_norm'].iloc[i],2) + pow(X_norm['weekend_day_norm'].iloc[i],2))
    #    print(s)
    #    X_norm['weekday_evening_norm'].iloc[i] /= s
    #    X_norm['work_traffic_norm'].iloc[i] /= s
    #    X_norm['weekend_day_norm'].iloc[i] /= s

    return X_norm

def visualize_data(conn, curs, X_norm):
    plt.rcParams['figure.figsize'] = (16, 9)


    kmeans = KMeans(n_clusters=8, random_state=0).fit(X_norm[['weekday_evening_norm', 'work_traffic_norm', 'weekend_day_norm']])
    labels = kmeans.predict(X_norm[['weekday_evening_norm', 'work_traffic_norm', 'weekend_day_norm']])
    print(labels)
    X_norm2 = X_norm.copy()
    lab = labels
    X_norm['cluster'] = pd.Series(lab, index=X_norm.index)
    X_norm = X_norm[X_norm['cluster'] != 5]
    X_norm = X_norm[X_norm['cluster'] != 7]

    try:
        sql_create_column = "ALTER TABLE all_stats2 ADD COLUMN cluster Integer;"
        curs.execute(sql_create_column)
        conn.commit()
    except:
        pass

    #for index, i in X_norm[['cluster','gid']].iterrows():
    #    sql = "UPDATE all_stats2 SET cluster = " + str(i['cluster']) + " WHERE gid = " + str(i['gid']) + ";"
    #    curs.execute(sql)
    #conn.commit()

    # inertia = []
    # x = []
    # for i in range(2,15):
    #    xx, iner = i, KMeans(n_clusters=i, random_state=0).fit(X_norm[['weekday_evening_norm', 'work_traffic_norm', 'weekend_day_norm']]).inertia_
    #    inertia.append(iner)
    #    x.append(xx)

    # plt.xlabel("Liczba klastrów")
    # plt.ylabel("Odległości od środków klastrów")
    # plt.plot(x,inertia)
    # plt.show()

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(X_norm2['weekday_evening_norm'], X_norm2['work_traffic_norm'], X_norm2['weekend_day_norm'], c=labels)
    #ax.scatter(X_norm2['weekday_evening'], X_norm2['work_traffic'], X_norm2['weekend_day'])
    ax.set_title(label = 'Unnormalized count of drives')
    ax.set_xlabel('Recreation drives')
    ax.set_ylabel('Education drives')
    ax.set_zlabel('Cultural drives')
    plt.show()

    return X_norm

def low_av_high(x):
    if x <= 0.2:
        return 'VERY LOW'
    elif 0.2 < x <= 0.4:
        return 'LOW'
    elif 0.4 < x <= 0.6:
        return 'AVERAGE'
    elif 0.6 < x <= 0.8:
        return 'HIGH'
    else:
        return 'VERY HIGH'

if __name__ == "__main__":
    conn = get_info.connect_to_db()

    curs = conn.cursor()
    X_norm = prepare_data(conn, curs)
    X_norm = visualize_data(conn, curs, X_norm)

    qgis_labels = {0: "jasno-zielony",
                   1: "czerwony",
                   2: "ciemno-zielony",
                   3: "żółty",
                   4: "ciemno-niebieski",
                   6: "jasno-niebieski"}

    clusters = [0, 1, 2, 3, 4, 6]
    max_we = X_norm['weekday_evening_norm'].max()
    max_wd = X_norm['weekend_day_norm'].max()
    max_wt = X_norm['work_traffic_norm'].max()

    min_we = X_norm['weekday_evening_norm'].min()
    min_wd = X_norm['weekend_day_norm'].min()
    min_wt = X_norm['work_traffic_norm'].min()

    print('\n')

    for c in clusters:
        print('{:18}{:.2}\t{:.2}\t{:.2}'.format(qgis_labels[c],
            (X_norm[X_norm['cluster'] == c]['weekday_evening_norm'].mean() - min_we) / (max_we - min_we),
            (X_norm[X_norm['cluster'] == c]['work_traffic_norm'].mean() - min_wt) / (max_wt - min_wt),
            (X_norm[X_norm['cluster'] == c]['weekend_day_norm'].mean() - min_wd) / (max_wd - min_wd)))

    print('\n')

    for c in clusters:
        wt = (X_norm[X_norm['cluster'] == c]['work_traffic_norm'].mean() - min_wt) / (max_wt-min_wt)
        wd = (X_norm[X_norm['cluster'] == c]['weekend_day_norm'].mean() - min_wd) / (max_wd-min_wd)
        wen = (X_norm[X_norm['cluster'] == c]['weekday_evening_norm'].mean() - min_we) / (max_we-min_we)

        wt = low_av_high(wt)
        wd = low_av_high(wd)
        wen = low_av_high(wen)

        print('{:17}{:9}\t{:9}\t{:9}'.format(qgis_labels[c], wen, wt, wd))