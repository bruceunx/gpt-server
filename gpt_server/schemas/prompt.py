from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class Prompt(BaseModel):
    top_p: int
    n: int
    model: str
    messages: list[Message]
    temperature: float
    intent: bool
    stream: bool
