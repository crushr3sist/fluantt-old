import platform, os, cowsay
from subprocess import Popen

def install():
    try:
        if platform.system()=='Windows':
            with open(f'{os.getcwd()}/inst.bat','w+') as inst:
                inst.write('''
                pip install 
                flask 
                flask_socketio 
                cowsay
                flask 
                SQLAlchemy 
                connexion 
                Flask-Restless 
                Flask-Potion 
                flask-restplus 
                Flask-Admin 
                Flask-Analytics
                Flask-Security 
                Flask-Login 
                Flask-User 
                Flask-SQLAlchem
                Flask-WTF 
                Flask-Cors 
                ''')
            inst.close
            p = os.popen('inst.bat', cwd=os.getcwd())
            stdout, stderr = p.communicate()

            # subprocess.call([rf'cd {os.getcwd()}\ && bat inst.bat'])
            cowsay.beavis('install was successful')
            os.remove('inst.bat')
            
        elif platform.system() == "Linux" or 'Darwin' :
            with open(f'{os.getcwd()}/inst.sh','w+') as inst:
                inst.write('''
                pip install 
                flask 
                flask_socketio 
                cowsay
                flask 
                SQLAlchemy 
                connexion 
                Flask-Restless 
                Flask-Potion 
                flask-restplus 
                Flask-Admin 
                Flask-Analytics
                Flask-Security 
                Flask-Login 
                Flask-User 
                Flask-SQLAlchem
                Flask-WTF 
                Flask-Cors 
                ''')
            inst.close
            # subprocess.call(rf'{os.getcwd()}/inst.sh')
            cowsay.beavis('install was successful')
            os.remove('inst.bat')
    except:
        cowsay.beavis('There was a error in the installation, i tried everything.\nplease make sure everything is installed mate.')
