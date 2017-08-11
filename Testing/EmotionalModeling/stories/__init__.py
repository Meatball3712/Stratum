# __init__ for stories testing module

stories = {
    "triangles" : "Trangles of Interest"
}

__all__ = stories.keys()

def openStory(title):
    if title in __all__:
        _module = __import__(title)
        _class = getattr(_module, title.upper())
        _instance = _class()
        return _instance