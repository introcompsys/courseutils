import click 
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

@click.command() 

def verify_badge(badge_name,approver,signature):
    '''
    check that file path/name matches included key
    '''
    # create expected message
    badge_bytes = b(badge_name) # bytes type

    # convert signature
    signature_bytes = bytes.fromhex(signature)

    # read public key for the approver
    # TODO: fix this to read from installed package data
    # TODO: make install save the file 
    with open(approver,'b') as f:
        public_bytes = f.read() # read file

    signer_key = Ed25519PublicKey.from_public_bytes(public_bytes)
    # Raises InvalidSignature if verification fails
    signer_key.verify(signature_bytes, badge_bytes)


@click.command()

def collect_pr_badges(json_output):
    '''
    process gh cli json
    '''
    # parse json 

    # extract title, latestReviews.author.login, latestReviews.body, latestReviews.state

    # filter to only process approved ones 

    # iterate approved

        # verify 

        # add to log file 

    #  TODO: pair this with a commit to a "badges" branch, so it doesn't create conflicts



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
