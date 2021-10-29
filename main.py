import os
import sys
from dotenv import load_dotenv
from modules.github import Github

load_dotenv()
if len(sys.argv) == 1:
    print("Require Arguments")
    exit

argument = sys.argv[1]
github = Github(os.getenv('CLIENT_ID'))

if argument == 'auth':
    github.auth()

if argument == 'unfollow':
    github.unfollow()
