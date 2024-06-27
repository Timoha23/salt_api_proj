import random


def run(start, end):
    if not (isinstance(start, int) and isinstance(end, int)):
        raise Exception(
            f'One or more args is not instnace int.\nStart: {start}, type: {type(start)}\nEnd: {end}, type: {type(end)}'
        )
    return random.randint(int(start), int(end))
