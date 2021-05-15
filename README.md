# Engine Hearth

All checks in _Engine Heart_ are done with d10 pools. Each d10 in the pool that rolls at or above the **target number** is a **success**. In most circumstances, a check requires a certain number of successes to pass. Any die that rolls a 10 "explodes", adding its success and rolling again. The target number is 8, unless otherwise specified, and may not be lower than 2.

Engine Hearth listens to one channel by name and only responds to messages that begin with a number. This number is interpreted as the pool size for a check. If a target number is specified by `tN`, e.g. `t4`, that target numebr is used.