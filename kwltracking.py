import pandas as pd
import numpy as np
import os
import click

repo = 'http://introcompsys.github.io/fall2023/'

@click.command()
@click.option('--practice', default=False, is_flag=True,
                help='flag for more practice related files or not')
@click.option('--zone', default='graded')

def get_file_list(zone='graded', practice =False):
    '''
    scrape the list, filter and echo back
    '''
    types = ['prepare','review']
    if practice:
        types.append('practice')

    # click.echo('in program')
    df = pd.read_html(repo + 'activities/kwl.html')[0]
    df_filt = filter_files(df,zone, types)
    click.echo(' '.join(df_filt['file'].to_list()))


def filter_files(df,zone, types):
    '''
    filter the dataframe based on a zone and type list
    '''
    zidx = df['zone'] ==zone
    tidx = np.sum(np.asarray([df['type'].str.contains(typ)  for typ in types]),axis=0)>0
    return df[np.product([tidx,zidx],axis=0)==1]


@click.command()
@click.option('--practice', default=False, is_flag=True,
                help='flag formore practice related files or not')
@click.option('--zone', default='graded')

def count_files(zone='graded',practice =False):
    '''
    get the file list, count per type by date, produce a status report 

    Parameters
    ----------
    zone : string {graded}
        graded or gradefree zone 
    practice : boolean {False}
        include more practice tasks or not
    '''
    types = ['prepare','review']
    if practice:
        types.append('practice')

    # click.echo('in program')
    df = pd.read_html(repo + 'activities/kwl.html')[0]
    df_filt = filter_files(df,zone, types)

    # get files in the current directory and subfodlers, but not git
    cur_files = set([f for cd,d,fn in os.walk('.') for f in fn if not('.git' in cd)])

    # filter by current files
    # check the whole file table for each present file, then sum and bool by taking all nonzero
    incomplete_dates = []
    bonus_counts =0
    missing_by_date = {}
    complete_count = 0
    bonus_dates = ['2022-12-05','2022-12-07','2022-12-12']
    for date, ddf in df_filt.groupby('date'):
        date_set = set(ddf['file'].to_list())
        missing = date_set-cur_files
        if missing:
            incomplete_dates.append(date)
            missing_by_date[date] = ' '.join(list(missing))
        else:
            complete_count +=1
            if date in bonus_dates:
                bonus_counts +=1 


    click.echo(str(complete_count)+ ' dates complete')
    click.echo('-----------------------------------')
    click.echo('dates missing 1 or more files: ' + ' '.join(incomplete_dates))
    click.echo('-----------------------------------')
    click.echo('\n'.join([' : '.join([d,l]) for d,l in missing_by_date.items()]))
    click.echo('-----------------------------------')
    click.echo(str(bonus_counts)+ ' bonus dates complete')
    click.echo('-----------------------------------')
    click.echo(str(bonus_counts+complete_count)+ 'effective dates complete')
    
    return 




    # count unique dates
@click.command()

def count_extra_files():
    jb_files = ['_toc.yml','_config.yml','requirements.txt']

    # click.echo('in program')
    df = pd.read_html(repo + 'activities/kwl.html')[0]
    expected_files = set(df['file'].to_list() + jb_files)

    # get files in the current directory and subfodlers, but not git
    cur_files = set([f for cd,d,fn in os.walk('.') for f in fn if not('.git' in cd)])

    # do a set differences
    extra_files = cur_files - expected_files

    click.echo(' '.join(extra_files))
