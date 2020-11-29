"""Web Server Gateway Interface"""

import os

##################
# FOR PRODUCTION
####################
###########################
from flaskapp.app.app import create_app

app = create_app(os.getenv('FLASK_CONFIG'))
# rather than import
###########################
"""

if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    app = create_app('testing')
    app.run(host='0.0.0.0', debug=True)
"""