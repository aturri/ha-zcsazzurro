"""Local replacement for flatdict library incompatible with Python 3.13."""

class FlatterDict(dict):
    def __init__(self, value=None, delimiter='.'):
        super().__init__()
        self.delimiter = delimiter
        if value:
            self.update(self._flatten(value))

    def _flatten(self, d, parent_key=''):
        items = []
        for k, v in d.items():
            new_key = parent_key + self.delimiter + k if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)
