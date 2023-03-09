import util
import write
import analysis

'''
Runs basic analysis and prints out climbing log.
'''

# ---- Input
LOGFILE = 'log.txt'
OUT_FILE = 'README.md'

CRAGFILE = './reference/crag_index.txt'
GRADEFILE = './reference/grade_conv.txt'
crags = util.get_crag_dict(CRAGFILE)
grades = util.get_grade_conv(GRADEFILE)
grades_inv = {v: k for k, v in grades.items()}
grades_inv[15] = '5a'  # Otherwise there would be no 15 equivelent

df = util.read_log_file(LOGFILE, grades)

# ---- Make the figures
analysis.sport_total(df, grades_inv)
analysis.sport_time(df)
analysis.sport_time_all(df)

# ---- Overwrite the HTML file
write.init()
write.analysis()
write.table(df, crags)
