from flask import Flask

app = Flask(__name__)
@app.route('/')
def show_user_profile():
    # Muestra el perfil del usuarioreturn 
    return f'Perfil de usuario'

app.run()