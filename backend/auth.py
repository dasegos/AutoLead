# FastApi imports
from fastapi import Request, status
from fastapi.responses import JSONResponse

# Project imports
from utils import fetch
from config import AppConfig

# Other imports
import aiohttp
from functools import wraps


def has_permission(func):
    '''Decorator to check if user signature is valid.'''
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        return await func(request, *args, **kwargs)
    
        # Aiohttp connection
        # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=AppConfig.SSL_CERT)) as session:
        #     response = await fetch(session.get)
        #     ....
        # if: (signature valid)
        # else:
        #     return JSONResponse(content='User sign is invalid.', status_code=status.HTTP_401_UNAUTHORIZED)

    return wrapper
