def init():
    open('README.md', 'w').close()


def log_by_crag(df, crags):
    '''
    Will print all logs per crag. Crags will be ordered by the order in crag_index.txt
    '''
    with open('README.md', 'a') as f:
        f.write('#Log by crag')
        f.write(df.to_string())
        print(crags)
