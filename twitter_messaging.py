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
    consumer_key=os.environ.get('CONSUMER-KEY'),
    consumer_secret=os.environ.get('CONSUMER-SECRET'),
    access_token=os.environ.get('ACCOUNT-ACCESS-TOKEN'),
    access_token_secret=os.environ.get('ACCOUNT-ACCESS-TOKEN-SECRET'),
)




def main(qt, issue_number:int):
    _repo = Repo(owner, repo)
    issues = Issue(_repo, issue_number)

    for issue in issues.get_content_issues('topics'):
        queue_tweet(QueueTweeter(Storage, Twitter), issue)    

if __name__ == "__main__":
     qt = QueueTweeter(Storage, Twitter)
    typer.run(main)