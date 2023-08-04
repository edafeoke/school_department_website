#!/usr/bin/python3
'''A module containing all function related to the lecturer model'''


from models import storage
import logging


lecturer_logger = logging.getLogger(__name__)


def get_all_lecturer():
    """Returns all instances of the lecturer model"""

    all_objs = []
    objs = storage.all()
    for v in objs.values():
        if v.__class__.__name__ == "Lecturer":
            # all_objs.append(str(v))
            all_objs.append(v)
    print(all_objs)
    return all_objs
