from .task_def import TaskDef


class ProcessFlow(object):

    def __init__(self):
        pass

    start = (TaskDef[Application][dict]())

    verification = (TaskDef[int][dict]())