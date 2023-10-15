import click 
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
from .config import gh_approvers
import json


badge_types = ['review', 'practice', 'explore', 'experience', 
               'build', 'lab','community']


@click.command() 
@click.option('-b','--badge-name',help="name of the badge formated like type.YYYY-MM-DD")
@click.option('-a','--approver',help='github username of the badge issuer')
@click.option('-s','--signature',help = "the signature hash to be checked")


def verify_badge(badge_name,approver,signature):
    '''
    check that file path/name matches included key

    .. deprecated:: 23.09
        receipts are no longer in use
    '''
    # create expected message
    badge_bytes = badge_name.encode('utf-8')  # bytes type

    # convert signature
    signature_bytes = bytes.fromhex(signature)

    # read public key for the approver
    # TODO: fix this to read from installed package data
    # TODO: make install save the file 
    with open(approver,'rb') as f:
        public_bytes = f.read() # read file

    signer_key = Ed25519PublicKey.from_public_bytes(public_bytes)
    # Raises InvalidSignature if verification fails
    signer_key.verify(signature_bytes, badge_bytes)

    click.echo(badge_name + ' Verified')
    


@click.command()
@click.option('-j','--json-output',default='badges.json',type=click.File('r'),
                help='json file to parse')
@click.option('-f','--file-out',default=None,type=click.File('w'),
                help='to write to a file, otherwise will echo')

def process_badges(json_output,file_out = None):
    '''
    process gh cli json

    .. deprecated:: 23.09
        receipts are no longer in use
        this may be a valid starting point or useful reference for different processing though
    '''
    
    with open(json_output, 'r') as f:
        PR_list = json.load(f)
     
    #filter for ones with reviews
    reviewed = [(pr['title'], pr['latestReviews'][0])
                for pr in PR_list if pr['latestReviews']]
    # filter to only process approved ones latestReviews.state
    # extract title, latestReviews.author.login, latestReviews.body, 
    logged_badges = [(title,review['author']['login'], review['body'])
                for title,review in reviewed if review['state'] == 'APPROVED']

    # iterate approved
    verified_badges = []
    questioned_badges = []
    for title, reviewer, body in logged_badges:
        signature = [s for s in body.split(' ') if len(s)==128]
        # verify 
        try:
            verify_badge(title, reviewer, signature)
            verified_badges.append(title)
        except InvalidSignature:
            questioned_badges.append(title)


    # add to log 
    report = "verified badges:\n" 
    report += '\n -' + '\n -'.join(verified_badges)
    if questioned_badges:
        report += '\n\nquestioned badges: \n'
        report += '\n -' + '\n -'.join(questioned_badges)

    if file_out:
        with open(file_out,'w') as f:
            f.write()
    else: 
        click.echo(report)
    #  TODO: pair this with a commit to a "badges" branch, so it doesn't create conflicts


    # review_df = badges_df['latestReviews'].apply(pd.Series)[0].apply(pd.Series)
    # author = review_df['author'].apply(pd.Series)



@click.command()
@click.option('-j','--json-output',default='badges.json',type=click.File('r'),
                help='json file to parse')
@click.option('-f','--file-out',default=None,type=click.File('w'),
                help='to write to a file, otherwise will echo')

def get_approved_titles(json_output,file_out = None):
    '''
    process gh cli json

    Parameters
    ----------
    json_output : filename
        file generated from `gh pr list -s all --json title,latestReviews `
    file_out : file name
        file to be generated and store the output
    '''
    
    with open(json_output, 'r') as f:
        PR_list = json.load(f)
        
    #filter for ones with reviews
    reviewed = [(pr['title'], pr['latestReviews'][0])
                for pr in PR_list if pr['latestReviews']]
    # filter to only process approved ones latestReviews.state
    # extract title, latestReviews.author.login, latestReviews.body, 
    logged_badges = [title for title,review in reviewed 
                    if review['state'] == 'APPROVED' and 
                    review['author']['login']in gh_approvers]
    
    out_list = '\n'.join(logged_badges)

    if file_out: 
        titles_by_type = {bt:[t for t in logged_badges if type in t.lower()] 
                          for bt in badge_types}
        verified_by_type = '\n'.join(['## '+bt + ' ('+str(len(bl)) +')' +'\n - '+'\n - '. join(bl) 
                        for bt,bl in titles_by_type.items()])
        valid_badges = [vi for v in titles_by_type.values() for vi in v]
        not_typed = [p for p in logged_badges if not(p in valid_badges)]
        with open(file_out,'w') as f:
            f.write('## all approved ')
            f.write(out_list)
            f.write(verified_by_type)
            f.write('## Cannot match as a typed badge')
            f.write('\n- ' + '\n - '.join(not_typed))
    else: 
        click.echo(out_list)

block_template = '''
# {type}
''' 


# 
# Put this in student repos  
# on:
#   pull_request_review:
#     types: [submitted]

# jobs:
#   approved:
#     if: github.event.review.state == 'approved'
#     runs-on: ubuntu-latest
#     steps:
#       - run: |
#           # figure out how to write to file? 


# on:
#   pull_request_target:
#     types:
#       - closed

# jobs:
#   if_merged:
#     if: github.event.pull_request.merged == true
#     runs-on: ubuntu-latest
#     steps:
#     - run: |
#         gh pr list --state all --json title,latestReviews >>tmp
        # process json to extract badges
