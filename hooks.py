import inspect


class HookPoint:
    """Simple HookPoint for the Hook protocol. I mean to enhance it with
       dependencies etc. Perhaps also after taking a look at gossip
       implementation in python.

       The Hook communicates with the HookPoint via a provides and
       requires mechanism. I can dependency in this. This simply
       ensures that the variable names (and only names) required by
       the Hook is available with the HookPoint.

       The whole point is that I don't want to expose any more
       variables of a class than necessary to such plugins, and with
       the whole confusion between which variables are available
       w.r.t. class and function local variables, it can be really
       hard to keep track especially for stateful functions.

       The update mechanism updates the local variables accordingly so
       for a loop (which was my primary use case) or any function with
       state specific variables can update the hook and trigger the
       required functions.

       This decouples the hook from the class (state machine) however
       the class still has full flexibility of execution.

    """
    def __init__(self, caller):
        self._caller = caller
        self._attached_hooks = []

    @property
    def attached_hooks(self):
        return self._attached_hooks

    @property
    def provides(self):
        return [x[0] for x in
                inspect.getmembers(self.__class__, lambda o: isinstance(o, property))
                if x[0] != 'provides']

    def insert_hook(self, hook, where):
        assert where in ['a', 'p']
        assert callable(hook)
        if where == 'a':
            self._attached_hooks.append(hook(self))
        elif where == 'p':
            self._attached_hooks.insert(hook(self), 0)

    def append(self, hook):
        self.insert_hook(hook, 'a')

    def prepend(self, hook):
        self.insert_hook(hook, 'p')

    def update(self):
        raise NotImplementedError

    def run_hooks(self):
        for hook in self._attached_hooks:
            hook.run()


class Hook:
    """Simple Hook implementation. Ensures that the parameters required by
       the hook are available in HookPoint.
       Derived classes must implement __call__"""
    def __init__(self, hook_point):
        self.hook_point = hook_point
        self._verify()

    def _verify(self):
        call_signature = inspect.signature(self.__call__).parameters
        self._requirements = [k for k in call_signature.keys()]
        hp_provides = self.hook_point.provides
        if not all([r in hp_provides for r in self._requirements]):
            raise ValueError

    def run(self):
        params = [self.hook_point.__getattribute__(p) for p in self._requirements]
        self.__call__(*params)

    @property
    def requires(self):
        return self._requirements

    # All parameters should be initialized to None
    def __call__(self):
        raise NotImplementedError


# TODO: A workflow agnostic testing framework
# 1. Unittests can be called but they aren't stateful
#
# 2. That is for stateful functions it is difficult to predict
#     which test should be valid according to which state
# 3. The tests should be automatically able to deduce which state
#    it is, simulate the state and execute the required tests
#    according to the state.
# 4. For that the state of the tests should change according to
#    the program execution (without the program actually being executed)
# 5. The state transition function for a test can be made accordingly
