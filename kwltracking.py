import pandas as pd
import click

@click.command()
def get_file_list():
    # click.echo('in program')
    df = pd.read_html('http://introcompsys.github.io/spring2022/activities/kwl.html')[0]
    click.echo(' '.join(df['file'].to_list()))
