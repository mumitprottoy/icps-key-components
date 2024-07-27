from django.contrib.auth.models import User
from .models import ActivationLink


def check_username(username):
    return {
        True: (False, 'Username already exists'),
        False: (True, ''),
    }[User.objects.filter(username=username).exists()]



def check_email(email):
    return {
        True: (False, 'Email already exists'),
        False: (True, ''),
    }[User.objects.filter(email=email.lower()).exists()]



def check_password(password, confirm_password):
    if len(password)<8: return False, 'Password too small.'
    if password!=confirm_password: return False, 'Passwords do not match.'
    return True, ''



def run_signup_checks(data):
    if not check_username(data['username'])[0]:
        return check_username(data['username'])
    if not check_email(data['email'])[0]:
        return check_email(data['email'])
    if not check_password(data['password'], data['confirm_password'])[0]:
        return check_password(data['password'], data['confirm_password'])
    return True, ''


def capitalize_name(name):
    parts=[]
    for p in name.split():
        parts.append(p.capitalize())
    
    return ' '.join(parts).strip()

def get_savable_data(data):
    data = dict(data)
    d = dict()
    for key in data.keys():
        if key not in ['csrfmiddlewaretoken', 'confirm_password']:
            d[key] = data[key][0]
    
    d['first_name']=capitalize_name(d['first_name'])
    d['last_name']=capitalize_name(d['last_name'])
    d['email'] = d['email'].lower()
    return d


def send_activation_link(user, link_head='https://icps7.xyz/activate/', email_type='activation'):
    from icps_email.email_lib import send_template_email
    context = dict()
    context['username']=user.username
    activation = ActivationLink.objects.get(user=user)
    context['link']=link_head+activation.link
    send_template_email(email_type=email_type, email=user.email, context=context)




def create_user(data, activate=True):
    if not run_signup_checks(data)[0]: return run_signup_checks(data)
    data = get_savable_data(data)
    if len(data['username'].split())>1: return False, 'Username cannot contain space.'
    new_user = User.objects.create(**data)
    new_user.set_password(data['password'])
    new_user.is_active=False
    new_user.save()
    post_signups(user=new_user)
    return True, ''



from django.contrib.auth import login, authenticate
def sign_in(request, user, password):
    response = {'logged_in':False}
    if authenticate(username=user.username, password=password):
        if user.is_active:
            login(request, user)
            response['logged_in']=True
            
    return response


def set_new_activation_link(user):
    from icps_lib.uniqueness import unique_key
    ActivationLink(user=user, link=unique_key(69)+user.username).save()


def update_activation_link(act_link_obj):
    from icps_lib.uniqueness import unique_key
    act_link_obj.link = unique_key(69)+act_link_obj.user.username
    act_link_obj.save()
    


def post_signups(user):
    send_activation_link(user)
