## *********************************************************
## 
## File autogenerated for the twist_controller package 
## by the dynamic_reconfigure package.
## Please do not edit.
## 
## ********************************************************/

from dynamic_reconfigure.encoding import extract_params

inf = float('inf')

config_description = {'upper': 'DEFAULT', 'lower': 'groups', 'srcline': 246, 'name': 'Default', 'parent': 0, 'srcfile': '/opt/ros/kinetic/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'cstate': 'true', 'parentname': 'Default', 'class': 'DEFAULT', 'field': 'default', 'state': True, 'parentclass': '', 'groups': [{'upper': 'STEER', 'lower': 'steer', 'srcline': 123, 'name': 'Steer', 'parent': 0, 'srcfile': '/opt/ros/kinetic/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'cstate': 'true', 'parentname': 'Default', 'class': 'DEFAULT::STEER', 'field': 'DEFAULT::steer', 'state': True, 'parentclass': 'DEFAULT', 'groups': [], 'parameters': [{'srcline': 9, 'description': 'P value for Steer PID controller', 'max': 1.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/home/student/Documents/Final-System-Integrated/ros/src/twist_controller/cfg/PIDParams.cfg', 'name': 'Steer_P', 'edit_method': '', 'default': 0.58, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 10, 'description': 'I value for Steer PID controller', 'max': 1.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/home/student/Documents/Final-System-Integrated/ros/src/twist_controller/cfg/PIDParams.cfg', 'name': 'Steer_I', 'edit_method': '', 'default': 0.0108, 'level': 0, 'min': 0.0, 'type': 'double'}, {'srcline': 11, 'description': 'D value for Steer PID controller', 'max': 1.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/home/student/Documents/Final-System-Integrated/ros/src/twist_controller/cfg/PIDParams.cfg', 'name': 'Steer_D', 'edit_method': '', 'default': 0.001, 'level': 0, 'min': 0.0, 'type': 'double'}], 'type': '', 'id': 1}, {'upper': 'THROTTLE', 'lower': 'throttle', 'srcline': 123, 'name': 'Throttle', 'parent': 0, 'srcfile': '/opt/ros/kinetic/lib/python2.7/dist-packages/dynamic_reconfigure/parameter_generator_catkin.py', 'cstate': 'true', 'parentname': 'Default', 'class': 'DEFAULT::THROTTLE', 'field': 'DEFAULT::throttle', 'state': True, 'parentclass': 'DEFAULT', 'groups': [], 'parameters': [{'srcline': 14, 'description': 'P value for Throttle PID controller', 'max': 1.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/home/student/Documents/Final-System-Integrated/ros/src/twist_controller/cfg/PIDParams.cfg', 'name': 'Throttle_P', 'edit_method': '', 'default': 0.6, 'level': 1, 'min': 0.0, 'type': 'double'}, {'srcline': 15, 'description': 'I value for Throttle PID controller', 'max': 1.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/home/student/Documents/Final-System-Integrated/ros/src/twist_controller/cfg/PIDParams.cfg', 'name': 'Throttle_I', 'edit_method': '', 'default': 0.01, 'level': 1, 'min': 0.0, 'type': 'double'}, {'srcline': 16, 'description': 'D value for Throttle PID controller', 'max': 1.0, 'cconsttype': 'const double', 'ctype': 'double', 'srcfile': '/home/student/Documents/Final-System-Integrated/ros/src/twist_controller/cfg/PIDParams.cfg', 'name': 'Throttle_D', 'edit_method': '', 'default': 0.0, 'level': 1, 'min': 0.0, 'type': 'double'}], 'type': '', 'id': 2}], 'parameters': [], 'type': '', 'id': 0}

min = {}
max = {}
defaults = {}
level = {}
type = {}
all_level = 0

#def extract_params(config):
#    params = []
#    params.extend(config['parameters'])    
#    for group in config['groups']:
#        params.extend(extract_params(group))
#    return params

for param in extract_params(config_description):
    min[param['name']] = param['min']
    max[param['name']] = param['max']
    defaults[param['name']] = param['default']
    level[param['name']] = param['level']
    type[param['name']] = param['type']
    all_level = all_level | param['level']

