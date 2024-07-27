from django.shortcuts import render, redirect


def outsiders_only(view):
    
    def check_outsider(request, *args, **kwargs):
        if request.user.is_authenticated:
           return redirect('home')
        else: return view(request, *args, **kwargs)
    
    return check_outsider  
