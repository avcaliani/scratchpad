import logging as log
import sys
from functools import wraps
from random import choice
from typing import Any, List

FRUITS = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅']
SPORTS = ['⚽️', '🏀', '🏈', '⚾️', '🎾', '🏐', '🎱']


def debug(func: Any) -> Any:
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.debug(f'-------------< func >--------------')
        log.debug(f'Function ')
        log.debug(f' └── {func.__name__}')
        log.debug(f'Arguments ')
        for arg in args:
            log.debug(f' ├── {arg}')
        log.debug(f' └── The End')
        log.debug(f'K. Arguments ')
        for k, v in kwargs.items():
            log.debug(f' ├── {k}: {v}')
        log.debug(f' └── The End')
        log.debug(f'-------------------------------------')
        return func(*args, **kwargs)

    return wrapper


def repeat(n: int = 4) -> Any:
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.debug(f'Repeating execution {n} times...')
            result = []
            for _ in range(n):
                result.append(func(*args, **kwargs))
            return result

        return wrapper

    return decorator


@debug
def get_emojis(how_many: int, **kwargs) -> List[str]:
    if kwargs.get('section') == 'fruits':
        return FRUITS[0:how_many]
    else:
        return SPORTS[0:how_many]


@debug
@repeat(n=3)
def pick(values: List[str]) -> str:
    return choice(values)


if __name__ == '__main__':
    log.basicConfig(
        format='[%(asctime)s] %(message)s',
        level=log.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout
    )

    emojis = get_emojis(4, section=choice(['sports', 'fruits']))
    log.info(f'Emojis Set: {emojis}')

    picked = pick(emojis)
    log.info(f'Picked Emoji(s): {picked}')
