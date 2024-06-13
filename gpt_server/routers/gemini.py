from typing import Any
from datetime import datetime, timedelta
import json
from functools import wraps
import os

from fastapi import APIRouter, Request
from pydantic_settings import BaseSettings
from sse_starlette import EventSourceResponse
import aiohttp
from redis.asyncio import Redis

from gpt_server.schemas.prompt import Prompt

router = APIRouter()

api_key = os.environ['GEMINI_KEY']

API_URL = f"{os.environ['GEMINI_URL']}?alt=sse&key={api_key}"
API_URL_PRO = f"{os.environ['GEMINI_PRO_URL']}?alt=sse&key={api_key}"

PROXY = os.environ['proxy'] if 'proxy' in os.environ else None


class Settings(BaseSettings):
    redis_host: str = os.environ['REDIS_HOST']
    redis_port: int = int(os.environ['REDIS_PORT'])
    redis_password: str = os.environ['REDIS_PASSWORD']
    rate_limit_per_minute: int = 2


settings = Settings()

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    db=0,
    decode_responses=True,
)


async def rate_limit(rate_limit: int) -> bool:
    """
    Apply rate limiting per minute
    """
    now = datetime.now()
    current_minute = now.strftime("%Y-%m-%dT%H:%M")

    redis_key = f"rate_limit_{current_minute}"
    current_count = await redis_client.incr(redis_key)

    if current_count == 1:
        await redis_client.expireat(name=redis_key,
                                    when=now + timedelta(minutes=1))
    if current_count > rate_limit:
        return False
    return True


def handle_request(prompt: Prompt, model: str, url: str):
    contents: list[Any] = []
    sys_message = None
    less_messages = []
    if len(prompt.messages) > 4:
        less_messages = [prompt.messages[0]] + prompt.messages[-3:]
    else:
        less_messages = prompt.messages
    for message in less_messages:
        single_message: dict[str, Any] = {}
        if message.role == "system":
            sys_message = message.content.replace("GitHub Copilot", "Gemini")
            continue
        elif message.role == "assistant":
            single_message["role"] = "model"
            single_message["parts"] = [{"text": message.content}]
        else:
            single_message["role"] = message.role
            if sys_message is not None:
                text = sys_message + " " + message.content
                sys_message = None
            else:
                text = message.content
            single_message["parts"] = [{"text": text}]
        contents.append(single_message)
    return EventSourceResponse(
        get_content({
            "contents": contents,
            "model": model
        }, url))


def check_limit(func):

    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        is_allowed = await rate_limit(settings.rate_limit_per_minute)
        if is_allowed:
            return await chat_pro(request, *args, **kwargs)
        return await func(request, *args, **kwargs)

    return wrapper


async def get_content(data, url):
    async with aiohttp.ClientSession() as sess:
        async with sess.post(url, json=data, proxy=PROXY) as res:
            async for chunk in res.content:
                _data = chunk.decode("utf-8")
                if _data.strip() != "":
                    try:
                        data = json.loads(_data[6:])
                        send_data = dict(choices=[{
                            "index": 0,
                            "delta": {
                                "content":
                                data["candidates"][0]["content"]["parts"][0]
                                ["text"]
                            }
                        }])
                        yield json.dumps(send_data)
                    except Exception:
                        yield '{"choices":[{"index":0,"delta":{"content":"error from gemini"}}]}'
                        break
            yield "[DONE]"


@router.post("/chat", status_code=200)
@check_limit
async def chat(request: Request, prompt: Prompt):
    return handle_request(prompt, "models/gemini-1.5-flash", API_URL)


async def chat_pro(request: Request, prompt: Prompt):
    return handle_request(prompt, "models/gemini-1.5-pro", API_URL_PRO)
