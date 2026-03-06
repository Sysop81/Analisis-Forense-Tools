class DataInfo:
    
    def __init__(self):
        self._name = None
        self._size = None
        self._content = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    def to_dict(self):
        return {
            "name": self._name,
            "size": self._size,
            "content": self._content
        }    