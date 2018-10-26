#
# For registering event callbacks
#
# Regular example:
#
#     def test_event_action(who, contents, time):
#         engine.message('event callback test {} - {} - {}'.format(who, contents, time))
#     events.register('event_action', test_event_action)
#
# Decorator example:
#
#     @events.event('event_action')
#     def test_event_action(who, contents, time):
#         engine.message('event callback test {} - {} - {}'.format(who, contents, time))
#

_supported_events = [
    'beacon_checkin',
    'beacon_error',
    'beacon_indicator',
    'beacon_initial',
    'beacon_initial_empty',
    'beacon_input',
    'beacon_mode',
    'beacon_output',
    'beacon_output_alt',
    'beacon_output_jobs',
    'beacon_output_ls',
    'beacon_output_ps',
    'beacon_tasked',
    'event_action',
    'event_beacon_initial',
    'event_join',
    'event_newsite',
    'event_notify',
    'event_nouser',
    'event_private',
    'event_public',
    'event_quit',
    'keylogger_hit',
    'profiler_hit',
    'ready',
    'sendmail_done',
    'sendmail_post',
    'sendmail_pre',
    'sendmail_start',
    'ssh_checkin',
    'ssh_error',
    'ssh_indicator',
    'ssh_initial',
    'ssh_input',
    'ssh_output',
    'ssh_output_alt',
    'ssh_tasked',
    'web_hit',
    'any',
    'beacons',
    'heartbeat_10m',
    'heartbeat_10s',
    'heartbeat_15s',
    'heartbeat_1m',
    'heartbeat_1s',
    'heartbeat_20m',
    'heartbeat_30m',
    'heartbeat_30s',
    'heartbeat_5m',
    'heartbeat_5s',
    'heartbeat_60m',
]

import collections

import pycobalt.utils as utils
import pycobalt.engine as engine

# name: [callback1, callback2]
_callbacks = collections.defaultdict(list)

# Call an event callback
def call(name, args):
    global _callbacks
    if name in _callbacks:
        for callback in _callbacks[name]:
            if utils.check_args(callback, args):
                callback(*args)
            else:
                syntax = '{}{}'.format(name, utils.signature(callback))
                engine.error("invalid number of arguments passed to event handler '{}' for event '{}'. syntax: {}".format(callback, name, syntax))
    else:
        engine.debug('no event handles for event: {}'.format(name))

# Register a callback
def register(name, callback):
    global _callbacks
    global _supported_events
    if name not in _supported_events:
        raise RuntimeError('tried to register unsupported event: {}'.format(name))
    _callbacks[name].append(callback)
    engine.event(name)

# Decorator
class event:
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        self.func = func
        register(self.name, self.func)