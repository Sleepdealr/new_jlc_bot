import asyncio
import datetime
import aiohttp
from dataclasses import dataclass
import discord
import database


@dataclass
class Component:
    name: str
    lcsc: str
    enabled: bool
    channel_id: int
    stock: int
    role_id: int = 0


@dataclass
class ComponentData:
    stock: int
    image_url: str
    price: float
    basic: str


async def jlc_stock_routine(client: discord.Client):
    statements = []
    with database.Database() as db:
        for component in db.get_components():
            statements.append(print_stock_data(component, client))
            # await jlc.print_stock_data(component, client)
    await asyncio.gather(*statements)


async def get_jlc_stock(lcsc: str) -> ComponentData:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                "https://jlcpcb.com/api/overseas-smt/web/component/getComponentDetail?componentCode={}".format(
                    lcsc)) as r:
            if r.status == 200:
                response = await r.json()

    jlc_stock = response["data"]["stockCount"]
    image_url = response["data"]["componentImageUrl"] or ""
    price = response["data"]["prices"][0]["productPrice"]
    base = "Basic" if response["data"]["componentLibraryType"] == "base" else "Extended"

    return ComponentData(jlc_stock, image_url, price, base)


async def print_stock_data(component: Component, client: discord.Client):
    data = await get_jlc_stock(component.lcsc)

    stock_delta = component.stock - data.stock
    if stock_delta == 0:
        return
    elif stock_delta > 0:
        indicator = "-"
        color = discord.Color.red()
        # color = discord.Color.from_rgb(000, 256, 000)
    else:
        indicator = "+"
        color = discord.Color.green()
        # color = discord.Color.from_rgb(000, 000, 256)

    embed = discord.Embed(title=component.name, description="Desc", color=color,
                          url="https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt={}".format(
                              component.lcsc))
    embed.set_thumbnail(url=data.image_url)
    embed.timestamp = datetime.datetime.now()
    embed.add_field(name="Stock", value="{} ({}{})".format(data.stock, indicator, abs(stock_delta)),
                    inline=False)
    embed.add_field(name="Previous Stock", value=component.stock, inline=False)
    embed.add_field(name="LCSC Number", value="{}\n{}".format(component.lcsc, data.basic), inline=False)

    channel = client.get_channel(component.channel_id)

    with database.Database() as db:
        db.update_component(data.stock, component.lcsc)

    await channel.send(embed=embed)
