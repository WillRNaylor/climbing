import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import util
import write


def sport_total(df, grades_inv, figname='figures/sport_total.png'):
    data = [
        df[df.ascent_type == 'o'].num_grade.values,
        df[df.ascent_type == 'f'].num_grade.values,
        df[df.ascent_type == 'r'].num_grade.values,
    ]


    first = 14
    last = 30
    xticks = np.arange(0, 24, 1)
    yticks = np.arange(first, last, 1)
    ytlabels = [f"{grades_inv[x]} / " + str(x) for x in np.arange(first, last, 1)]
    with plt.rc_context({'xtick.color':'grey', 'ytick.color':'gray', 'axes.edgecolor':'grey', 'figure.dpi':140}):
        fig = plt.figure()
        fig.set_facecolor('black')
        ax = fig.add_subplot(1,1,1)
        ax.set_facecolor('black')
        colors = ['white', 'yellow', 'red']
        plt.hist(data, np.arange(first - .5, last + .5), stacked=True, density=False, orientation='horizontal', edgecolor="black", color=colors);
        plt.yticks(yticks, ytlabels)
        plt.xticks(xticks, xticks)
        ax.set_axisbelow(True)
        ax.xaxis.grid(color='gray', linestyle='dashed')
        legend = plt.legend(['Onsight', 'Flash', 'Redpoint'])
        frame = legend.get_frame()
        frame.set_facecolor('black')
        frame.set_edgecolor('black')
        for text in legend.get_texts():
            text.set_color("grey")
        fig.tight_layout()
        plt.savefig(figname)


def sport_time(df, figname='figures/sport_time.png'):
    start = 2017
    stop = 2023
    df_sport = df[df.num_grade != 0]
    data = []
    for y in np.arange(start, stop + 1):
        temp = df_sport[df_sport.date >= datetime.date(y, 1, 1)]
        temp = temp[temp.date <= datetime.date(y, 12, 31)]
        data_year = []
        for ascent in ['o', 'f', 'r']:
            g = temp[temp.ascent_type == ascent].num_grade.values
            g.sort()
            if len(g) > 10:
                g = g[-10:]
            data_year.append(np.mean(g))
        data.append(data_year)
    data = np.array(data)
    x = np.arange(start, stop + 1)

    with plt.rc_context({'xtick.color':'grey', 'ytick.color':'gray', 'axes.edgecolor':'grey', 'figure.dpi':140}):
        fig = plt.figure()
        fig.set_facecolor('black')
        ax = fig.add_subplot(1,1,1)
        ax.set_facecolor('black')
        plt.plot(x, data[:, 0], 'w-s', x, data[:, 1], 'y-s', x, data[:, 2], 'r-s')
        yticks = np.arange(14, 27, 1)
        plt.yticks(yticks, yticks)
        ax.set_axisbelow(True)
        ax.yaxis.grid(color='gray', linestyle='dashed')
        legend = plt.legend(['Onsight', 'Flash', 'Redpoint'])
        frame = legend.get_frame()
        frame.set_facecolor('black')
        frame.set_edgecolor('black')
        for text in legend.get_texts():
            text.set_color("grey")
        fig.tight_layout()
        plt.savefig(figname)


def sport_time_all(df, figname='figures/sport_time_all.png'):
    start = 2017
    stop = 2023
    df_sport = df[df.num_grade != 0]
    data = []
    for y in np.arange(start, stop + 1):
        temp = df_sport[df_sport.date >= datetime.date(y, 1, 1)]
        temp = temp[temp.date <= datetime.date(y, 12, 31)]
        data_year = []
        g = temp.num_grade.values
        g.sort()
        if len(g) > 10:
            g = g[-10:]
        data_year.append(np.mean(g))
        temp = df_sport[df_sport.date >= datetime.date(y, 1, 1)]
        temp = temp[temp.date <= datetime.date(y, 12, 31)]
        for ascent in ['o', 'f', 'r']:
            g = temp[temp.ascent_type == ascent].num_grade.values
            g.sort()
            if len(g) > 10:
                g = g[-10:]
            data_year.append(np.mean(g))
        data.append(data_year)
    data = np.array(data)
    x = np.arange(start, stop + 1)

    with plt.rc_context({'xtick.color':'grey', 'ytick.color':'gray', 'axes.edgecolor':'grey', 'figure.dpi':140}):
        fig = plt.figure()
        fig.set_facecolor('black')
        ax = fig.add_subplot(1,1,1)
        ax.set_facecolor('black')
        plt.plot(x, data[:, 0], 'g-s', x, data[:, 1], 'w-s', x, data[:, 2], 'y-s', x, data[:, 3], 'r-s')
        yticks = np.arange(14, 27, 1)
        plt.yticks(yticks, yticks)
        ax.set_axisbelow(True)
        ax.yaxis.grid(color='gray', linestyle='dashed')
        legend = plt.legend(['All', 'Onsight', 'Flash', 'Redpoint'])
        frame = legend.get_frame()
        frame.set_facecolor('black')
        frame.set_edgecolor('black')
        for text in legend.get_texts():
            text.set_color("grey")
        fig.tight_layout()
        plt.savefig(figname)