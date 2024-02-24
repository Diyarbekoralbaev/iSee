import aiohttp

import json

with open ('key.txt', 'r') as f:
    API_KEY = f.read()

async def send_request(text):
    url = 'https://mohir.ai/api/v1/tts'
    headers = {
        'Authorization': f"{API_KEY}",  # Replace [API_KEY] with your actual API key
        'Content-Type': 'application/json',
    }
    data = {
        "text": text,
        "model": "davron",
        "mood": "neutral",
        "blocking": "true",
        "webhook_notifaication_url": "https://example.com/webhook",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data)) as response:
            response_data = await response.text()
            print(response_data)


async def main():
    text = "Hello, how are you?"
    await send_request(text)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())