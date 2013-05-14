"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

Callbacks to manage the engine when a new file is loaded in tank.

"""
import os
import textwrap
import nuke
import tank
import sys
import traceback
from tank_vendor import yaml

from .menu_generation import MenuGenerator


def __tank_startup_node_callback():    
    """
    Callback that fires every time a node gets created.
    
    Carefully manage exceptions here so that a bug in Tank never
    interrupts the normal workflows in Nuke.    
    """    
    try:
        # look for the root node - this is created only when a new or existing file is opened.
        tn = nuke.thisNode()
        if tn != nuke.root():
            return
            
        if tank.platform.current_engine():
            # already an engine running. Exit early
            return
            
        # try to set up tank!
        engine_name = os.environ.get("TANK_NUKE_ENGINE_INIT_NAME")
        ctx_str = os.environ.get("TANK_NUKE_ENGINE_INIT_CONTEXT")
        context = tank.context.deserialize(ctx_str)        
        tank.platform.start_engine(engine_name, context.tank, context)
    
    except Exception, e:
        nuke.error("Error starting Tank: %s" % e)
        
        
        
g_tank_callbacks_registered = False

def tank_ensure_callbacks_registered():   
    """
    Make sure that we have callbacks tracking context state changes.
    """
    global g_tank_callbacks_registered
    if not g_tank_callbacks_registered:
        nuke.addOnCreate(__tank_startup_node_callback)
        g_tank_callbacks_registered = True

