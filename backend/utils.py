# Project imports
from database import SettingsDatabase

#  Other imports
from aiohttp import ClientSession
from typing import Any, Optional, Union


async def fetch(func: Union[ClientSession.get, ClientSession.post, ClientSession.patch, ClientSession.delete], # function to call
                url: str, # target url
                params: dict[str, Any]=None, 
                data: dict[str, Any]=None,
                headers: dict[str, Any]=None):
    '''The function to fetch response from Megaplan\n
    
       Parameters
       -----------
       func    : `Union[ClientSession.get, ClientSession.post, ClientSession.patch, ClientSession.delete]`, required (function to call)\n
       url     : `str`, required (target url)
       params  : `dict[str, Any]`, not required, default=`None` (params)
       data    : `dict[str, Any]`, not required, default=`None` (data)
       headers : `dict[str, Any]`, not required, default=`None` (headers)
    '''
    async with func(url, params=params, json=data, headers=headers) as response:
        return await response.json()


async def create_deal_form(uid: str, contractor_type: str, contractor_id: int) -> dict[str, dict[str, Any]]:
    '''The function to generate a data dictionary for a deal-creating request.
       
       Parameters
       -----------
       uid             : `str`, required (unique account identifier)\n
       contractor_type : `str`, required\n
       contractor_id   : `int`, required
    '''
    data = {'program' : {
                'contentType' : 'Program',
                'id' : await SettingsDatabase.get_setting(uid, 'program_id')
                },
            'state' : {
                'contentType' : 'ProgramState',
                'id' : await SettingsDatabase.get_setting(uid, 'status_id')
                },
            'contractor' : {
                'contentType' : contractor_type,
                'id' : contractor_id
                },
            'manager' : {
                'contentType' : 'Employee',
                'id' : await SettingsDatabase.get_setting(uid, 'employee_id')
                }
            }
    return data