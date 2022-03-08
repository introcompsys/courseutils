import pandas as pd
import click

@click.command()
@click.option('--type', default= 'all',
                help= 'select only prepare, only practice, or all')



def get_file_list(type ):
    '''
    get the current list of expected files from the course website

    Parameters
    ----------
    type : string (default = 'all')
        how to filter the table, other values are prepare or practice
    '''
    df = pd.read_html('http://introcompsys.github.io/spring2022/activities/kwl.html')[0]

    if type == 'all':
        click.echo(' '.join(df['file'].to_list()))
    else:
        # select rows by type
        df_selected_type = df[df['type (prepare/practice)']==type]
        click.echo(' '.join(df_selected_type['file'].to_list()))
