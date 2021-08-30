import aiohttp
import asyncio
from aiohttp import web
import json
import jinja2
import aiohttp_jinja2




@aiohttp_jinja2.template('basic.html')
async def handle_info(req):
    if req.method == 'POST':
        request_data = await req.post()
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as resp:
                data = await resp.json()
                dict_data = {item['ccy']: item for item in data}
                rate = float(dict_data[request_data['select_to']]['buy']) * float(request_data['exchange'])
                return {'rate': rate}
    return None


app = web.Application()
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader("static"))
app.add_routes([
    web.get('/', handle_info),
    web.post('/', handle_info),
])


web.run_app(app)
