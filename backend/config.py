# Other imports
import os
import ssl, certifi
from dotenv import load_dotenv


load_dotenv()


class AppConfig:
    '''Конфигурация микросервиса - приложения FastAPI'''
    APP_TITLE         : str            = 'АвтоЛИД'
    APP_DESC          : str            = 'Автоматическое создание сделки при создании клиента'
    DOCT_ROUTE        : str            = '/docs'
    API_TOKEN         : str            = f'Bearer {os.getenv('API_TOKEN')}'
    APP_UUID          : str            = os.getenv('APP_UUID')
    SSL_CERT          : ssl.SSLContext = ssl.create_default_context(cafile=certifi.where())


class RedisConfig:
    '''Конфигурация No-SQL БД Redis'''
    HOST  : str = 'redis'
    PORT  : int = 6379
    DB    : int = 1
    ATTRS : list[str] = ['client_types', 'program_id', 'status_id', 'employee_id']
