import util
import write

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

df = util.read_log_file(LOGFILE, grades)

# ---- Overwrite the README.md file
write.init()
write.log_by_crag(df, crags)