import requests
import click
from datetime import date as dt


@click.command()
@click.option('--type', 'assignment_type', default='prepare',
                help='type can be prepare, review, or practice')
@click.option('--date', default=None)


def get_assignment(date, assignment_type = 'prepare'):

    if not(date):
        date = dt.today().isoformat()

    base_url = 'https://raw.githubusercontent.com/introcompsys/fall2022/main/_'

    md_activity = md_to_checklist(date, assignment_type)
    click.echo( md_activity)

def fetch_to_checklist(date, assignment_type = 'prepare'):
    base_url = 'https://raw.githubusercontent.com/introcompsys/spring2022/main/_'

    path = base_url +assignment_type + '/' + date +'.md'
    return requests.get(path).text.replace('1. ','- [ ] ')

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
