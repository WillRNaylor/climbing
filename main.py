import util
import write
import analysis
import datetime

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
today = datetime.date.today()
current_year = today.year

df = util.read_log_file(LOGFILE, grades, WARNINGS)

# ---- Make the figures
analysis.fig_sport_total(df, grades_inv, max_ascents=39)
analysis.fig_sport_time(df, stop=current_year, top_year=current_year)
analysis.fig_sport_time_all(df, stop=current_year)
analysis.sport_grade_table(df, stop=current_year)

# ---- Overwrite the HTML file
write.init()
write.analysis()
write.table(df, crags)
write.grade_table()