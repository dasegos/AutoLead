# FastApi imports
from fastapi import FastAPI, Form, Body, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
import uvicorn

# Project imports
from config import AppConfig
from database import SettingsDatabase
from auth import has_permission
from utils import create_deal_form, fetch

# Other imports
import json
import aiohttp
import logging


# Configuration
app = FastAPI(title=AppConfig.APP_TITLE, summary=AppConfig.APP_DESC, docs_url=AppConfig.DOCT_ROUTE)
app.mount('/static', StaticFiles(directory='./static'), 'static')
templates = Jinja2Templates(directory='./templates')
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')


# Routes
# --------------------------------------
@app.get(f'/page/{AppConfig.APP_UUID}') # Main index page with logs and current settings
@has_permission
async def page(request: Request, accountId: str, applicationUuid: str, userSign: str):

    # Aiohttp connection
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=AppConfig.SSL_CERT)) as session:
        current_user = await fetch(func=session.get, url=f'https://{accountId}/api/v3/currentUser', headers={'AUTHORIZATION' : AppConfig.API_TOKEN})

    settings = await SettingsDatabase.get_settings(applicationUuid)

    if request.headers.get('Accept') == 'application/json':
        logging.info(f'Main page API GET-request. From: {request.query_params.get("accountId")} ; {request.query_params.get("applicationUuid")}')
        return JSONResponse({'current_user' : current_user, 'settings' : settings})
    else:
        context = {'request' : request, 'current_user' : current_user, 'settings' : settings}
        logging.info(f'Main page template GET-request. From: {request.query_params.get("accountId")} ; {request.query_params.get("applicationUuid")}')
        return templates.TemplateResponse('page.html', context)


@app.get(f'/settings/{AppConfig.APP_UUID}') # Settings page where you can change settings
@has_permission
async def get_settings(request: Request, accountId: str, applicationUuid: str, userSign: str):

    # Aiohttp connection
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=AppConfig.SSL_CERT)) as session:
        # Requests to get all required data for selection
        client_types_list = await fetch(func=session.get, url=f'https://{accountId}/api/v3/contractorType', params=json.dumps({'fields' : ['id', 'name', 'type'], 'onlyRequestedFields' : True}), headers={'AUTHORIZATION' : AppConfig.API_TOKEN})
        program_list = await fetch(func=session.get, url=f'https://{accountId}/api/v3/program', params=json.dumps({'fields' : ['id', 'name'], 'onlyRequestedFields' : True}), headers={'AUTHORIZATION' : AppConfig.API_TOKEN})
        status_list = await fetch(func=session.get, url=f'https://{accountId}/api/v3/contractorType', params=json.dumps({'fields' : ['id', 'name'], 'onlyRequestedFields' : True}), headers={'AUTHORIZATION' : AppConfig.API_TOKEN})
        employee_list = await fetch(func=session.get, url=f'https://{accountId}/api/v3/employee', params=json.dumps({'fields' : ['id', 'name', 'position'], 'onlyRequestedFields' : True}), headers={'AUTHORIZATION' : AppConfig.API_TOKEN})

    new_settings = {
                    'client_types_list' : client_types_list,
                    'program_list' : program_list,
                    'status_list' : status_list,
                    'employee_list' : employee_list
                    }


    if request.headers.get('Accept') == 'application/json':
        logging.info(f'Settings page API GET-request. From: {request.query_params.get("accountId")} ; {request.query_params.get("applicationUuid")}')
        return JSONResponse(new_settings)
    else:
        current_settings = await SettingsDatabase.get_settings(applicationUuid)
        context = {'request' : request, **new_settings}
        logging.info(f'Settings page template GET-request. From: {request.query_params.get("accountId")} ; {request.query_params.get("applicationUuid")}')
        return templates.TemplateResponse('settings.html', {**context, **current_settings})
    

@app.post(f'/settings/{AppConfig.APP_UUID}') # Completing a POST-request to change settings
@has_permission
async def post_settings(request: Request, accountId: str, applicationUuid: str, userSign: str,
                        client_types: list[int] = Form(default=None), program_id: int = Form(default=None), status_id: int = Form(default=None), employee_id: int = Form(default=None)):
     

    # Since Redis can not store lists, 
    # and `client_types` is a list instance,
    # we have to serialize it to a JSON-formatted
    # string. 

    if client_types is not None: #!important 
        client_types = json.dumps(client_types)

    data = {
            'client_types' : client_types,
            'program_id' : program_id,
            'status_id' : status_id,
            'employee_id' : employee_id
           }
    
    await SettingsDatabase.update_settings(applicationUuid, data) # Updating user's settings in the database

    if request.headers.get('Accept') == 'application/json':
        logging.info(f'Settings page API POST-request. From: {request.query_params.get("accountId")} ; {request.query_params.get("applicationUuid")} | Data: {data}')
        return JSONResponse(data)
    else:
        logging.info(f'Settings page template POST-request. From: {request.query_params.get("accountId")} ; {request.query_params.get("applicationUuid")} | Data: {data}')
        redirect_url = request.url_for('page')
        return RedirectResponse(f'{redirect_url}?{request.query_params}', status_code=302)


@app.post(f'/events/{AppConfig.APP_UUID}') # Endpoint that monitors creation of contractors
async def events(data=Body()):
    # If contractor event is creation & contractor type id in the list
    if (data['event'] == 'on_after_create') and (data['data']['type']['id'] in await SettingsDatabase.get_setting(data['uuid'], 'client_types')):
        deal_data = await create_deal_form(data['model'], data['data']['id'])
        url = f'https://{data['accountInfo']['accountName']}/api/v3/deal' # building a url for POST-request

        # Aiohttp connection
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=AppConfig.SSL_CERT)) as session:
            result = await fetch(func=session.post, url=url, data=deal_data)

        logging.info(f'Events POST-request: {data}\nResponse: {result}')
    # Otherwise don't create a new deal
    else:
        logging.info(f'Events POST-request: {data}\nRequest not processed')
# --------------------------------------


# Running an app
if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', reload=True)