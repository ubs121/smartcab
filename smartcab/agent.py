#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import numpy as np
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    actions = [None, 'forward', 'left', 'right']

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # TODO: Initialize any additional variables here
        self.epsilon = 0.7 # epsilon
        self.alpha = 0.5 # learning rate
        self.gamma = 0.9 # discount

        self.k = 0
        self.mem = {} # learning memory
        self.total_reward = 0.0 # total reward for 'mem'
        self.total_time = 0.0 # total spend time for 'mem'

    def reset(self, destination=None):
        self.planner.route_to(destination)

        # Prepare for a new trip
        self.state = '' # reset state

        self.last_action = None
        self.last_state = None
        self.last_reward = None


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # update state
        self.state = (self.last_action, self.next_waypoint)

        # Select action according to your policy
        action = self.choose_action(inputs)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # Learn policy based on last state, action, reward
        self.learn(self.last_state, self.last_action, self.last_reward, self.state)

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

        # next state (kind of hacking?)
        next_state = self.planner.next_waypoint()

        if action:
            self.last_action = action

        self.total_reward += reward
        self.total_time += 1 # every 1 move

        if self.total_time > 0:
            print 'average reward', self.total_reward/ self.total_time

    def choose_action(self, inputs):
        acts = self.actions[:] # all possible actions

        # select greedy action with probability 1−p(k), k is iteration count
        self.k += 1
        self.epsilon = 1.0 - (1000.0/(2000.0 + 10 * self.k)) # k ~ 100 times * 30 * 10 constant
        print 'self.epsilon', self.epsilon

        if random.random() < self.epsilon:
            ql = [self.mem.get((self.state, a), 0.0) for a in acts]
            i = ql.index(max(ql))
            action = acts[i]
        else: # do exploration
            action = random.choice(acts)

        return action

    def learn(self, state1, action1, reward1, state2):
        if state1 == None:
            # no previuos state
            return

        # Q learning formula: Q(s,a) <- Q(s,a)+alpha[r+ gamma* max Q(s',a')-Q(s,a)]

        # Adapted from: https://studywolf.wordpress.com/2012/11/25/reinforcement-learning-q-learning-and-exploration/)
        # Reference from Udacity Machine Learning Course. https://classroom.udacity.com/nanodegrees/nd009/parts/0091345409/modules/e64f9a65-fdb5-4e60-81a9-72813beebb7e/lessons/5446820041/concepts/6348990570923
        sa1 = self.mem.get((state1, action1), 0.0)
        sa`_max2 = max([self.mem.get((state2, a), 0.0) for a in self.actions]) # max Q(s',a'
        self.mem[(state1, action1)] = sa1 + self.alpha * (reward + self.gamma*sa2_max2 - sa1)

        #print self.mem


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.3, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
