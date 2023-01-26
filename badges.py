import click 
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
import json
import pkg_resources as pkgrs

@click.command() 
@click.option('-b','--badge-name',help="name of the badge formated like type.YYYY-MM-DD")
@click.option('-a','--approver',help='github username of the badge issuer')
@click.option('-s','--signature',help = "the signature hash to be checked")

def verify_badge(badge_name,approver,signature):
    '''
    check that file path/name matches included key
    '''
    # create expected message
    badge_bytes = badge_name.encode('utf-8')  # bytes type

    # convert signature
    signature_bytes = bytes.fromhex(signature)

    # read public key for the approver
    # TODO: fix this to read from installed package data
    # TODO: make install save the file 
    approver_rel = os.path.join('signatures', approver)
    approver_key_file = pkgrs.resource_filename(__name__,approver_rel)
    with open(approver_key_file, 'rb') as f:
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
