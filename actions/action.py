import abc


class AbstractAction(abc.ABC):
    model = None

    def __init__(self, action_name, data):
        self.data = data
        self.action_name = action_name

    def run(self):
        return getattr(self, self.action_name)()

    @abc.abstractmethod
    def create(self):
        raise NotImplementedError

    def update(self):
        instance = self._get_instance()
        instance.update(data=self.data, with_commit=True)

    @abc.abstractmethod
    def _get_instance(self):
        raise NotImplementedError
