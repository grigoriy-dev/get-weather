import asyncio, aiohttp
from Tools.utils import round_value, get_wind_direction


async def main():
    temperature = await round_value(value=12.22553)

if __name__ == "__main__":
    asyncio.run(main())
