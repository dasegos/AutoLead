# Project imports
from .config import config

# Other imports
import aiohttp
from typing import Any


async def get(url: str, params: dict[str, Any]=None):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=config.SSL_CERT)) as session:
        async with session.get(f'{config.CLIENT_URL}{url}', params=params, headers={'AUTHORIZATION' : config.API_TOKEN}) as response:
            json = await response.json()
            return json

async def create_deal_form(contractor_type: str, contractor_id: int):
    data = {'program' : {
                'contentType' : 'Program',
                'id' : config.SETTINGS['program']},
            'state' : {
                'contentType' : 'ProgramState',
                'id' : config.SETTINGS['status']},
            'contractor' : {
                'contentType' : contractor_type,
                'id' : contractor_id},
            'manager' : {
                'contentType' : 'Employee',
                'id' : config.SETTINGS['manager']}
            }
    return data

async def read_logs():
    ...

async def delete_logs():
    ...