import util

'''
Runs basic analysis and prints out climbing log.
'''



# ---- Input
LOGFILE = '/Users/Hermes/Dropbox/Climbing_log/climbing_log.txt'
OUT_FILE = '/Users/Hermes/Dropbox/Climbing_log/climbing_log.md'

CRAGFILE = '/Users/Hermes/Dropbox/Climbing_log/Code/reference/crag_index.txt'
GRADEFILE = '/Users/Hermes/Dropbox/Climbing_log/Code/reference/grade_conv.txt'
crags = util.get_crag_dict(CRAGFILE)
grades = util.get_grade_conv(GRADEFILE)

df = util.read_log_file(LOGFILE, grades)


print(df.crag.unique())