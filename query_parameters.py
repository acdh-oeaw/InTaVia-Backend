import json
from typing import Any
from fastapi import Query
from pydantic import BaseModel, HttpUrl, NonNegativeInt, PositiveInt
from dateutil.parser import *
import datetime


class QueryBase(BaseModel):
    page: PositiveInt = Query(default=1, gte=1)
    limit: int = Query(default=50, le=1000, gte=1)

    def get_cache_str(self):
        return str(hash(json.dumps(self.dict(exclude={"page", "limit"}), sort_keys=True)))

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)


class Search(QueryBase):
    q: str = Query(default=None,
                   max_length=200,
                   description="Searches across labels of all entity proxies")
    occupation: str = Query(default=None,
    max_length=200,
    description="Searches the labels of the Occupations")
    bornBefore: str|datetime.datetime = Query(default=None, description="Filters for Persons born before a certain date")
    bornAfter: str|datetime.datetime = Query(default=None, description="Filters for Persons born after a certain date")
    diedAfter: str|datetime.datetime = Query(default=None, description="Filters for Persons died after a certain date")
    diedBefore: str|datetime.datetime = Query(default=None, description="Filters for Persons died before a certain date")

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        if data["bornBefore"] is not None:
            __pydantic_self__.__setattr__('bornBefore', parse(data['bornBefore']).strftime('%Y-%m-%dT00:00:00'))
        if data["bornAfter"] is not None:
            __pydantic_self__.__setattr__('bornAfter', parse(data['bornAfter']).strftime('%Y-%m-%dT00:00:00'))
        if data["diedBefore"] is not None:
            __pydantic_self__.__setattr__('diedBefore', parse(data['diedBefore']).strftime('%Y-%m-%dT00:00:00'))
        if data["diedAfter"] is not None:
            __pydantic_self__.__setattr__('diedAfter', parse(data['diedAfter']).strftime('%Y-%m-%dT00:00:00'))
        print('test')