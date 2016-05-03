Droid Blue
===

This project is an experiment to see if it's possible to construct an AI 
capable of playing the X-Wing Miniatures Game at a championship level.
   
   
Design
===

The basic design is to represent game state as a DAG, with each node being a 
snapshot of game state and each edge representing a decision, action or random 
event that changes the state of the game.

`BoardState` is the DAG node class, and is the main hub that the rest of the 
code interacts with.

`ConstantState` is used to hold information that does not change throughout the 
course of the game. Squad lists, point values, etc.

`Edge` subclasses implement the state transitions that actually execute 
gameplay. 

`Rule` subclasses are responsible for producing edges from the current state, 
as well as curating the list of possible edges. For example, a rule could 
provide an edge that removes a focus token and converts eyes to hits. At the 
same time, the rule for Carnor Jax could remove that edge from the list of 
valid options. 

Future scaling
---

The idea is that the final state of flow will be something along the lines of:

- UI layer constructs initial game state, starts main loop
- CPython neural network worker(s) 
    - Evaluate state for likelihood of win
    - Also dial suggestions
- PyPy state space search workers
    - Prune dial search based on NN dial suggestions
    - Alpha-beta search through intra-round choices (actions, targeting, spending tokens)
    - End of round evaluation goes back to CPy NN layer, repeats until target depth reached
    
Current intent is to have each of the three layers above communicate via ZeroMQ 
python bindings. Should make for seamless state transfer, and allow for 
multiple hosts should the need arise.

Performance notes
---

CPython:

Current implementation uses ~10KB of RAM per BoardState instance. 
`copy.deepcopy` can make about 1k copies per second.

PyPy:

Untested. Likely higher RAM usage.

TODO
===

- [ ] overlap detection
- [ ] patrial maneuvers for bumps
- [ ] arc logic
- [ ] rules and edges for combat
- [x] dice pools, rerolls, modifications, etc.
- [ ] niche actions (cloak, slam, etc.)
- [ ] target locks
- [ ] 99% of the upgrades, pilots, etc.
- [ ] other stuff?

Running an example turn
===

    $ python -m droidblue.game

Produces output like the folowing. `FF` means that the edge used was the only 
option at that point in the game (for example, after you reveal a dial, you 
must execute the maneuver, assuming you don't have Advanced Sensors). `Rnd` 
means that edge was chosen randomly from a list of possibilities.


    FF:  <DialsChooseActivePilotEdge object at 0x10b27d7d0 active_id:0, opportunity_list:[(<DialsChooseActivePilotRule object at 0x10b271f10 pilot_id:0, player_id:0, upgrade_id:None>,)], order_tup:(0, 0)>
    Rnd: <SetDialEdge object at 0x10b27dd50 active_id:0, color_int:3, known:False, maneuver_str:'trollL3', opportunity_list:[(<SetDialRule object at 0x10b27d110 pilot_id:0, upgrade_id:None>, 3, 'setDial')], speed_int:3, type_str:'trollL'> 17
    FF:  <DialsChooseActivePilotEdge object at 0x10b27f250 active_id:1, opportunity_list:[(<DialsChooseActivePilotRule object at 0x10b27d350 pilot_id:1, player_id:1, upgrade_id:None>,)], order_tup:(1, 1)>
    Rnd: <SetDialEdge object at 0x10b27f7d0 active_id:1, color_int:1, known:False, maneuver_str:'turnL1', opportunity_list:[(<SetDialRule object at 0x10b27d490 pilot_id:1, upgrade_id:None>, 5, 'setDial')], speed_int:1, type_str:'turnL'> 16
    FF:  <ActivationChooseActivePilotEdge object at 0x10b27f6d0 active_id:0, opportunity_list:[(<ActivationChooseActivePilotRule object at 0x10b271ed0 pilot_id:0, player_id:0, upgrade_id:None>,)], order_tup:(0, 0)>
    FF:  <RevealDialEdge object at 0x10b27ff90 active_id:0, opportunity_list:[(<RevealDialRule object at 0x10b27d150 pilot_id:0, upgrade_id:None>, 7, 'revealDial')]>
    FF:  <PerformManeuverEdge object at 0x10b27ffd0 active_id:0, opportunity_list:[(<PerformManeuverRule object at 0x10b27d190 pilot_id:0, upgrade_id:None>, 7, 'performManeuver')]>
    Rnd: <PerformBoostActionEdge object at 0x10b2814d0 active_id:0, maneuver_str:'bankR1', opportunity_list:[(<PerformBoostActionRule object at 0x10b27d250 pilot_id:0, upgrade_id:None>,), ('performAction', 0, 7, 'performAction')]> 5
    FF:  <ActivationChooseActivePilotEdge object at 0x10b281910 active_id:1, opportunity_list:[(<ActivationChooseActivePilotRule object at 0x10b27d310 pilot_id:1, player_id:1, upgrade_id:None>,)], order_tup:(0, 1)>
    FF:  <RevealDialEdge object at 0x10b281190 active_id:1, opportunity_list:[(<RevealDialRule object at 0x10b27d4d0 pilot_id:1, upgrade_id:None>, 11, 'revealDial')]>
    FF:  <PerformManeuverEdge object at 0x10b281210 active_id:1, opportunity_list:[(<PerformManeuverRule object at 0x10b27d510 pilot_id:1, upgrade_id:None>, 11, 'performManeuver')]>
    Rnd: <PerformBarrelRollActionEdge object at 0x10b281a90 active_id:1, mx:-80.0, my:-20.0, opportunity_list:[(<PerformBarrelRollActionRule object at 0x10b27d590 pilot_id:1, upgrade_id:None>,), ('performAction', 1, 11, 'performAction')]> 12
