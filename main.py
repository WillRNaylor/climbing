import util
import write
import analysis

'''
Runs basic analysis and prints out climbing log.
'''

# ---- Input
LOGFILE = 'log.txt'
OUT_FILE = 'README.md'
WARNINGS = False

CRAGFILE = './reference/crag_index.txt'
GRADEFILE = './reference/grade_conv.txt'
crags = util.get_crag_dict(CRAGFILE)
grades = util.get_grade_conv(GRADEFILE)
grades_inv = {v: k for k, v in grades.items()}
grades_inv[15] = '5a'  # Otherwise there would be no 15 equivelent

df = util.read_log_file(LOGFILE, grades, WARNINGS)

# ---- Make the figures
analysis.fig_sport_total(df, grades_inv)
analysis.fig_sport_time(df)
analysis.fig_sport_time_all(df)
analysis.sport_grade_table(df)

# ---- Overwrite the HTML file
write.init()
write.analysis()
write.table(df, crags)
write.grade_table()