import os

# ------- local imports -------
from app.app import app

if __name__ == '__main__':
    host = os.environ.get('HOST')
    port = os.environ.get('PORT')
    app.run(host=host, port=port, debug=True)
