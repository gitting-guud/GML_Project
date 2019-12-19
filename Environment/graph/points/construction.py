#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
# ... Above _unlocks_ some compatibility _magics_
#     for running within Python 2 or 3

import sys
sys.dont_write_bytecode = True

from __init__ import Point
# ... Import the `Point` class from the
#    `__init__.py` file within the same directory.

license = """
Python class for modeling Construction Points of time based graphs.
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


class Construction(Point):
    """
    Construction aids in modeling costs that rise and fall based on current hour

    ## Arguments

    - `hours` could be a dictionary, eg. `{12: 0.6, 14: 0.8, ...}`
    """

    def __init__(self, hours, current_hour, address, neighbors, **kwargs):
        super(Construction, self).__init__(address = address,
                                           neighbors = neighbors,
                                           **kwargs)
        self.update(hours = hours, current_hour = current_hour)

    def cost_modifier(self, cost):
        """
        Returns cost plus current hour's cost if available
        """
        if self['current_hour'] not in self['hours'].keys():
            return cost

        return cost + self['hours'][self['current_hour']]

    def how_much_to(self, address):
        """
        Returns adjusted cost for given `neighbors` `address` from `cost_modifier`
        """
        base = self['neighbors'][address]
        return self.cost_modifier(cost = base)

    def cheapest(self, routes = {}):
        """
        Returns `dict` of `{address: cost}` adjusted with `how_much_to`
        """
        headings = {}
        for address in super(Construction, self).cheapest(routes).keys():
            headings.update({address: self.how_much_to(address)})

        return headings


if __name__ == '__main__':
    f_line = "".join(['_' for x in range(9)])
    print("Initializing unit test.\n{0}".format(f_line))
    X = 0.2
    O = 0.7

    points = {
        'u': Point(address = 'u', neighbors = {'v': X, 'w': X}),
        'v': Point(address = 'v', neighbors = {'u': O, 'w': X}),
        'w': Point(address = 'w', neighbors = {'u': O, 'v': X}),
    }

    print("Adding exra {0} named points.\n{1}".format('c', f_line))
    points.update({
        'c': Construction(
            address = 'w',
            neighbors = {'v': O, 'w': X},
            current_hour = 6,
            hours = {9: 0.1, 10: 0.3,
                     11: 0.4, 13: 0.6,
                     14: 0.7, 15: 0.85,
                     16: 0.3, 17: 0.2}
            )})

    print("Updating neighbors of {0}.\n{1}".format('c', f_line))
    Z = 0.1
    for address in points['c']['neighbors'].keys():
        points[address]['neighbors'].update({'c': Z})

    print("Dumping named points.\n{0}".format(f_line))
    hours_start = 1
    hours_end = 24
    hours_step = 1
    days = 1

    day_count = 0
    for i in range(hours_start, (hours_end * days) + 1, hours_step):
        for address, point in points.items():
            # ... This `try`/`except` syntax is known as
            #     "asking forgiveness" _dig_ into previous
            #     edits for a "asking permission" version ;-)
            try:
                current_hour = point['current_hour']
            except KeyError:
                current_hour = 'NaN'
            else:
                if current_hour >= hours_end:
                    point['current_hour'] = hours_start
                    day_count += 1
                else:
                    point['current_hour'] += hours_step

            finally:
                cheapest_routs = point.cheapest()
                print("{d} {h} {p} cheapest routes -> {r}".format(
                    d = day_count, h = current_hour,
                    p = address, r = cheapest_routs))

    print("Finished unit tests.\n{0}".format(f_line))
