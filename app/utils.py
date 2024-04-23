from datetime import datetime
import pytz

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def get_current_time(timezone='Europe/Moscow'):
    moscow_tz = pytz.timezone(timezone)
    moscow_time = datetime.now(moscow_tz)
    formatted_time = moscow_time.strftime('%d.%m.%y %H:%M')
    return formatted_time


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
