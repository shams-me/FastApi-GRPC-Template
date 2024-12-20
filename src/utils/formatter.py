class FormatterMap(dict):
    def __missing__(self, key):
        return key
