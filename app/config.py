# Other imports
import os, ssl, certifi
from ssl import SSLContext
from typing import Optional
from dotenv import load_dotenv


load_dotenv()

class Config:
    API_TOKEN    : str        = f'Bearer {os.getenv('API_TOKEN')}'
    CLIENT_URL   : str        = os.getenv('CLIENT_URL')
    SSL_CERT     : SSLContext = ssl.create_default_context(cafile=certifi.where())
    SETTINGS     : dict[str, int | list[int]] = {'client_type_list' : None, 'program' : None, 'status' : None, 'manager' : None}

    async def update(self, data: dict[str, int | list[int]]) -> None:
        for key, value in data.items():
            if value is not None:
                self.SETTINGS[key] = value


config = Config()