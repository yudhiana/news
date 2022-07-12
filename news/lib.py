# -*- coding: utf-8 -*-
from datetime import datetime
import pytz


def to_number_of_month(month_str):
    nick_month = {'jan': 'januari', 'feb': 'februari', 'mar': 'maret', 'apr': 'april', 'mei': 'mei', 'jun': 'juni', 'jul': 'juli',
                  'agu': 'agustus', 'ags': 'agustus', 'agu/ags': 'agustus', 'sep': 'september', 'okt': 'oktober', 'nov': 'november', 'des': 'desember'}
    try:
        month_str = nick_month[month_str]
    except:
        pass
    month_lst = [('januari', '01'), ('februari', '02'), ('maret', '03'), ('april', '04'),
                 ('mei', '05'), ('juni', '06'), ('juli', '07'), ('agustus', '08'),
                 ('september', '09'), ('oktober', '10'), ('november', '11'), ('december', '12')]
    month = [x[1] for x in month_lst if x[0] == month_str]
    return ''.join(month)


def remove_tabs(content):
    content = content.replace('\t', '').replace('\r', '').strip()
    return content


def utc_to_id_month(month):
    month_name = None
    month = str(month).lower()
    UTC = [('january', 'januari'), ('february', 'februari'), ('march', 'maret'), ('april', 'april'),
           ('may', 'mei'), ('june', 'juni'), ('july', 'juli'), ('august', 'agustus'),
           ('september', 'september'), ('october', 'oktober'), ('november', 'november'), ('december', 'desember')]

    for mth in UTC:
        if mth[0] != month:
            month_name = month
        else:
            month_name = mth[1]
            break
    return month_name


def date_parse(date_string):
    local_format = pytz.timezone('Asia/Jakarta')
    date_lst = date_string.split(' ')
    if len(date_lst) == 5:
        try:
            date_lst = date_lst[:-1]
            if len(date_lst[-1].split(':')) == 3:
                date_str = '{}/{}/{} {}'.format(
                    date_lst[0],
                    to_number_of_month(date_lst[1].lower()),
                    date_lst[2].replace(',', '').strip(),
                    date_lst[3].strip())
                date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
        except:
            pass
    elif len(date_lst) != 3:
        date_lst = date_lst[1:-1]
        date_str = '{}/{}/{} {}:00'.format(date_lst[0],
                                           to_number_of_month(
                                               date_lst[1].lower()),
                                           date_lst[2].replace(',', ''), date_lst[3])
        date = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S')
    else:
        try:
            date_lst = date_lst[:-1]
            date_str = ' '.join(date_lst)
            date = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
        except:
            date_str = ' '.join(date_lst)
            date = datetime.strptime(date_str+":00", '%d/%m/%Y %H:%M:%S')
    local_time = local_format.localize(date, is_dst=None)
    utc_time = local_time.astimezone(pytz.utc)
    return utc_time


def remove_baca_juga(content):
    content = content.replace('Baca Juga', '')
    return content
