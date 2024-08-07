from typing import List
import json
from allauth.account.forms import SignupForm
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.responses import Response
import helpers
from ninja_jwt.authentication import JWTAuth
from .forms import WaitlistCreateForm
from .models import WaitlistEntry
from .schemas import (
    WaitlistEntryCreateSchema,
    WaitlistEntryListSchema,
    WaitlistEntryDetailSchema,
    ErrorWaitlistEntryCreateSchema,
    WaitlistEntryUpdateSchema
)

router = Router()

@router.post("/signup")
def signup(request, email: str, password: str):
    form = SignupForm(data={
        'email': email,
        'password1': password,
        'password2': password,
    })
    if form.is_valid():
        user = form.save(request)
        print(f"User created: {user.email}")  # Debug statement

        # Generate tokens
        auth = JWTAuth()
        access_token = auth.create_access_token(user)
        refresh_token = auth.create_refresh_token(user)

        return {
            'email': user.email,
            'id': user.id,
            'access': access_token,
            'refresh': refresh_token,
        }
    form_errors = json.loads(form.errors.as_json())
    return 400, form_errors

# /api/waitlist
@router.get("", response=List[WaitlistEntryListSchema], auth=helpers.api_auth_user_required)
def list_waitlist_entries(request):
    qs = WaitlistEntry.objects.filter(user=request.user)
    return qs

# /api/waitlist
@router.post("", response={
    201: WaitlistEntryDetailSchema,
    400: ErrorWaitlistEntryCreateSchema

    }, auth=helpers.api_auth_user_or_annon)
def create_waitlist_entry(request, data:WaitlistEntryCreateSchema):
    form = WaitlistCreateForm(data.dict())
    if not form.is_valid():
        #cleaned_data = form.cleaned_data
        #obj =  WaitlistEntry(**cleaned_data.dict())
        form_errors = json.loads(form.errors.as_json())
        return 400, form_errors
    obj = form.save(commit=False)
    if request.user.is_authenticated:
        obj.user = request.user
    obj.save()
    return 201, obj


@router.get("{entry_id}/", response=WaitlistEntryDetailSchema, auth=helpers.api_auth_user_required)
def get_waitlist_entry(request, entry_id:int):
    obj = get_object_or_404(
        WaitlistEntry,
        id=entry_id,
        user=request.user)
    return obj

@router.put("{entry_id}/", response=WaitlistEntryDetailSchema, auth=helpers.api_auth_user_required)
def update_wailist_entry(request, entry_id:int, payload:WaitlistEntryUpdateSchema):
    obj = get_object_or_404(
        WaitlistEntry,
        id=entry_id,
        user=request.user)
    payload_dict = payload.dict()
    for k,v in payload_dict.items():
        setattr(obj, k, v)
    obj.save()
    return obj

# http DELETE
@router.delete("{entry_id}/delete/", response=WaitlistEntryDetailSchema, auth=helpers.api_auth_user_required)
def delete_wailist_entry(request, entry_id:int):
    obj = get_object_or_404(
        WaitlistEntry,
        id=entry_id,
        user=request.user)
    obj.delete()
    return obj

