import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Secret key for session management. You can generate random strings here:
# https://randomkeygen.com/
SECRET_KEY = 'my precious'

USER_APP_NAME = "HELP IN PT"

USER_UNAUTHENTICATED_ENDPOINT = 'login'

USER_UNAUTHORIZED_ENDPOINT = 'login'