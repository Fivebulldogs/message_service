import copy
from ninja import NinjaAPI, Query
from typing import List
from appmessages.models import Message
from appmessages.schemas import (
    DeleteResultSchema,
    ErrorSchema,
    MessageDeleteSchema,
    MessageInSchema,
    MessageOutSchema,
)

api = NinjaAPI()


@api.get("/messages/new", response=List[MessageOutSchema])
def fetch_new_messages(request):
    query = Message.objects.filter(is_new=True)

    # we must shallow copy the queryset or we lose it when running the update
    query_copy = copy.copy(query)

    # set the messages as not new anymore
    query.update(is_new=False)

    # return the copy (that is unchanged by the update)
    return query_copy


@api.get("/messages", response=List[MessageOutSchema])
def fetch_all_messages(request, start: int = None, stop: int = None):
    query = Message.objects.all()

    if start is None:
        start = 0

    if stop is None:
        stop = query.count()

    indexed_query = query[start:stop]

    # we must shallow copy the queryset to still show in result which messages are new
    indexed_query_copy = copy.copy(indexed_query)

    # cannot update a sliced queryset, so need to do new query go by the id:s
    query.filter(pk__in=indexed_query.values_list("id", flat=True)).update(is_new=False)

    # return the copy (that is unchanged by the update)
    return indexed_query_copy


@api.post("/messages", response=MessageOutSchema)
def create_message(request, message: MessageInSchema):
    return Message.objects.create(recipient=message.recipient, text=message.text)


@api.delete("/messages", response={200: DeleteResultSchema, 400: ErrorSchema})
def delete_messages(
    request,
    params: MessageDeleteSchema = Query(...),
):
    if params.id is None:
        return (400, {"reason": "No message ids specified."})
    (delete_count, _) = Message.objects.filter(id__in=params.id).delete()

    return (200, {"delete_count": delete_count})
