import datetime
from pydantic import Field
from typing import List
from ninja import Schema


class MessageInSchema(Schema):
    recipient: str
    text: str


class MessageOutSchema(Schema):
    id: int
    recipient: str
    text: str
    is_new: bool
    created_at: datetime.datetime


class MessageDeleteSchema(Schema):
    id: List[int] = Field(None)


class DeleteResultSchema(Schema):
    delete_count: str


class ErrorSchema(Schema):
    reason: str
