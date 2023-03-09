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


def analysis():
    with open('log.html', 'a') as f:
        f.write("\n<h2>Summary</h2>\n")
        f.write('<figure class="left">')
        f.write('<img src="figures/sport_total.png" alt="Sports sends summary" style="width:500px; height:380px; object-fit: cover;">\n')
        f.write('<figcaption>Total sends per grade and type</figcaption>')
        f.write('</figure>\n')
        f.write('<figure class="right">')
        f.write('<img src="figures/sport_time.png" alt="Sports sends summary" style="width:500px; height:380px; object-fit: cover;">\n')
        f.write('<figcaption>Average of top 10 climbs per year</figcaption>')
        f.write('</figure>')


def table(df, crags):

    df = df.sort_values('date', ascending=False)

    with open('log.html', 'a') as f:
        f.write("\n<h2>Log of sends</h2>\n")
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