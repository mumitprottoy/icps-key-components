from django.shortcuts import render
from .restrictions import allow_admins_only, profile_pic_required
from .models import Club
from .operations import get_context


