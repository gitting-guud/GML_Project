#!/usr/bin/env python
from __future__ import absolute_import

import sys
sys.dont_write_bytecode = True

from hybrid_iterator import Hybrid_Iterator
from graph.points import Point
from graph.agents import Agent


license = """
Python class for simulating moving agents to points on a graph.
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


class Graph(Hybrid_Iterator):
    """
    Let `agents` be a `dict` with `{'agent_name': 'address'}` key pares
    Let `points` be a `dict` with `{'address': {'neighbors': {'addr': 'cost'}}}`
    """

    def __init__(self, agents, points, **kwargs):
        super(Graph, self).__init__(**kwargs)
        self.update(
            agents = {},
            points = {},
            off_duty = {},
            travel_plans = {})

        for point, neighbors in points.items():
            self.add_point(point, neighbors)

        for name, address in agents.items():
            self.add_agent(name, address)

    def add_agent(self, name, address):
        """
        ## Arguments
        - `address` maybe a `str`ing or instance of `Point`
        - `name` should be a `str`ing

        ## Assigns
        - instance of `Agent` under `self['agents'][name]`
        - reference to `self['points'][address]` under `self['agents'][name]['points']`

        ## Appends `name` to
        - `self['points'][address]['population']`
        """
        if isinstance(address, str):
            address = self['points'][address]

        self['agents'].update({name: Agent(name, address)})
        address['population'].append(name)

    def add_point(self, address, neighbors):
        """
        Adds instance of `Point` under `self['points'][name]`

        ## Arguments
        - `address` should be a `str`ing
        - `neighbors` should be a `{addr: cost}` `dict`ionary
        """
        self['points'].update({address: Point(address, neighbors)})

    def set_travel_plans(self, agents = None):
        """
        Assigns `self['travel_plans']` by calling `next()` on each of `agents`

        Example: `{'Bill': Agent(name='Bill', ...), ...}`, __or__ `{}`

        ## Arguments
        - `agents`; should be a `{key: Agent()}` `dict`ionary

        > `agents` defaults to `self['agents']` if `None` where passed
        """
        self['travel_plans'] = {}
        if not agents:
            agents = self['agents']

        for key, agent in agents.items():
            try:
                self['travel_plans'].update({key: agent.next()})
            except (StopIteration, GeneratorExit):
                # Pop agents that will not move anymore
                print("Moved {name} to off_duty".format(name = agent['name']))
                self['off_duty'].update({key: agents.pop(key)})
                if self['travel_plans'].get(key):
                    self['travel_plans'].pop(key)

        return self['travel_plans']

    def next(self):
        """
        Calls `self.set_travel_plans`, `raise`s `GeneratorExit`
        if out of `agents` or `travel_plans`, otherwise this
        method will _simulate_ moving agents around the graph
        """
        self.set_travel_plans(agents = self['agents'])
        if not self['agents'] or not self['travel_plans']:
            self.throw(GeneratorExit)

        for key, agent in self['travel_plans'].items():
            here = agent['point']['address']
            heading = agent['heading']
            there = heading.keys()[0]
            # ... `heading` ~ `{addr: cost}`

            print("{name} traveling from {here} to {there} paying {cost}".format(
                name = agent['name'], here = here,
                there = there, cost = heading[there]))

            agent['point']['population'].remove(agent['name'])
            agent['visited'].append(heading)

            agent['point'] = self['points'][there]
            agent['point']['population'].append(agent['name'])

        return self


if __name__ == '__main__':
    raise Exception("This file must be used as a module!")
