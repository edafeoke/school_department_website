#!/usr/bin/python3
'''A module containing all function related to the news model'''


from models import storage


def get_all_news():
    """Prints all string representation of all instances based or not on the class name."""

    all_objs = []
    objs = storage.all()
    for v in objs.values():
        if v.__class__.__name__ == "News":
            # all_objs.append(str(v))
            all_objs.append(v)
    print(all_objs)
    return all_objs
