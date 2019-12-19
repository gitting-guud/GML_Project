#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True
# ... When in production remove or comment above
#     two lines to gain `pyc` _speed boost_.
#     They're there to mitigate thrashing
#     SSD or similar during development process.

from collections import Iterator


class Hybrid_Iterator(dict, Iterator):
    """
    Contains _boilerplate_ and Python 2/3 compatibility for
    making a looping dictionary. Not intended to be used
    directly but instead to reduce redundant repetition.
    """

    def __init__(self, **kwargs):
        super(Hybrid_Iterator, self).__init__(**kwargs)

    def __iter__(self):
        return self

    def throw(self, type = None, traceback = None):
        raise StopIteration

    def next(self):
        """
        Inheriting classes __must__ override this method to activate.

        - Called implicitly via `for` loops but maybe called explicitly.
        - `GeneratorExit`/`StopIteration` are an exit signal for loops.
        """
        self.throw(GeneratorExit)

    __next__ = next


if __name__ == '__main__':
    raise Exception("Hybrid_Iterator import and modify it to iterate dictionaries!")
