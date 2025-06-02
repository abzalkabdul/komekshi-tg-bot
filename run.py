import asyncio
import aiogram
from aiogram import Bot, Dispatcher

bot = Bot('8037509589:AAFYpACnb_rYTExhmTtUTew1Q391IQfd6Nk')
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main()) 