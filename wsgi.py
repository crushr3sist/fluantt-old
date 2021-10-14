from src.views.login import *
from src import app
if __name__=='__main__':
        
    app.run(ssl_context='adhoc',port = 8080 , debug=True)
