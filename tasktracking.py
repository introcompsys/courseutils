import requests
import click
from datetime import date as dt
from datetime import timedelta
import re
base_url = 'https://raw.githubusercontent.com/introcompsys/fall2022/main/_'


day_adj = {0:timedelta(days=0), 2:timedelta(days=0),
            1:timedelta(days=1), 3:timedelta(days=1),
            4:timedelta(days=2),5:timedelta(days=3),
            6:timedelta(days=4)}


@click.command()
@click.option('--type', 'assignment_type', default='prepare',
                help='type can be prepare, review, or practice')
@click.option('--date', default=None)


def get_assignment(date, assignment_type = 'prepare'):

    if not(date):
        today = dt.today()
        last_class = today- day_adj[today.weekday()]
        date = last_class.isoformat()

    
    md_activity = fetch_to_checklist(date, assignment_type)
    click.echo( md_activity)




def fetch_to_checklist(date, assignment_type = 'prepare'):


    path = base_url +assignment_type + '/' + date +'.md'
    check_list = requests.get(path).text.replace('1. ','- [ ] ')

    # remove index items and return
    return re.sub(r'\n```\{index\} (?P<file>.*\n)```','',check_list)


@click.command()
@click.option('--type', 'assignment_type', default='prepare',
                help='type can be prepare, review, or practice')
@click.option('--date', default=None)
def get_all(date):
    '''
    '''
    type_list = ['prepare','review','practice']
    activities = []
    for assignment_type in type_list:
        try:
            activities.append(get_assignment(date,assignment_type))
        except:
            print('no ' + assignment_type + ' currently posted for this date')
