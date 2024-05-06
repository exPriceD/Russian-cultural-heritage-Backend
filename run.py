from app import application
from app.views.views import api

if __name__ == '__main__':
    application.register_blueprint(api)
    application.run(host='0.0.0.0', port=5000, load_dotenv=True)
