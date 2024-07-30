from typing import List, Any
from datetime import datetime
from ninja import Schema
from pydantic import EmailStr

class WaitlistEntryCreateSchema(Schema):
    # create - data
    # waitlistEntryIn
    email: EmailStr
class ErrorWaitlistEntryCreateSchema(Schema):
    # create - data
    # waitlistEntryIn
    email: List[Any]
    #non_field_errors: List[dict] = []

class WaitlistEntryListSchema(Schema):
    # List - data
    # waitlistEntryOut
    id: int
    email: EmailStr

class WaitlistEntryDetailSchema(Schema):
    # Get - data
    # waitlistEntryOut
    id: int
    email: EmailStr
    updated: datetime
    timestamp: datetime