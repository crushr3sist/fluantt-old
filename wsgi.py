from src.views.login import *
from src import app
if __name__=='__main__':
        
    app.run(ssl_context=('certificates/cert.pem', 'certificates/key.pem'))
