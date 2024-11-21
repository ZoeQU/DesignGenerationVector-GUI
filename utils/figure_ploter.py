# -*- coding:utf-8 -*-
import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import pandas as pd

def visualize_pie_chart(sim, processPath, title):
    y = np.array(sim)
    bins = pd.IntervalIndex.from_tuples([(0.0, 0.05), (0.05, 0.1), (0.1, 0.15), (0.15, 0.2), (0.2, 0.25),
                                         (0.25, 0.3), (0.3, 0.35), (0.35, 0.4), (0.4, 0.45), (0.45, 0.5),
                                         (0.5, 0.55), (0.55, 0.6), (0.6, 0.65), (0.65, 0.7), (0.7, 0.75),
                                         (0.75, 0.8), (0.8, 0.85), (0.85, 0.9), (0.9, 0.95), (0.95, 1.0)])
    y_cut = pd.cut(y, bins)
    y_score = pd.value_counts(y_cut)
    y_score2 = dict(y_score)
    labels = []
    values = []
    for key, value in y_score2.items():
        if value > 0:
            labels.append(str(key))
            values.append(value)

    plt.pie(np.array(values), labels=labels, autopct='%.2f%%')
    plt.title(title)
    plt.savefig(processPath + title + "_similarity_pie_chart.svg")
    # plt.show()
    plt.close('all')


def visualize_hist(sim, processPath, method):
    n = len(sim)
    plt.hist(sim, bins=n, facecolor="blue", edgecolor="black", alpha=0.7)
    plt.xlabel("times")
    plt.ylabel("sim value")
    plt.title("similarity values")
    plt.savefig(processPath + str(method) + " similarity values.svg")
    # plt.show()
    plt.close('all')

