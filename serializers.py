from models import User


def user_serializer(users, is_list=True):
    if is_list:
        data = []
        for user in users:
            data.append({
                "name": user.get_name(),
                "email": user.get_email(),
                "password": user.get_password(),
                "code": 200
            })
        return data
    else:
        return {
            "name": users.get_name(),
            "email": users.get_email(),
            "password": users.get_password(),
            "code": 200
        }
