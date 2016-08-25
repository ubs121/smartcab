#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import numpy as np
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

# alpha - learning rate, as suggested for stochastic problem
# gamma - discount, the importance of future rewards
options = {'alpha': 0.1, 'gamma': 0.5}

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    actions = [None, 'forward', 'left', 'right']

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # TODO: Initialize any additional variables here
        self.alpha = options['alpha']
        self.gamma = options['gamma']
        self.mem = {} # learning memory

        self.success = 0

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
        self.state = (self.next_waypoint, inputs['light'], inputs['oncoming'], inputs['left'], inputs['right'])

        # Select action according to your policy
        action = self.choose_action(inputs)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # Learn policy based on last state, action, reward
        self.learn(self.last_state, self.last_action, self.last_reward, self.state)

        #print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

        # remember last state
        self.last_state = self.state
        self.last_waypoint = self.state
        self.last_action = action
        self.last_reward = reward

        # measure performance
        self.measure_results()

    def choose_action(self, inputs):
        # assume Q = 0.0 for unknown state-action, it's preferred over a failed state-action
        sa_Q_values = [self.mem.get((self.state, a), 0.0) for a in self.actions]
        sa_max = max(sa_Q_values)

        # add some exploration among the max actions
        sa_max_indexes = [i for i in range(len(self.actions)) if sa_Q_values[i] == sa_max]
        i = random.choice(sa_max_indexes)

        # TODO: do some exploration to avoid frequent waits ('None' actions)

        return self.actions[i] # random action with max value

    def learn(self, state1, action1, reward1, state2):
        if state1 == None:
            # no previuos state
            return

        # Adapted from: https://studywolf.wordpress.com/2012/11/25/reinforcement-learning-q-learning-and-exploration/)
        # Reference from Udacity Machine Learning Course. https://classroom.udacity.com/nanodegrees/nd009/parts/0091345409/modules/e64f9a65-fdb5-4e60-81a9-72813beebb7e/lessons/5446820041/concepts/6348990570923
        sa1 = self.mem.get((state1, action1), 0.0)
        sa2_maxQ = max([self.mem.get((state2, a), 0.0) for a in self.actions])

        # Q learning formula: Q(s,a) <- Q(s,a)+alpha[r+ gamma* max Q(s',a')-Q(s,a)]
        self.mem[(state1, action1)] = sa1 + self.alpha * (reward1 + self.gamma*sa2_maxQ - sa1)


    """ ---------- FOR MEASUREMENT PURPOSE ------------ """
    def measure_results(self):
        agentState = self.env.agent_states[self]

        if self.env.done:
            self.success += 1

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    print 'Success trials', a.success
    return a.success

if __name__ == '__main__':
    run()

    # parameter tuning test
    
    # options['alpha'] = 0.1
    # options['gamma'] = 0.1

    # rates = {}
    # for a in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    #     for g in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    #         options['alpha'] = a
    #         options['gamma'] = g
    #         srate = run()
    #         rates[(a,g)] = srate
    #
    # for key in sorted(rates):
    #     print key, ': ', rates[key]
