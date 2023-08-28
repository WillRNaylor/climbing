import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_top_sport_climbs(df, year, n_top, fill_blank=None, avg=False, total=False):
    df_sport = df[df.num_grade != 0]
    temp = df_sport[df_sport.date >= datetime.date(year, 1, 1)]
    temp = temp[temp.date <= datetime.date(year, 12, 31)]
    top = []
    for ascent in ['o', 'f', 'r']:
        g = temp[temp.ascent_type == ascent].num_grade.values
        g.sort()
        if len(g) > n_top:
            g = g[-n_top:]
        g = [str(i) for i in g]
        g.reverse()
        top.append(g)
    if fill_blank is not None:
        for g in top:
            if len(g) < n_top:
                g.extend([fill_blank] * (n_top - len(g)))
    return top


def fig_sport_total(
        df, grades_inv, figname='figures/sport_total.png',
        min_grade=14, max_grade=30, min_ascents=0, max_ascents=30, counts_figsize=9):
    
    text_vert_start = 0.23
    text_hor_start = -0.54

    data = [
        df[df.ascent_type == 'o'].num_grade.values,
        df[df.ascent_type == 'f'].num_grade.values,
        df[df.ascent_type == 'r'].num_grade.values,
    ]

    xticks = np.arange(min_ascents, max_ascents, 1)
    yticks = np.arange(min_grade, max_grade, 1)
    ytlabels = [f"{grades_inv[x]} / " + str(x) for x in np.arange(min_grade, max_grade, 1)]
    with plt.rc_context({'xtick.color':'grey', 'ytick.color':'gray', 'axes.edgecolor':'grey', 'figure.dpi':140}):
        fig = plt.figure()
        fig.set_facecolor('black')
        ax = fig.add_subplot(1,1,1)
        ax.set_facecolor('black')
        colors = ['white', 'yellow', 'red']
        plt.hist(data, np.arange(min_grade - .5, max_grade + .5), stacked=True, density=False, orientation='horizontal', edgecolor="black", color=colors)
        plt.yticks(yticks, ytlabels)
        plt.xticks(xticks, xticks)
        ax.set_axisbelow(True)
        ax.xaxis.grid(color='gray', linestyle='dashed')
        legend = plt.legend(['Onsight', 'Flash', 'Redpoint'])
        # Put the 'counts' of each bar
        counts = []
        for i in range(3):
            counts_, bins_ = np.histogram(data[i], np.arange(min_grade - .5, max_grade + .5))
            counts.append(counts_)
        grade_diff = max_grade - min_grade
        send_sums = np.zeros(grade_diff)
        # First print the sums for each type:
        for a_type in range(3):
            send_sums += counts[a_type]
            for i in range(grade_diff):
                if counts[a_type][i] == 0:
                    continue
                ax.text(
                    text_hor_start + send_sums[i], text_vert_start + i + min_grade,
                    str(counts[a_type][i]), horizontalalignment='center', verticalalignment='top',
                    transform=ax.transData, fontsize=counts_figsize, color='black')
        # Now print the sums of the total
        for i in range(grade_diff):
            if send_sums[i] == 0:
                continue
            ax.text(
                text_hor_start + send_sums[i] + 1, text_vert_start + i + min_grade,
                str(int(send_sums[i])), horizontalalignment='center', verticalalignment='top',
                transform=ax.transData, fontsize=counts_figsize, color='white')
        # Legend, and finishing up
        frame = legend.get_frame()
        frame.set_facecolor('black')
        frame.set_edgecolor('black')
        for text in legend.get_texts():
            text.set_color("grey")
        fig.tight_layout()
        plt.savefig(figname)


def fig_sport_time(df, figname='figures/sport_time.png', print_top=True, top_year=2023):
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

    n_top = 13
    fill_blank = '-'
    header_vert_align = 0.99
    top_vert_align = 0.93
    line_vert_align = 0.28
    top_hor_align = 1.03
    top_hor_step = 0.045
    top_fontsize = 9


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
        if print_top:
            top = get_top_sport_climbs(df, top_year, n_top, fill_blank=fill_blank)
            ax.text(top_hor_align + 1 * top_hor_step, header_vert_align, str(top_year) + ":",
                horizontalalignment='center', verticalalignment='top',
                transform=ax.transAxes, fontsize=top_fontsize, color='grey')
            for i, c in enumerate(['white', 'yellow', 'red']):
                ax.text(top_hor_align + i * top_hor_step, top_vert_align, "\n\n".join(top[i]),
                    horizontalalignment='center', verticalalignment='top',
                    transform=ax.transAxes, fontsize=top_fontsize, color=c)
            ax.text(top_hor_align + 1 * top_hor_step, line_vert_align, "___________",
                horizontalalignment='center', verticalalignment='top',
                transform=ax.transAxes, fontsize=top_fontsize, color='grey')
        legend = plt.legend(['Onsight', 'Flash', 'Redpoint'])
        frame = legend.get_frame()
        frame.set_facecolor('black')
        frame.set_edgecolor('black')
        for text in legend.get_texts():
            text.set_color("grey")
        fig.tight_layout()
        plt.savefig(figname)


def fig_sport_time_all(df, figname='figures/sport_time_all.png'):
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


def sport_grade_table(df, figname='figures/sport_grade_table.png', start=2015, stop=2023, n_top=20):

    fill_blank = '-'
    header_vert_align = 0.99
    vert_align = 0.941
    line_vert_align = 0.086
    hor_start = 0.03
    hor_step_inner = 0.016
    hor_step_year = 0.06
    fontsize = 9

    fig_height = 6.8

    with plt.rc_context({'xtick.color':'grey', 'ytick.color':'gray', 'axes.edgecolor':'grey', 'figure.dpi':140}):
        fig = plt.figure(figsize=(12, fig_height))
        fig.set_facecolor('black')
        # Outer loop going through the years (y):
        for yi, y in enumerate(range(start, stop + 1)):
            top = get_top_sport_climbs(df, y, n_top, fill_blank=fill_blank)
            top_no_fill = get_top_sport_climbs(df, y, 100)  # This one just used to calculate the totals.
            for i, g in enumerate(top):
                g.append("\n" + str(len(top_no_fill[i])))
            fig.text(hor_start + 1 * hor_step_inner + yi * hor_step_year, header_vert_align, str(y) + ":",
                horizontalalignment='center', verticalalignment='top', fontsize=fontsize, color='grey')
            for ti, c in enumerate(['white', 'yellow', 'red']):
                fig.text(hor_start + ti * hor_step_inner + yi * hor_step_year, vert_align, "\n\n".join(top[ti]),
                    horizontalalignment='center', verticalalignment='top', fontsize=fontsize, color=c)
            fig.text(hor_start + 1 * hor_step_inner + yi * hor_step_year, line_vert_align, "___________",
                horizontalalignment='center', verticalalignment='top', fontsize=fontsize, color='grey')
        fig.tight_layout()
        plt.savefig(figname)
