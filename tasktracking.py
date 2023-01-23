import requests
import click
from datetime import date as dt
from datetime import timedelta
import re
base_url = 'https://raw.githubusercontent.com/introcompsys/spring2023/main/_'

# MW 
day_adj_MW = {0:timedelta(days=0), 2:timedelta(days=0),
            1:timedelta(days=1), 3:timedelta(days=1),
            4:timedelta(days=2),5:timedelta(days=3),
            6:timedelta(days=4)}

day_adj_TTh = {1: timedelta(days=0), 3: timedelta(days=0),
              2: timedelta(days=1), 4: timedelta(days=1),
              5: timedelta(days=2), 6: timedelta(days=3),
              0: timedelta(days=4)}

day_adj = day_adj_TTh


@click.command()
@click.option('--type', 'assignment_type', default='prepare',
                help='type can be prepare, review, or practice')
@click.option('--date', default=None,
                help='date should be YYYY-MM-DD of the tasks you want')


def get_assignment(date, assignment_type = 'prepare'):

    if not(date):
        today = dt.today()
        last_class = today- day_adj[today.weekday()]
        date = last_class.isoformat()

    
    md_activity = fetch_to_checklist(date, assignment_type)
    click.echo( md_activity)



@ click.command()
@click.option('--type', 'assignment_type', default='prepare',
              help='type can be prepare, review, or practice')
@click.option('--date', default=None,
              help='date should be YYYY-MM-DD of the tasks you want and must be valid')

def fetch_to_checklist(date, assignment_type = 'prepare'):


    path = base_url +assignment_type + '/' + date +'.md'
    # get and convert to checklist from enumerated
    fetched_instructions = requests.get(path).text
    check_list = re.sub('[0-9]\. ', '- [ ] ', fetched_instructions)

    # remove index items 
    cleaned_lists = re.sub(r'\n```\{index\} (?P<file>.*\n)```', '', check_list)
    cleaned_lists = re.sub('{index}','',cleaned_lists)
    # and return
    return cleaned_lists


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
