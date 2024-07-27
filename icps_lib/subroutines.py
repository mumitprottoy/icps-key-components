
def validate_form_fields(inputs: list, fields:list, csrf: bool=True) -> bool:
    if csrf: fields = ['csrfmiddlewaretoken']+fields
    if not (len(inputs)==len(fields)): return False
    for i in range(len(fields)):
        if inputs[i]!=fields[i]: return False
    
    return True


from django.contrib.auth import login, authenticate
def sign_in(request, user, password):
    response = dict()
    if authenticate(username=user.username, password=password):
        login(request, user)
        response['logged_in']=True
    else: response['logged_in']=False
    return response
