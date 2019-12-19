#!/usr/bin/env python
from __future__ import absolute_import

import sys
sys.dont_write_bytecode = True


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


class Point(dict):
    """
    Point is a custom dictionary to aid in modeling
    a graph point and base cost to get to neighbors.

    ## Arguments

    - `address`; unique identifier that can be used as a `key`
    - `neighbors`; `dict` with `{address: cost}` key value pares
      - `cost`; `float` or `int`

    > `address`es are the same regardless of scope
    """

    def __init__(self, address, neighbors = {}, **kwargs):
        super(Point, self).__init__(**kwargs)
        self.update({
            'address': address,
            'neighbors': neighbors,
            'population': []})

    def cheapest(self, routes = {}):
        """
        Returns `dict` with '{address: cost}' key pares

        > `routes` by default will read `self['neighbors']`
        """
        if not routes:
            routes = self['neighbors']

        headings = {}
        for address, cost in routes.items():
            destination = {address: cost}
            if not headings:
                headings = destination
                continue

            cheaper_mask = [cost < x for x in headings.values()]
            equal_mask = [cost == x for x in headings.values()]
            if False not in cheaper_mask:
                headings = destination
            elif True in equal_mask:
                headings.update(destination)

        return headings


if __name__ == '__main__':
    """
    Quick unit tests for when this file is run as a script
    """
    f_line = "".join(['_' for x in range(9)])

    print("Initializing unit test.\n{0}".format(f_line))
    X, Y = (0.2, 0.7)
    points = {
        'u': Point(address = 'u', neighbors = {'v': X, 'w': X}),
        'v': Point(address = 'v', neighbors = {'u': Y, 'w': X}),
        'w': Point(address = 'w', neighbors = {'u': Y, 'v': X}),
    }

    print("Dumping named points.\n{0}".format(f_line))
    for name, point in points.items():
        print("{name} -> {point}".format(name = name, point = point))

    print("Finished unit tests.\n{0}".format(f_line))
