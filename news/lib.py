# -*- coding: utf-8 -*-

def to_number_of_month(month_str):
    month_lst = [('januari', '01'), ('februari', '02'), ('maret', '03'), ('april', '04'),
                 ('mei', '05'), ('juni', '06'), ('juli', '07'), ('agustus', '08'),
                 ('september', '09'), ('oktober', '10'), ('november', '11'), ('december', '12')]
    month = [x[1] for x in month_lst if x[0] == month_str]
    return ''.join(month)

def remove_tabs(content):
    content = content.replace('\t','').replace('\r','').strip()
    return content
