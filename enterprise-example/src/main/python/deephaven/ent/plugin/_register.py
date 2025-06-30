from deephaven.plugin import Registration, Callback
from deephaven.plugin.utilities import DheSafeCallbackWrapper
from . import IncrementPlugin

class IncrementPluginRegistration(Registration):
    """ Registration for IncrementPlugin. """

    @classmethod
    def register_into(cls, callback: Callback) -> None:
        """ Register the IncrementPlugin. """
        callback = DheSafeCallbackWrapper(callback)
        callback.register(IncrementPlugin)