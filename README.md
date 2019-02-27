# hooks
A meta programming experiment for routines that can be outside the standard workflow of a program.

The term is borrowed from emacs and the hooks are in principle similar to emacs's hooks. The longer a python project becomes the more testing is needed. I prefer not to do test drive programming and hooks are an attempt to mitigate that. Functions interacting with a self contained class can declare what they "require" and classes can "provide" certain variables. This will can be checked at program init leading to bugs being identified earlier.

The whole system depends on python's "inspect" module. Much more functionality can be added e.g., 
  - Dependency resolution
  - type validation
  - Hierarchical hooks
  - Generalization to microservices and routines as services

At a broader level this is an attempt to make the routines more independent and verifiable by introducing explicit capabilities and requirements. Of course, it isn't mandatory but in some cases it can be useful.
