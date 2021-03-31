# -*- coding: utf-8 -*-

def to_number_of_month(month_str):
    nick_month = {'jan':'januari','feb':'februari','mar':'maret','april':'april','mei':'mei','jun':'juni','agustus':'agustus','sep':'september','okt':'oktober','nov':'november','des':'desember'}
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
           ('may', 'mei'), ('june', 'juni'), ('july', 'juli'), ('august', 'agustus'), ('september', 'september'),
           ('october', 'oktober'), ('november', 'november'), ('december', 'desember')]

    for mth in UTC:
        if mth[0] != month:
            month_name = month
        else:
            month_name = mth[1]
            break
    return month_name
