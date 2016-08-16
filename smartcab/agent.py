#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import numpy as np
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # TODO: Initialize any additional variables here
        self.epsilon = 0.1 # randomness or exploration
        self.alpha = 0.5 # learning rate
        self.gamma = 0.9
        self.q = {} # RESET ?
        self.actions = [None, 'forward', 'left', 'right']


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.state = ''
        self.last_state = ''
        self.last_action = ' '
        self.last_waypoint = ' '


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: update state (last 2 waypoint and 1 action)
        self.state = "{}{}{}".format(self.last_waypoint[0],
            self.last_action[0] if self.last_action else ' ',
            self.next_waypoint[0])

        # TODO: Select action according to your policy
        action = self.choose_action(inputs)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        self.learn(self.last_state, self.last_action, reward, self.state)

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

        # remember values
        self.last_state = self.state
        self.last_waypoint = self.next_waypoint
        self.last_action = action


        # print self.q

    def learn(self, state, action, reward, state2):
        oldv = self.q.get((state, action), 0.0)
        maxqnew = max([self.q.get((state2, a), 0.0) for a in self.actions])
        self.q[(state, action)] = oldv + self.alpha * (reward + self.gamma*maxqnew - oldv)

    def choose_action(self, inputs):
        if random.random() < self.epsilon:
            action = random.choice(self.actions) #self.next_waypoint
        else:
            ql = [self.q.get((self.state, a), 0.0) for a in self.actions]
            maxQ = max(ql)
            best = [i for i in range(len(self.actions)) if ql[i] == maxQ]
            i = random.choice(best)
            action = self.actions[i]

        # Policy1: Follow traffic rule
        action_okay = True
        if action == 'right':
            if inputs['light'] == 'red' and inputs['left'] == 'forward':
                action_okay = False
        elif action == 'forward':
            if inputs['light'] == 'red':
                action_okay = False
        elif action == 'left':
            if inputs['light'] == 'red' or (inputs['oncoming'] == 'forward' or inputs['oncoming'] == 'right'):
                action_okay = False

        if not action_okay:
            action = None

        return action

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
