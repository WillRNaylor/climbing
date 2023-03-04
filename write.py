def init():
    open('README.md', 'w').close()


def make_nested_crag_list(crags):
    oc = list(crags.keys())
    print(oc)
    crags[oc[0]][0]



def log_by_crag(df, crags):
    '''
    Will print all logs per crag. Crags will be ordered by the order in crag_index.txt
    '''

    # Make the nested list of crags with locations
    cnested = make_nested_crag_list(crags)

    with open('README.md', 'a') as f:
        f.write('# Log by crag\n\n')

        # Contents
        crags_visited = df.crag.unique()
        levels = [None, None, None, None]
        ordered_crags = list(crags.keys())
        for crag in ordered_crags:
            if crag not in crags_visited:
                continue
            crag_details = crags[crag]
            for l in range(len(crag_details)):
                if levels[l] != crag_details[l]:
                    levels[l] = crag_details[l]
                    f.write(f"{l * '  '}* [{levels[l]}](#{'-'.join(crags[crag]).replace(' ', '-').lower()})\n")
        
        # List of sends
        for crag in ordered_crags:
            f.write(f"## {', '.join(crags[crag])}\n\n")
            cdf = df.loc[df.crag == crag].sort_values('grade').reset_index()
            print(cdf)
            f.write("| Date | Grade | Route name | Type | Comment |\n")
            f.write("| ---- |:-----:| ---------- |:----:| ------- |\n")
            for i in range(cdf.shape[0]):
                f.write(f"| {cdf.date[i]} | {cdf.grade[i]} | {cdf.route[i]} | {cdf.ascent_type[i]} | {cdf.comment[i]} |\n")

        f.write(df.to_string())
        print(df)
