def init():
    open('log.html', 'w').close()

    with open('log.html', 'a') as f:
        f.write('''
<!doctype html>
<html>
<head>
<title>Climbing log</title>
<script src="sorttable.js"></script>
<link rel="stylesheet" href="styles.css">
</head>

<header>
<h1>Climbing log</h1>
</header>
<div id="content">

''')


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

    # Contents
    with open('log.html', 'a') as f:
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


def write_table(df, crags):

    df = df.sort_values('date', ascending=False)

    with open('log.html', 'a') as f:
        f.write('<table class="sortable">\n')
        f.write('<tr><th style="width:5%">date</th><th>crag</th><th>route</th><th style="width:5%">grade</th><th>type</th><th>comment</th></tr>\n')
        for index, row in df.iterrows():
            if row['ascent_type'] == 'a':
                continue
            # ---- Grade:
            if str(row['num_grade']) == row['grade']:
                grade = row['grade'] + ' -'
            else:
                grade = str(row['num_grade']) + " (" + row['grade'] + ")"
            # ---- Type:
            if row['ascent_type'] == 'o':
                asc_type = "<td style='color: white; font-weight: bold;'>o</td>"
            elif row['ascent_type'] == 'f':
                asc_type = "<td style='color: yellow; font-weight: bold;'>f</td>"
            elif row['ascent_type'] == 'r':
                asc_type = "<td style='color: red; font-weight: bold;'>r</td>"
            else:
                asc_type = f"<td>{row['ascent_type']}</td>"
            f.write(f"<tr><td>{row['date'].strftime('%d.%m.%y')}</td><td>{row['crag']}</td><td>{row['route']}</td><td>{grade}</td>{asc_type}<td>{row['comment']}</td></tr>\n")
        f.write('</table>\n')