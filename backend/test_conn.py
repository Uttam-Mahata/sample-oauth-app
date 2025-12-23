import httpx
import asyncio

async def test_connection():
    url = 'https://accounts.google.com/.well-known/openid-configuration'
    print(f"Testing connection to {url}...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            print(f"Status Code: {response.status_code}")
            print("Connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
