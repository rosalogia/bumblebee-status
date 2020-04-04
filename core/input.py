import uuid
import logging

import core.event

import util.cli

LEFT_MOUSE = 1
MIDDLE_MOUSE = 2
RIGHT_MOUSE = 3
WHEEL_UP = 4
WHEEL_DOWN = 5

def button_name(button):
    if button == LEFT_MOUSE: return 'left-mouse'
    if button == RIGHT_MOUSE: return 'right-mouse'
    if button == MIDDLE_MOUSE: return 'middle-mouse'
    if button == WHEEL_UP: return 'wheel-up'
    if button == WHEEL_DOWN: return 'wheel-down'
    return 'n/a'

class Object(object):
    def __init__(self):
        super(Object, self).__init__()
        self.id = str(uuid.uuid4())

def __event_id(obj_id, button):
    return '{}::{}'.format(obj_id, button_name(button))

def __execute(cmd):
    try:
        util.cli.execute(cmd, wait=False)
    except Exception as e:
        logging.error('failed to invoke callback: {}'.format(e))

def register(obj, button=None, cmd=None):
    event_id = __event_id(obj.id, button)
    logging.debug('registering callback {}'.format(event_id))
    if callable(cmd):
        core.event.register(event_id, cmd)
    else:
        core.event.register(event_id, lambda _: __execute(cmd))

def trigger(event):
    if not 'button' in event: return
    for field in ['instance', 'name']:
        if not field in event: continue
        core.event.trigger(__event_id(event[field], event['button']), event)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
