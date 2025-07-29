import os

class Config:
    SECRET_KEY       = os.environ.get('SECRET_KEY', 'fallback-secret')
    DAILY_HOUR_LIMIT = int(os.environ.get('DAILY_HOUR_LIMIT', 8))

    # Trello only
    TRELLO_KEY       = os.environ.get('TRELLO_KEY')
    TRELLO_TOKEN     = os.environ.get('TRELLO_TOKEN')
