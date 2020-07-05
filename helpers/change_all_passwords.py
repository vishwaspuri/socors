from user.models import User


def change_password_for_all_users(password):
    all_users = User.objects.all()
    for u in all_users:
        u.set_password(password)
        u.save()
