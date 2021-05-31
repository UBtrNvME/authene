import itertools
# from utility.time import monotonic_utc_now
from datetime import datetime

_now = object()


class DomainEvent:
    """A base class for all events in this domain.

    DomainEvents are value objects and all attributes are specified as keyword
    arguments at construction time. There is always a timestamp attribute which
    gives the event creation time in UTC, unless specified.  Events are
    equality comparable.
    """

    def __init__(self, timestamp=_now, **kwargs):
        self.__dict__["timestamp"] = (
            datetime.utcnow() if timestamp is _now else timestamp
        )
        self.__dict__.update(kwargs)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise AttributeError(
                "{} attributes can be added but not modified."
                "Attribute {!r} already exists with value {!r}".format(
                    self.__class__.__name__, key, getattr(self, key)
                )
            )
        self.__dict__[key] = value

    def __eq__(self, rhs):
        if type(self) is not type(rhs):
            return NotImplemented
        return self.__dict__ == rhs.__dict__

    def __ne__(self, rhs):
        return not (self == rhs)

    def __hash__(self):
        return hash(tuple(itertools.chain(self.__dict__.items(), [type(self)])))

    def __repr__(self):
        return (
            self.__class__.__qualname__
            + "("
            + ", ".join("{0}={1!r}".format(*item) for item in self.__dict__.items())
            + ")"
        )


_event_handlers = {}


def subscribe(event_predicate, subscriber):
    """Subscribe to events.

    Args:
        event_predicate: A callable predicate which is used to identify the events to which to subscribe.
        subscriber: A unary callable function which handles the passed event.
    """
    if event_predicate not in _event_handlers:
        _event_handlers[event_predicate] = set()
    _event_handlers[event_predicate].add(subscriber)


def unsubscribe(event_predicate, subscriber):
    """Unsubscribe from events.

    Args:
        event_predicate: The callable predicate which was used to identify the events to which to subscribe.
        subscriber: The subscriber to disconnect.
    """
    if event_predicate in _event_handlers:
        _event_handlers[event_predicate].discard(subscriber)


def unsubscribe_all(subscriber):
    predicates_for_removal = []
    for event_predicate, event_handlers in _event_handlers.items():
        event_handlers.discard(subscriber)
        if len(event_handlers) == 0:
            predicates_for_removal.append(event_predicate)

    for predicate in predicates_for_removal:
        del _event_handlers[predicate]


def publish(event):
    """Send an event to all subscribers.

    Each subscriber will receive each event only once, even if it has been subscribed multiple
    times, possibly with different predicates.

    Args:
        event: The object to be tested against by all registered predicate functions and sent to
            all matching subscribers.
    """
    matching_handlers = set()
    for event_predicate, handlers in _event_handlers.items():
        if event_predicate(event):
            matching_handlers.update(handlers)

    for handler in matching_handlers:
        handler(event)
