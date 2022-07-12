# -*- coding: utf-8 -*-
from datetime import datetime
import pytz


def to_number_of_month(month_str):
    nick_month = {'jan': 'januari', 'feb': 'februari', 'mar': 'maret', 'apr': 'april', 'mei': 'mei', 'jun': 'juni', 'jul': 'juli',
                  'agu': 'agustus', 'ags': 'agustus', 'agu/ags': 'agustus', 'sep': 'september', 'okt': 'oktober', 'nov': 'november', 'des': 'desember'}
    try:
        month_str = nick_month[month_str]
    except:
        month_str = month_str
    month_lst = [('januari', '01'), ('februari', '02'), ('maret', '03'), ('april', '04'),
                 ('mei', '05'), ('juni', '06'), ('juli', '07'), ('agustus', '08'),
                 ('september', '09'), ('oktober', '10'), ('november', '11'), ('december', '12')]
    month = [x[1] for x in month_lst if x[0] == month_str]
    if month:
        return month[0]
    return None


def remove_tabs(content):
    content = content.replace('\t', '').replace('\r', '').strip()
    return content


def utc_to_local_month(month):
    local_month = None
    month = str(month).lower()
    month_utc = {'january': 'januari', 'february': 'februari', 'march': 'maret', 'april': 'april', 'may': 'mei', 'june': 'juni',
                 'july': 'juli', 'august': 'agustus', 'september': 'september', 'october': 'oktober', 'november': 'november', 'december': 'desember'}
    try:
        local_month = month_utc[month]
    except:
        local_month = month
    return local_month


def date_parse(date_string):
    local_format = pytz.timezone('Asia/Jakarta')
    date_lst = date_string.split(' ')
    date = None
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
            elif len(date_lst[-1].split(':')) == 2:
                date_str = '{}/{}/{} {}'.format(
                    date_lst[0],
                    to_number_of_month(date_lst[1].lower()),
                    date_lst[2].replace(',', '').strip(),
                    date_lst[3].strip())
                print(date_str)
                date = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        except:
            pass
    elif len(date_lst) == 6:
        date_lst = date_lst[1:-1]
        try:
            if len(date_lst[-1].split(':')) == 2:
                date_str = '{}/{}/{} {}'.format(date_lst[0],
                                                to_number_of_month(
                    date_lst[1].lower()),
                    date_lst[2].replace(',', ''), date_lst[3])
                date = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        except:
            pass
    # if len(date_lst) == 3:
    #     try:
    #         date_lst = date_lst[0:2]
    #         date_str = ' '.join(date_lst)
    #         date = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
    #     except:
    #         pass
    # else:
    #     try:
    #         date_lst = date_lst[:-1]
    #         date_str = ' '.join(date_lst)
    #         date = datetime.strptime(date_str, '%Y/%m/%d %H:%M:%S')
    #     except:
    #         date_str = ' '.join(date_lst)
    #         date = datetime.strptime(date_str+":00", '%d/%m/%Y %H:%M:%S')
    if date:
        local_time = local_format.localize(date, is_dst=None)
        utc_time = local_time.astimezone(pytz.utc)
        return utc_time
    return None


def remove_baca_juga(content):
    content = content.replace('Baca Juga', '')
    return content
