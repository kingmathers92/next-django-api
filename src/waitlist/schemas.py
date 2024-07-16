from datetime import datetime
from ninja import Schema
from pydantic import EmailStr

class WaitlistEntryCreateSchema(Schema):
    # create - data
    # waitlistEntryIn
    email: EmailStr

class WaitlistEntryDetailSchema(Schema):
    # Get - data
    # waitlistEntryOut
    email: EmailStr
    timestamp: datetime