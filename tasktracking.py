import requests
import click



@click.command()
@click.option('--type', 'assignment_type', default='prepare',
                help='type can be prepare, review, or practice')
@click.option('--date', default='2022-02-03')


def get_assignment(date, assignment_type = 'prepare'):
    base_url = 'https://raw.githubusercontent.com/introcompsys/spring2022/main/_'
    path = base_url +assignment_type + '/' + date +'.md'
    click.echo( requests.get(path).text.replace('1. ','- [ ] '))

def get_all(date):
    '''
    '''
    type_list = ['prepare','review','practice']

    for assignment_type in type_list:
        try:
            get_assignment(date,assignment_type)
        except:
            print('no ' + assignment_type + ' currently posted for this date')
