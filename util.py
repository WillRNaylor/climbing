import os
import re
import datetime
import pandas as pd


def get_crag_dict(file):

    with open(file, 'r') as f:
        lines = f.readlines()

    crags = dict()
    for line in lines:
        line_parts = line.split(":")
        assert len(line_parts) == 2
        crag = line_parts[0].split(";")
        key = line_parts[1]
        crags[key.lstrip().rstrip().lower()] = [x.lstrip().rstrip() for x in crag]
    
    return crags


def get_grade_conv(file):

    with open(file, 'r') as f:
        lines = f.readlines()

    grades = dict()
    for line in lines:
        line_parts = line.split(":")
        assert len(line_parts) == 2
        grades[line_parts[0].lstrip().rstrip().lower()] = int(line_parts[1])
    
    return grades


def is_date(line):
    date_regex = re.compile(r'\d\d\.\d\d\.\d\d')
    return re.fullmatch(date_regex, line)


def read_log_file(file, grades, WARNINGS=True):

    with open(file, 'r') as f:
        lines = f.readlines()
    lines = [l[:-1] for l in lines]  # Remvoe the '\n'

    date = None
    crag = None
    french_grades = list(grades.keys())
    
    log = []
    for i, line in enumerate(lines):
        if len(line) == 0:
            continue
        if is_date(line):
            date = datetime.datetime.strptime(line, '%d.%m.%y').date()
            continue
        if line.rstrip()[-1] == ':':
            crag = line.rstrip()[:-1].lower()
            continue
        else:
            entry = line.split(';')
            if (len(entry) < 3) or (len(entry) > 4):
                print(f'ERROR: Weird line (l.{i + 1}): {line}')
                continue
            # Convert grade
            route = entry[0].lstrip().rstrip()
            grade = entry[1].lstrip().rstrip()
            if grade in french_grades:
                num_grade = grades[grade]
            elif grade[0] in ['B', 'V']:
                if WARNINGS:
                    print(f'WARNING: Skipping boulders for now (l.{i + 1}): {line}')
                num_grade = 0
            else:
                num_grade = int(grade)
            ascent_type = entry[2].lstrip().rstrip()
            if len(entry) == 3:
                comment = ''
            else:
                comment = entry[3].lstrip().rstrip()
            
            log.append([date, crag, route, grade, num_grade, ascent_type, comment])
    
    return pd.DataFrame(log, columns=['date', 'crag', 'route', 'grade', 'num_grade', 'ascent_type', 'comment'])
