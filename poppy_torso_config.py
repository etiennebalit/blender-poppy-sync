# -*- coding: utf-8 -*-

bone_motor_map = [{
        'bone': ('Spine.Y', 'y'),
        'motor_id': 33,
        'fromMin': -75,
        'fromMax': 75,
        'toMin': 75,
        'toMax': -75
    },


    {
        'bone': ('Bust.XZ', 'x'),
        'motor_id': 34,
        'fromMin': -25,
        'fromMax': 35,
        'toMin': 25,
        'toMax': -35
    }, {
        'bone': ('Bust.XZ', 'z'),
        'motor_id': 35,
        'fromMin': -30,
        'fromMax': 30,
        'toMin': 30,
        'toMax': -30
    },


    {
        'bone': ('Head.Pan', 'y'),
        'motor_id': 36,
        'fromMin': -75,
        'fromMax': 75,
        'toMin': -75,
        'toMax': 75
    }, {
        'bone': ('Head.Tilt', 'x'),
        'motor_id': 37,
        'fromMin': -30,
        'fromMax': 30,
        'toMin': 30,
        'toMax': -30
    },


    {
        'bone': ('Left.Shoulder.Y', 'y'),
        'motor_id': 41,
        'fromMin': -180,
        'fromMax': 0,
        'toMin': -90,
        'toMax': 90
    }, {
        'bone': ('Left.Shoulder.X', 'x'),
        'motor_id': 42,
        'fromMin': 0,
        'fromMax': 180,
        'toMin': 90,
        'toMax': -90
    }, {
        'bone': ('Left.Arm.Y', 'y'),
        'motor_id': 43,
        'fromMin': -100,
        'fromMax': 100,
        'toMin': -100,
        'toMax': 100
    }, {
        'bone': ('Left.Elbow.Z', 'z'),
        'motor_id': 44,
        'fromMin': -120,
        'fromMax': 0,
        'toMin': -120,
        'toMax': 0
    },


    {
        'bone': ('Right.Shoulder.Y', 'y'),
        'motor_id': 51,
        'fromMin': 0,
        'fromMax': 180,
        'toMin': -90,
        'toMax': 90
    }, {
        'bone': ('Right.Shoulder.X', 'x'),
        'motor_id': 52,
        'fromMin': 0,
        'fromMax': 180,
        'toMin': -90,
        'toMax': 90
    }, {
        'bone': ('Right.Arm.Y', 'y'),
        'motor_id': 53,
        'fromMin': -100,
        'fromMax': 100,
        'toMin': -100,
        'toMax': 100
    }, {
        'bone': ('Right.Elbow.Z', 'z'),
        'motor_id': 54,
        'fromMin': 0,
        'fromMax': 120,
        'toMin': 0,
        'toMax': 120
    },
]


bone_by_motor_id = { joint['motor_id'] : joint['bone'] for joint in bone_motor_map }

config_by_motor = { joint['motor_id'] :
                        {'fromMin': joint['fromMin'],
                        'fromMax':  joint['fromMax'],
                        'toMin':    joint['toMin'],
                        'toMax':    joint['toMax'] }
                                for joint in bone_motor_map }
