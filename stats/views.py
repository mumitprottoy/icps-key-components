from django.shortcuts import render, render
from control.restrictions import profile_pic_required
from control.operations import get_context
from .operations import get_fixture


@profile_pic_required
def list_fixtures(request):
    context = get_context(request)
    context['fixtures']=get_fixture()
    return render(request, 'fixtures.html', context)