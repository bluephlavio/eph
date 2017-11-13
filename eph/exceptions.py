"""Defines eph package related exceptions.

"""


class EphError(Exception):
    pass


class InvalidTargetClassError(EphError):
    """An :class:`InvalidTargetClassError` is raised when has been requested to parse a Jpl Response to an unknwon class.

    """
    pass
