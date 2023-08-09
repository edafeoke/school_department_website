#!/usr/bin/python3
'''A module containing all function related to the user model'''


from models import storage


def get_all_user():
    """Prints all string representation of all instances based or not on the class name."""

    all_objs = []
    objs = storage.all()
    for v in objs.values():
        if v.__class__.__name__ == "User":
            all_objs.append(v)
    print(all_objs)
    return all_objs
