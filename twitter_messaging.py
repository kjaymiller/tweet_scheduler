import json
import os

import dotenv
from typer import Typer
from azqueuetweeter import QueueTweeter, storage, twitter
from gh_issues import Issue, Repo

dotenv.load_dotenv()

app = Typer()

Storage = storage.Auth(
    connection_string=os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
    queue_name=os.environ.get("AZURE_STORAGE_QUEUE_NAME"),
)

Twitter = twitter.Auth(
    consumer_key='CONSUMER-KEY',
    consumer_secret='CONSUMER-SECRET',
    access_token='ACCOUNT-ACCESS-TOKEN',
    access_token_secret='ACCOUNT-ACCESS-TOKEN-SECRET',
)


def queue_tweet(qt, issue):
    qt = QueueTweeter(Storage, Twitter)
    return qt.queue_message(issue.social)


def main(owner:str, repo:str, issue_number:int):
    _repo = Repo(owner, repo)
    issues = Issue(_repo, issue_number)

    for issue in issues.get_content_issues('topics'):
        .

if __name__ == "__main__":
    typer.run(main)



