import os
import requests
from dotenv import load_dotenv

from classes import PassworkClient

load_dotenv()

client = PassworkClient(os.getenv('EMAIL'), os.getenv('password'))
print(client.workspaceApi.get_current_user_workspaces())