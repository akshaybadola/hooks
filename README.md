# hooks

Envisioned while designing a computer vision project this is a a meta
programming experiment for routines that can be outside the standard
workflow of a program. I had thought of this idea for arbitrary
injection of code in existing objects. The point of this whole thing
was to add functionality to a sequential program without breaking its
functionality and also, while making sure that while writing (or
integrating) the function itself some number of checks may be
performed so that the error doesn't occur when it actually is called
two hours down the code.

The term is borrowed from emacs and the hooks are in principle similar
to emacs's hooks. The longer a python class, or a function becomes the
more testing is needed if some new functionality is added. I prefer
not to do test driven programming and hooks are an attempt to mitigate
that. Functions interacting with a self contained class can declare
what they `require` and classes can `provide` certain variables. This
will can be checked at program init leading to bugs being identified
earlier.

# Current implementation

For now a Hook needs a HookPoint object, to which Hooks can be
attached. Each HookPoint maintains a list of attached hooks and a
function `run_hooks()`, runs those functions in sequence.

HookPoint `provides` and Hook `requires` certain variables to be
executed. However, a dependency can be built like packages which can
both have a provide and require attributes which should be resolved
whenever an instance is initialized. Typechecking can also be
implemented at that time but I don't think it's necessary.

The whole system depends on python's "inspect" module. Much more functionality can be added e.g., 
  - Dependency resolution
  - type validation
  - Hierarchical hooks
  - Generalization to microservices and routines as services

At a broader level this is an attempt to make the routines more
independent and verifiable by introducing explicit capabilities and
requirements. Of course, it isn't mandatory but in some cases it can
be useful.

# Why not gossip?

-   [Gossip](https://github.com/getslash/gossip/blob/develop/gossip/hooks.py) has a hooks module. I can take a look at it, but I didn't want to understand the full library as of now.
-   For now I have a simple implementation which fulfils my needs, I
    can compare or integrate with gossip later if required.

# Features to be added in future maybe

## Only one Hook class with provides and requires

-   Instead of a HookPoint providing and a Hook requiring a Hook can
    both provide and require.
-   Still override `__call__` for it to run and check.
-   Can have additional `__attached_hooks__` to call additional functions
-   Of course, everyone should verify that everything works at
    `__init__`


## Dependency resolution

-   Hooks can ultimately ask for symbol names from certain other
    hooks, e.g., `MonkeyPoop.fling_poop` symbol
-   Symbol of course can be a callable or any other type which can be
    checked optionally at `__init__`. A simple function can be added
    that checks if the type has a certain property or
    not. E.g. `iscallable` (can be a check to `__call__` or actually
    `callable(x)`), `isiterable` can (be a check for `__iter__` or
    `iter(x)`.


## Parallel execution.

-   In certain cases the execution of the hook needn't be
    synchronous with the code/type in which it is executing. In
    those circumstances such hooks can be executed via the
    threading or the multiprocessing module.
-   In that case all hooks may have the potential to be
    parallelized but only do so if the environment (HookPoint?)
    says that it is ok to do so.


## Asynchronous signalling

-  `__call__` is simply a signal for a hook to execute. There may be
    asynchronous mechanisms embedded in the hooks which may be
    communicated over an arbitrary protocol.
-   Aside from `__call__` it may also support a `__pause__` or
    `__halt__` signal for a lot more distributed representation.
-   Also variable change at runtime may also be possible with such
    signals.

