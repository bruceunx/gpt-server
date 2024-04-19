from typing import Any
import json

from fastapi import APIRouter, Request
from sse_starlette import EventSourceResponse
import aiohttp

from .._config import APIs

from gpt_server.schemas.prompt import Prompt

router = APIRouter()

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:streamGenerateContent?alt=sse&key={APIs['gemini']}"


async def get_content(data):
    async with aiohttp.ClientSession() as sess:
        async with sess.post(API_URL, json=data, proxy=APIs["proxy"]) as res:
            async for chunk in res.content:
                _data = chunk.decode("utf-8")
                if _data.strip() != "":
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
            yield "[DONE]"


@router.post("/chat", status_code=200)
async def chat(request: Request, prompt: Prompt):
    contents: list[Any] = []
    sys_message = None
    less_messages = []
    if len(prompt.messages) > 4:
        less_messages = [prompt.messages[0]] + prompt.messages[-3:]
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
            # "model": "models/gemini-pro"
        }))
