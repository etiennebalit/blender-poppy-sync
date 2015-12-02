# -*- coding: utf-8 -*-

import bpy
from math import degrees

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'virtualenv/lib/python3.4/site-packages'))
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import traceback
import time

from multiprocessing import Process

from zmq_custom_utils import *
from zmq.utils import jsonapi as json

import pypot.dynamixel
from poppy_torso_config import *


def rotation(armature, bone_name, axis):
    try:
        bone = armature.data.bones[bone_name]
        posebone = armature.pose.bones[bone_name]

        if bone.parent is not None:
            parent_rest = bone.parent.matrix_local.to_quaternion()
            bone_rest = bone.matrix_local.to_quaternion()
            angle_rest = bone_rest.rotation_difference(parent_rest)

            parent_pose = posebone.parent.matrix.to_quaternion()
            bone_pose = posebone.matrix.to_quaternion()
            angle_pose = bone_pose.rotation_difference(parent_pose)
        else:
            angle_rest = bone.matrix_local.to_quaternion()
            angle_pose = posebone.matrix.to_quaternion()

        angle = angle_pose.rotation_difference(angle_rest).to_euler()

        if axis == 'x':
            return degrees(angle.x)
        elif axis == 'y':
            return degrees(angle.y)
        elif axis == 'z':
            return degrees(angle.z)
    except:
        print('Error : ', bone_name)
        return 0

def mapInterval(value, fromMin, fromMax, toMin, toMax):
    value = max(fromMin, value)
    value = min(fromMax, value)

    fromSpan = fromMax - fromMin
    toSpan = toMax - toMin

    valueScaled = float(value - fromMin) / float(fromSpan)

    return toMin + (valueScaled * toSpan)

class Synchronizer:
    def __init__(self):
        context = ZMQLocalContext()
        self.output_ipc_filename = 'output.ipc'

        self.output_socket = context.publisher(filename=self.output_ipc_filename)
        self.process = Process(target=self.sync_loop, args=(self.output_ipc_filename,))
        self.process.start()

        self.armature = bpy.data.objects['Armature']

        self.reset_event_handler('scene_update_post', self.send_motor_positions)

        print('Synchronizer initialized.')

    def stop(self):
        self.process.terminate()
        self.clean_event_handler('scene_update_post')

        try:
            os.remove(self.output_ipc_filename)
        except OSError:
            pass

        print("Synchronizer stopped.")

    def send_motor_positions(self, context):
        if bpy.data.objects.is_updated:
            message = { motor_id: rotation(self.armature, *bone)
                        for motor_id, bone in bone_by_motor_id.items() }
            self.output_socket.send_json(message)

    def sync_loop(self, ipc_filename):
        context = ZMQLocalContext()
        socket = context.lazy_subscriber(filename=ipc_filename)

        ports = pypot.dynamixel.get_available_ports()

        if not ports:
            raise IOError('No port found!')

        print('Ports found:', ports)
        print('Connecting on the first available port:', ports[0])

        with pypot.dynamixel.DxlIO(ports[0]) as io:
            ids = io.scan([ id for id in config_by_motor.keys() ])

            io.set_moving_speed({ id: 100 for id in ids })
            io.set_torque_limit({ id: 1000 for id in ids })
            io.set_max_torque({ id: 1000 for id in ids })

            rest_pos = { id: 0 for id in ids }
            rest_pos[41] = 90
            rest_pos[42] = 90
            rest_pos[51] = -90
            rest_pos[52] = -90
            io.set_goal_position(rest_pos)

            time.sleep(2) # wait 2 second before starting the sync loop

            print("Sync loop started.")

            consecutive_errors = 0
            while True:
                try:
                    data = json.loads(socket.recv(flags = zmq.NOBLOCK))
                    consecutive_errors = 0

                    io.set_goal_position( { int(id) : mapInterval(angle, **config_by_motor[int(id)])
                                                for id, angle in data.items() } )

                except zmq.ZMQError:
                    consecutive_errors += 1
                    if consecutive_errors > 10000:
                        socket.close()
                        socket = context.lazy_subscriber(filename=ipc_filename)
                        consecutive_errors = 0

                except KeyboardInterrupt:
                    socket.close()
                    sys.exit()

    def clean_event_handler(self, event_name):
        event_handlers = getattr(bpy.app.handlers, event_name)
        for i in range( len( event_handlers ) ):
            event_handlers.pop()

    def reset_event_handler(self, event_name, handler):
        self.clean_event_handler(event_name)
        event_handlers = getattr(bpy.app.handlers, event_name)
        event_handlers.append(handler)

###############################################################################

bl_info = {
    "name": "Start/Stop Synchronizer",
    "category": "Object",
}

class StartSynchronizer(bpy.types.Operator):
    """Start Synchronizer"""
    bl_idname = "object.start_synchronizer"
    bl_label = "Start Synchronizer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global synchronizer
        synchronizer = Synchronizer()
        return {'FINISHED'}

class StopSynchronizer(bpy.types.Operator):
    """Stop Synchronizer"""
    bl_idname = "object.stop_synchronizer"
    bl_label = "Stop Synchronizer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global synchronizer
        if synchronizer:
            synchronizer.stop()
        return {'FINISHED'}

def register():
    bpy.utils.register_class(StartSynchronizer)
    bpy.utils.register_class(StopSynchronizer)

def unregister():
    bpy.utils.unregister_class(StartSynchronizer)
    bpy.utils.unregister_class(StopSynchronizer)

if __name__ == "__main__":
    register()
