
from django.contrib.auth.models import Group

def user_groups(user):
    if user.is_master or user.is_admin:
        group = Group.objects.all().values(code=F("groupcustom__code"))
    else:
        group = user.role_group.all().values(code=F("role__groupcustom__code"))
    return group