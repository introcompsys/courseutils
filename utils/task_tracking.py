import click
import urllib.request as urlreq


base_url = 'https://raw.githubusercontent.com/introcompsys/spring2022/main/_'



@click.command()
@click.argument('date')
@click.option('--type', default='practice')



def get_task_text(date,type='practice'):
    '''

    '''
    # create the full url
    if type in ['practice', 'prepare']:
        url_list = [base_url + type + date + '.md']
    elif type == 'both':
        url_list = [base_url + ty + date + '.md' for ty in ['practice', 'prepare']]

    text = ''
    for url in url_list:
        # read the file and concatenate
        text += urlreq.urlopen(url).str + '\n'

    # convert from bullets to checklist items
    text.replace('- ', '- [ ] ')

    click.echo(text)
