#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import sys
sys.dont_write_bytecode = True

from __init__ import Hybrid_Iterator

license = """
Python class for modeling Points of simple graphs.
Copyright (C) 2019  S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class Priority_Buffer(Hybrid_Iterator):
    """
    Priority_Buffer

    ## Arguments

    - `graph`, with `{name: sub_graph}` and `sub_graph[key_name]` to compare
    - `buffer_size`, `int` of desired `{name: sub_graph}` pairs to buffer
    - `priority`, dictionary containing the following data structure
        - `key_name`, withing `graph` to compare with `_bound`s bellow
        - `GE_bound`, buffers those greater than or equal to `graph[key_name]`
        - `LE_bound`, buffers those less than or equal to `graph[key_name]`
    - `step`, dictionary containing the following `{key: value}` pairs
        - `amount`, to increment or decrement `_bound`s to ensure full buffer
        - `GE_min`/`LE_max`, bounds the related `_bounds` above
    - `modifier` if set __must__ accept `{key: value}` pairs from `graph`
    """

    def __init__(self, graph, priority, buffer_size, step, modifier = None, **kwargs):
        super(Priority_Buffer, self).__init__(**kwargs)
        self.update(
            graph = graph,
            priority = priority,
            buffer_size = buffer_size,
            step = step,
            modifier = modifier,
            buffer = {})

    @property
    def is_buffered(self):
        """
        Returns `True` if buffer is satisfied or graph is empty, `False`
        otherwise. Used by `next()` to detect conditions to `return` on.
        """
        if len(self['buffer'].keys()) >= self['buffer_size']:
            return True

        if len(self['graph'].keys()) <= 0:
            return True

        # ... Note `\` ignores new-lines so that
        #     the following compound checks do not
        #     require excessive side-scrolling...
        if self['step'].get('GE_min') is not None:
            if self['priority']['GE_bound'] < self['step']['GE_min']:
                return True
        elif self['step'].get('LE_max') is not None:
            if self['priority']['LE_bound'] > self['step']['LE_max']:
                return True
        else:
            raise ValueError("self['priority'] missing step missing min/max")

        return False

    def top_priority(self, graph = None):
        """
        Yields `dict`s from `graph` where value of `graph[key_name]`,
        as set by `self['priority']['key_name']`, is within range of
        `self['GE_bound']` or `self['LE_bound']`

        - `graph`, dictionary that is __destructively__ read (`pop`ed) from

        > if `graph` is `None` then `top_priority` reads from `self['graph']`
        """
        if graph is None:
            graph = self['graph']

        key_name = self['priority']['key_name']
        for name, node in graph.items():
            # ... Priorities greater or equal to some bound
            if self['priority'].get('GE_bound') is not None:
                if node[key_name] >= self['priority']['GE_bound']:
                    yield {name: graph.pop(name)}
            # ... Priorities less or equal to some bound
            elif self['priority'].get('LE_bound') is not None:
                if node[key_name] <= self['priority']['LE_bound']:
                    yield {name: graph.pop(name)}
            else:
                raise ValueError('Misconfiguration, either `GE_`/`LE_bound`s ')

        self.throw(GeneratorExit)

    def next(self):
        """
        Sets `self['buffer']` from `self.top_priority()` and returns `self`
        """
        if not self['graph']:
            self.throw(GeneratorExit)

        self['buffer'] = {}
        priority_gen = self.top_priority()
        while not self.is_buffered:
            try:
                # ... to get next priority
                next_sub_graph = priority_gen.next()
            except (StopIteration, GeneratorExit):
                # ... that we have run out items within
                #     the current bounds, so _step_ in prep
                #     for next iteration of `while` loop
                if self['priority'].get('GE_bound'):
                    self['priority']['GE_bound'] += self['step']['amount']
                    priority_gen = self.top_priority()
                    # ... Note `priority_gen` re-assignments are
                    #     a good place for future optimization.
                elif self['priority'].get('LE_bound'):
                    self['priority']['LE_bound'] += self['step']['amount']
                    priority_gen = self.top_priority()
                else:
                    raise ValueError("self['priority'] missing bounds")
            else:
                # ... got `next_sub_graph` successfully! So
                try:
                    self['buffer'].update(self['modifier'](next_sub_graph))
                except TypeError:
                    self['buffer'].update(next_sub_graph)
                #     though this is a good spot
                #     for pre-processing too...
            finally:
                # ... check for other ways out of `while`
                #     loop before doing it all again...
                pass

        return self


if __name__ == '__main__':
    """
    The following are run when this file is executed as
    a script, eg. `python priority_buffer.py`
    but not executed when imported as a module, thus a
    good place to put unit tests.
    """
    from random import randint

    print("Initalizing unit test.\n{0}".format("".join(['_' for x in range(9)])))
    graph = {}
    for i in range(0, 21, 1):
        graph.update({
            "sub_graph_{0}".format(i): {
                'points': {},
                'first_to_compute': randint(0, 9),
            }
        })

    print("Sample graph head.\n{0}".format("".join(['_' for x in range(9)])))
    head_counter = 0
    for k, v in graph.items():
        print("{0} -> {1}".format(k, v))
        head_counter += 1
        if head_counter > 3:
            break

    buffer = Priority_Buffer(
        graph = graph,
        priority = {'key_name': 'first_to_compute',
                    'GE_bound': 7},
        step = {'amount': -2,
                'GE_min': -1},
        buffer_size = 5,
    )

    print("Iterating over sample graph.\n{0}".format("".join(['_' for x in range(9)])))
    counter = 0
    c_max = int(len(graph.keys()) / buffer['buffer_size'] + 1)
    # ... (21 / 5) + 1 -> int -> 5
    for chunk in buffer:
        print("Chunk {count} of ~ {max}".format(
            count = counter, max = c_max - 1))

        for key, val in chunk['buffer'].items():
            print("\t{k} -> {v}".format(**{
                'k': key, 'v': val}))

        counter += 1

        if counter > c_max:
            raise Exception("Hunt for bugs!")

    print("Finished first unit tests.\n{0}".format("".join(['_' for x in range(9)])))

    print("Starting second unit tests.\n{0}".format("".join(['_' for x in range(9)])))

    # ... This is just an example function
    #     for use as a `modifier`
    def populate(sub_graph):
        """
        Expects `{'hash': {'key': None}}` structure where `key` needs a population
        """
        key = 'points'
        hash = sub_graph.keys()[0]
        for x in range(randint(2, 5)):
            sub_graph[hash][key].update(
                {
                    "point_{0}".format(x): randint(200, 500),
                }
            )

        return sub_graph

    buffer['modifier'] = populate
    buffer['priority']['GE_bound'] = 7
    print("Re-populating `buffer['graph']`.\n{0}".format("".join(['_' for x in range(9)])))
    for i in range(0, 21, 1):
        buffer['graph'].update({
            "sub_graph_{0}".format(i): {
                'points': {},
                'first_to_compute': randint(0, 9),
            }
        })

    print("Iterating over sample graph while populating sub-graphs.\n{0}".format("".join(['_' for x in range(9)])))
    counter = 0
    c_max = int(len(graph.keys()) / buffer['buffer_size'] + 1)
    # ... (21 / 5) + 1 -> int -> 5
    for chunk in buffer:
        print("Chunk {count} of ~ {max}".format(
            count = counter, max = c_max - 1))

        for key, val in chunk['buffer'].items():
            print("\t{k} -> {v}".format(**{
                'k': key, 'v': val}))

        counter += 1

        if counter > c_max:
            raise Exception("Hunt for bugs!")

    print("Finished second unit tests.\n{0}".format("".join(['_' for x in range(9)])))
