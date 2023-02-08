import jlc


async def get_components(bot):
    async with bot.pool.acquire() as connection:
        async with connection.transaction():
            value = await connection.fetch('SELECT * FROM components', record_class=jlc.JLCRecord)
            return value


async def update_component(bot, new_stock, lcsc):
    async with bot.pool.acquire() as connection:
        async with connection.transaction():
            connection.execute("UPDATE components SET stock = $1 WHERE lcsc = $2", new_stock, lcsc)


async def add_component(bot, name, lcsc, channel):
    async with bot.pool.acquire() as connection:
        async with connection.transaction():
            connection.execute('''INSERT INTO components (name, lcsc, enabled, channel_id, stock, role_id)\
         VALUES ($1, $2, $3, $4, $5, $6''', name, lcsc, True, channel, 1, 0)
