import click 
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
import json

gh_approvers = ['brownsarahm','ascott20','marcinpawlukiewicz']

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
    reviewed = [(pr['title'], pr['reviews'][0])
                for pr in PR_list if pr['reviews']]
    # filter to only process approved ones reviews.state
    # extract title, reviews.author.login, reviews.body, 
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


    # review_df = badges_df['reviews'].apply(pd.Series)[0].apply(pd.Series)
    # author = review_df['author'].apply(pd.Series)



@click.command()
@click.argument('json-output', type =click.Path(exists=True))
@click.option('-f','--file-out',default=None,
                help='to write to a file, otherwise will use stdout')
def cli_get_approved_titles(json_output,file_out = None):
    '''
    list PR titles from json or - to use std in  that have been approved by an official approver 
    
    gh pr list -s all --json title,reviews
      
     
    '''

    get_approved_titles(json_output,file_out)


def get_approved_titles(json_output, file_out = None):
    '''
    process gh cli json

    Parameters
    ----------
    json_output : filename
        file generated from `gh pr list -s all --json title,reviews `
    file_out : file name
        file to be generated and store the output
    '''
    
    with open(json_output, 'r') as f:
        PR_list = json.load(f)
        
    #filter for ones with reviews
    reviewed = [(pr['title'], pr['reviews'][0])
                for pr in PR_list if pr['reviews']]
    # filter to only process approved ones reviews.state
    # extract title, reviews.author.login, reviews.body, 
    logged_badges = [title for title,review in reviewed 
                    if review['state'] == 'APPROVED' and 
                    review['author']['login']in gh_approvers]
    
    

    if file_out: 
        titles_by_type = {bt:[t for t in logged_badges if bt in t.lower()] 
                          for bt in badge_types}
        verified_by_type = '\n' +  '\n'.join(['\n## '+bt + ' ('+str(len(bl)) +')' +'\n- '+'\n- '. join(bl) 
                        for bt,bl in titles_by_type.items() if len(bl)>0 ])
        valid_badges = [vi for v in titles_by_type.values() for vi in v]
        not_typed = [p for p in logged_badges if not(p in valid_badges) ]
        with open(file_out,'w') as f:
            f.write('## all approved \n\n')
            f.write('- ' + '\n- '.join(logged_badges))
            f.write(verified_by_type)

            if len(not_typed) >0 :
                f.write('\n\n## Approved, not badges')
                f.write('\n- ' + '\n - '.join(not_typed))
                f.write('\n')
    else: 
        click.echo('\n'.join(logged_badges))

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
#         gh pr list --state all --json title,reviews >>tmp
        # process json to extract badges
