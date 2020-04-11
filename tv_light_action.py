#!/usr/bin/env python3

import aiohttp
import asyncio
import pysmartthings
import requests
import config

async def main():
    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, config.token)
        devices = await api.devices()
        for device in devices:
            print(device.name)
            await device.status.refresh()
            if(device.status.switch):
                resp = requests.post(
                    url = config.light_url,
                    json = { "ids": config.light_ids}
                )


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
