import asyncio
import aiohttp
import requests

url = "http://127.0.0.1:8000/groq/chat"


async def test_gemini():
    async with aiohttp.ClientSession() as sess:
        async with sess.post(url) as res:
            async for chunk in res.content.iter_chunked(100):
                print(chunk.decode("utf-8"))
                # if chunk:
                #     yield chunk.decode("utf-8")


# async def test_main():
#     async for data in test_gemini():
#         print(data)

asyncio.run(test_gemini())


def test_gemini_sync():
    response = requests.post(url)
    for chunk in response.iter_content(chunk_size=100):
        if chunk:
            data = chunk.decode("utf-8")
            print(data)
