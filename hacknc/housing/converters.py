class SlugKeyConverter:
    """
    Path converter for 6 character slug keys.
    """
    regex = '[a-zA-Z0-9]{6}'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
