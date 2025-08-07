# FastApi imports
from fastapi import FastAPI, Request, Body, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Project imports
from .config import config
from .utils import get, create_deal_form, read_logs

# Other imports
import json
import aiohttp
import logging


app = FastAPI()
app.mount('/static', StaticFiles(directory='./static'), 'static')
templates = Jinja2Templates(directory='./templates')
logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', format='%(asctime)s %(levelname)s %(message)s')


@app.post('/receiving_clients')
async def receiving_clients(data=Body()):
    if (data['event'] == 'on_after_create') and (data[''] in config.SETTINGS['client_type_list']):
        deal_data = await create_deal_form()
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=config.SSL_CERT)) as session:
            async with session.post(f'{config.CLIENT_URL}/api/v3/deal', json=deal_data, headers={'AUTHORIZATION' : config.API_TOKEN}) as response:
                result = response.json()
                logging.INFO(f'Data: {data}; Response: {result}')
                return result
    logging.INFO(f'Data: {data}; Response: not processed')


@app.get('/settings')
async def get_settings(request: Request):
    program_list = await get('/program', params=json.dumps({'fields' : ['id', 'name'], 'onlyRequestedFields' : True}))
    status_list  = [await get(f'/programState/{program['id']}', params=json.dumps({'fields' : ['id', 'name'], 'onlyRequestedFields' : True})) for program in program_list['data']]

    context = {
        'request'              : request,

        'current_user'         : await get('/currentUser'),

        'client_type_list'     : await get('/contractorType', params=json.dumps({'fields' : ['id', 'name', 'type'], 'onlyRequestedFields' : True})),
        'current_client_types' : config.SETTINGS['client_type_list'],

        'program_list'         : program_list,
        'current_program_id'   : config.SETTINGS['program'],

        'status_list'          : status_list,
        'current_status_id'    : config.SETTINGS['status'],

        'employee_list'        : await get('/employee', params=json.dumps({'fields' : ['id', 'name', 'position'], 'onlyRequestedFields' : True})),
        'current_employee_id'  : config.SETTINGS['manager'],
    }
    return templates.TemplateResponse('settings.html', context)


@app.post('/settings')
async def post_settings(client_type_list: list[int] = Form(default=None), program: int = Form(default=None), status: int = Form(default=None), manager: int = Form(default=None)):
    data = {'client_type_list' : client_type_list, 'program' : program, 'status' : status, 'manager' : manager}
    await config.update(data)
    return data
    

@app.get('/logs')
async def logs(request: Request):
    context = {
        'request'   : request,
        'logs_list' : await read_logs()
    }
    return templates.TemplateResponse('logs.html', context)