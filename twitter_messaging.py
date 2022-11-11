import json
import os

import dotenv
import typer
import azure.core.exceptions
from azqueuetweeter import QueueTweeter, storage, twitter
from gh_issues import Issue, Repo
import strip_markdown
import spacy

nlp = spacy.load("en_core_web_sm")

dotenv.load_dotenv()
queue_name=os.environ.get("AZURE_STORAGE_QUEUE_NAME")

Storage = storage.Auth(
    connection_string=os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
    queue_name=queue_name,
)

print(Storage.Client)

Twitter = twitter.Auth(
    consumer_key=os.environ.get('CONSUMER_KEY'),
    consumer_secret=os.environ.get('CONSUMER_SECRET'),
    access_token=os.environ.get('ACCOUNT_ACCESS_TOKEN'),
    access_token_secret=os.environ.get('ACCOUNT_ACCESS_TOKEN_SECRET'),
)

def main(owner:str, repo:str, issue_number:int):
    qt = QueueTweeter(Storage, Twitter)
    _repo = Repo(owner, repo)
    _issue = Issue.from_issue_number(
            repo=_repo,
            issue_number=issue_number,
            )

    try:
        Storage.Client.create_queue()    
    except azure.core.exceptions.ResourceExistsError:
        pass

    for issue in _issue.get_content_issues('issues'):
        msg = nlp(strip_markdown.strip_markdown(issue.summary)).sents
        qt.queue_message(next(msg))

if __name__ == "__main__":
    typer.run(main)