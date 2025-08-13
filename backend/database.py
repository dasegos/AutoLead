# Project imports
from .config import RedisConfig

# Other imports
import redis.asyncio as aioredis
from typing import Any, Optional, Union


class SettingsDatabase:
    '''Class to manage Redis database for storing users' settings'''
    
    
    @classmethod
    async def create_setting(cls, uid: str) -> None:
        '''
        '''
        async with aioredis.Redis(host=RedisConfig.HOST, port=RedisConfig.PORT, db=RedisConfig.DB, decode_responses=True) as client:
            await client.hset(uid, mapping={
                
            })

    @classmethod      
    async def get_setting(cls, uid: str, name: str) -> Optional[int | list[int] | None]:
        '''The method gets specific settings value from the specific user.\n

           Parameters
           -----------
           uid : `str`, required (unique account identifier)\n
           name : `str`, required (key)

           Returns
           -----------
           `Optional[int | list[int] | None]`
        '''
        async with aioredis.Redis(host=RedisConfig.HOST, port=RedisConfig.PORT, db=RedisConfig.DB, decode_responses=True) as client:
            result = await client.hget(uid, name)
            return result


    @classmethod        
    async def get_settings(cls, uid: str) -> dict[str, Union[int, list[int]]]:
        '''The method gets all settings from the specific user.\n

           Parameters
           -----------
           uid : `str`, required (unique account identifier)
        '''
        async with aioredis.Redis(host=RedisConfig.HOST, port=RedisConfig.PORT, db=RedisConfig.DB, decode_responses=True) as client:
            result = await client.hgetall(uid)
            return result
        

    @classmethod
    async def _set_setting(cls, uid: str, name: str, value: Any) -> None:
        '''The method updates specific settings value from the specific user.\n
           NOTE: this method is protected!

           Parameters
           -----------
           uid   : `str`, required (unique account identifier)\n
           name  : `str`, required (key to access settings attr)\n
           value : `Any`, required (new value for the key)

           Returns
           -----------
           `None`
        '''
        async with aioredis.Redis(host=RedisConfig.HOST, port=RedisConfig.PORT, db=RedisConfig.DB, decode_responses=True) as client:
            await client.hset(uid, mapping={name : value})


    @classmethod        
    async def update_settings(cls, uid: str, settings: dict[str, Union[int, list[int], None]]) -> None:
        '''The method updates specific settings value from the specific user.\n

           Parameters
           -----------
           uid      : `str`, required (unique account identifier)\n
           settings : `dict[str, Union[int, list[int], None]]`, required (new settings mapping)

           Returns
           -----------
           `None`
        '''
        for key, value in settings.items():
            if value is not None and key in RedisConfig.ATTRS: # We are not updating settings if value is None since it will ruin deal creation & if the key is not in the list
                await cls._set_setting(uid, key, value) # Calling protected method