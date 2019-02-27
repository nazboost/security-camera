import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

slack_api_token = os.environ.get('slack_api_token')
slack_channel_id = os.environ.get('slack_channel_id')
