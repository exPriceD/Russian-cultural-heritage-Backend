from app import application
import app.views.views
from app.views.views import api

if __name__ == '__main__':
    application.register_blueprint(api)
    application.run(load_dotenv=True)