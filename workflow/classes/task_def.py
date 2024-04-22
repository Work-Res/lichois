from typing import Generic, TypeVar

T = TypeVar('T')
V = TypeVar('V')


class TaskTransaction(Generic[T][V]):
    """
    """

    def __init__(self):
        self.object_data = None
        self.object_rules = None

    def rules(self, rules: V):
        self.object_rules = rules

    def source(self, source: T):
        self.object_data = source

    def predicate(self):
        pass

    def action(self):
        pass

    def done(self):
        pass