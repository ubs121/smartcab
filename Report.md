# SmartCab project report

## Implement a Basic Driving Agent


**QUESTION**: Observe what you see with the agent's behavior as it takes random actions. Does the smartcab eventually make it to the destination? Are there any other interesting observations to note?

**ANSWER**:  It seems, the agent could not reach to the given destination within a deadline by taking random actions. But rarely, it could. As observed, it could reach the destination usually at the beginning of simulation.

The reward was between -1.0 and 2.0, it's like
* 0.0 reward for the 'None' action,
* 2.0 reward for valid move etc.

The smartcab was jumping from one edge to another, it was very annoying and weird.

The traffic light stays about 3 seconds (updates) at one state.

## Inform the Driving Agent

**QUESTION**: What states have you identified that are appropriate for modeling the smartcab and environment? Why do you believe each of these states to be appropriate for this problem?

**ANSWER**:

This is a navigation problem with a deadline. The mission is to reach a given destination with a given time in a given environment (grid space).

The current location of the agent is the most important metric to complete the task. But in this problem the agent doesn't know it's location and destination. So the agent should follow the waypoint, it may waste time if goes in other direction.

So I think, the following states are appropriate (ordered by importance):

* `Next waypoint` - The next waypoint location relative to its current location and heading. Since current location and distance are unknown for the agent, the waypoint should be the most important information to navigate in the environment. Just by following the 'next_waypoint', the agent could reach the destination successfully, except traffic light rule.

* `Deadline` -  The current time left from the allotted deadline. The agent has to select a correct action according to deadline. It represents how many moves the agent has left, at maximum. The deadline must be enough for the task, otherwise it would be a mission impossible. So we may skip this information and follow the shortest path policy.

* `Light` - traffic lights: red, green

* `Oncoming cars` - oncoming vehicles from other directions


**OPTIONAL**: How many states in total exist for the smartcab in this environment? Does this number seem reasonable given that the goal of Q-Learning is to learn and make informed decisions about each state? Why or why not?

**ANSWER**:  

I think, 'Next waypoint' and 'Deadline' states are important for this task. But, we could ignore 'Deadline' state, because we could maintain it by policy.

We need to keep state combinations as few as possible, because many states (many combinations) will take longer time to "learn".

## Implement a Q-Learning Driving Agent

**QUESTION**: What changes do you notice in the agent's behavior when compared to the basic driving agent when random actions were always taken? Why is this behavior occurring?

Success rate is increased. Because it's learning from the past history.


## Improve the Q-Learning Driving Agent


**QUESTION**: Report the different values for the parameters tuned in your basic implementation of Q-Learning. For which set of parameters does the agent perform best? How well does the final driving agent perform?

**ANSWER**

Gamma, epsilon ?

Цаг хугацааны хувьд ?
Зөв замаа олох тухайд ?


**QUESTION**: Does your agent get close to finding an optimal policy, i.e. reach the destination in the minimum possible time, and not incur any penalties? How would you describe an optimal policy for this problem?

**ANSWER**

Optimal policy is:

1. obey traffic rule
2. follow the waypoint, it will be a guiding path to the destination
3. minimize travel time (to maintain the deadline)
  * to follow the waypoint,  same time increase exploration to seek a better route
  * to avoid U turns, don't go to the opposite direction of the waypoint
  * to avoid circling in one place !!!
