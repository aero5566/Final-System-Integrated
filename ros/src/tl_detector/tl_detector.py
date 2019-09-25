#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped, Pose
from styx_msgs.msg import TrafficLightArray, TrafficLight
from styx_msgs.msg import Lane
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from light_classification.tl_classifier import TLClassifier as TLClassifier_SIM
from light_classification.tl_classifier_udcar import TLClassifier as TLClassifier_UDCAR
import tf
import cv2
import yaml


from scipy.spatial import KDTree
import math
import numpy as np

STATE_COUNT_THRESHOLD = 3

class TLDetector(object):
    def __init__(self):
        rospy.init_node('tl_detector')

        self.pose = None
        self.waypoints = None
        self.camera_image = None
        self.lights = []

        self.base_waypoints = None
        self.waypoints_2d = None
        self.waypoint_tree = None
        self.imgcount = 0
        self.red_light_state_count = 0
        self.green_light_state_count = 0

        sub1 = rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        sub2 = rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)

        '''
        /vehicle/traffic_lights provides you with the location of the traffic light in 3D map space and
        helps you acquire an accurate ground truth data source for the traffic light
        classifier by sending the current color state of all traffic lights in the
        simulator. When testing on the vehicle, the color state will not be available. You'll need to
        rely on the position of the light and the camera image to predict it.
        '''
        sub3 = rospy.Subscriber('/vehicle/traffic_lights', TrafficLightArray, self.traffic_cb)
        sub6 = rospy.Subscriber('/image_color', Image, self.image_cb)

        config_string = rospy.get_param("/traffic_light_config")
        self.config = yaml.load(config_string)

        self.is_site = self.config["is_site"]
        self.confidence_threshold = self.config["confidence_threshold"]

        self.upcoming_red_light_pub = rospy.Publisher('/traffic_waypoint', Int32, queue_size=1)

        self.bridge = CvBridge()

        if(self.is_site == False):
            self.light_classifier = TLClassifier_SIM( boIsContextRealCar    = self.is_site, 
                                                      boDebugMode           = False, 
                                                      ConfidenceThreshold   = self.confidence_threshold)
        else:
            self.light_classifier = TLClassifier_UDCAR()


        #self.light_classifier = TLClassifier()
        self.listener = tf.TransformListener()

        self.state = TrafficLight.UNKNOWN
        self.last_state = TrafficLight.UNKNOWN
        self.last_wp = -1
        self.state_count = 0

        #rospy.spin()

        self.handle_ros_spin()


    def handle_ros_spin(self):
        '''
        Publish upcoming red lights at camera frequency.
        Each predicted state has to occur `STATE_COUNT_THRESHOLD` number
        of times till we start using it. Otherwise the previous stable state is
        used.
        '''
        '''
        SR:
        *if*
        If observed state != state , set state to observed state and start the counter. The different state may be an exception
        and we have to make sure. 
        *elif*
        If the same state is seen more than thrice, we are sure the light has changed. Update last_state to state, update
        light_wp only if the light is red.
        (light_wp is the waypoint next to traffic light stop). Otherwise, set light_wp to -1. 
        Publish the waypoint and also set it to last_wp that has the previous known traffic light waypoint
        *else*
        This means that the observed state is same as the state but it hasn't been observed thrice. In this case, continue
        publishing the previous traffic light waypoint. 
        ****
        Finally, in all cases, increment the counter by one.
        '''
        rate = rospy.Rate(3)
        while not rospy.is_shutdown():
            if self.pose is not None and self.waypoints is not None and self.camera_image is not None:
                light_wp, state = self.process_traffic_lights()
                
                #if self.state != state:
                #    self.state_count = 0
                #    self.state = state
                #elif self.state_count >= STATE_COUNT_THRESHOLD:
                #    self.last_state = self.state
                #    light_wp = light_wp if state == TrafficLight.RED else -1
                #    self.last_wp = light_wp
                #    self.upcoming_red_light_pub.publish(Int32(light_wp))
                #else:
                #    self.upcoming_red_light_pub.publish(Int32(self.last_wp))
                #self.state_count += 1
                #print ("state_count:{0} | state:{1} | last_state: {2}".format(self.state_count, state, self.last_state) )
               
                if(state == TrafficLight.GREEN):
                    self.green_light_state_count +=1;
                else:
                    self.green_light_state_count = 0
                    
                if(state == TrafficLight.RED):
                    if(self.red_light_state_count < STATE_COUNT_THRESHOLD*2):
                        self.red_light_state_count += 1

                elif (self.red_light_state_count > 0) and (state != TrafficLight.RED):
                    self.red_light_state_count -= 1
                    if(self.green_light_state_count >= STATE_COUNT_THRESHOLD):
                        self.red_light_state_count = 0
                
                if(self.red_light_state_count >= STATE_COUNT_THRESHOLD):
                    self.last_wp = light_wp
                    self.upcoming_red_light_pub.publish(Int32(self.last_wp))
                else:
                    self.last_wp = -1
                    if(self.red_light_state_count == 0):
                        self.upcoming_red_light_pub.publish(Int32(self.last_wp))

                self.has_image = False
                self.camera_image = None
                
                print ("red_state_count:{0} | green_state_count:{1} | WP: {2}".\
                        format(self.red_light_state_count, self.green_light_state_count, self.last_wp) )
        rate(sleep)

    def pose_cb(self, msg):
        self.pose = msg

    def waypoints_cb(self, waypoints):
        self.waypoints = waypoints
        if not self.waypoints_2d:
            self.waypoints_2d = [[waypoint.pose.pose.position.x, waypoint.pose.pose.position.y] for waypoint in
                                 waypoints.waypoints]
            self.waypoint_tree = KDTree(self.waypoints_2d)

    def traffic_cb(self, msg):
        self.lights = msg.lights

    def image_cb(self, msg):
        """Identifies red lights in the incoming camera image and publishes the index
            of the waypoint closest to the red light's stop line to /traffic_waypoint

        Args:
            msg (Image): image from car-mounted camera

        """
        self.has_image = True
        self.camera_image = msg
        light_wp, state = self.process_traffic_lights()

        '''
        Publish upcoming red lights at camera frequency.
        Each predicted state has to occur `STATE_COUNT_THRESHOLD` number
        of times till we start using it. Otherwise the previous stable state is
        used.
        '''
        if self.state != state:
            self.state_count = 0
            self.state = state
        elif self.state_count >= STATE_COUNT_THRESHOLD:
            self.last_state = self.state
            light_wp = light_wp if state == TrafficLight.RED else -1
            self.last_wp = light_wp
            self.upcoming_red_light_pub.publish(Int32(light_wp))
        else:
            self.upcoming_red_light_pub.publish(Int32(self.last_wp))
        self.state_count += 1

    def get_closest_waypoint(self, pose):
        """Identifies the closest path waypoint to the given position
            https://en.wikipedia.org/wiki/Closest_pair_of_points_problem
        Args:
            pose (Pose): position to match a waypoint to

        Returns:
            int: index of the closest waypoint in self.waypoints

        """
        #TODO implement

        x = position_x
        y = position_y 

        #finde the closest waypoint's idx
        closest_idx = self.waypoint_tree.query([x,y], 1)[1]
        
        # check if closest is ahead or behind car
        closest_waypoint = self.waypoints_2d[closest_idx]
        pre_closest_waypoint = self.waypoints_2d[closest_idx-1]
        
        cl_vect = np.array(closest_waypoint)
        pre_vect = np.array(pre_closest_waypoint)
        pos_vect = np.array([x,y])

        if np.dot(cl_vect - pre_vect, pos_vect - cl_vect) > 0:
            closest_idx = (closest_idx + 1) % len(self.waypoints_2d)
        
        return closest_idx

    def get_light_state(self, light):
        """Determines the current color of the traffic light

        Args:
            light (TrafficLight): light to classify

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        if(not self.has_image):
            self.prev_light_loc = None
            return False

        cv_image = self.bridge.imgmsg_to_cv2(self.camera_image, "bgr8")

        #Get classification
        return self.light_classifier.get_classification(cv_image)

    def process_traffic_lights(self):
        """Finds closest visible traffic light, if one exists, and determines its
            location and color

        Returns:
            int: index of waypoint closes to the upcoming stop line for a traffic light (-1 if none exists)
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #light = None

        closest_light = None
        line_wp_idx = None

        # List of positions that correspond to the line to stop in front of for a given intersection
        stop_line_positions = self.config['stop_line_positions']
        '''
        if(self.pose):
            car_position = self.get_closest_waypoint(self.pose.pose)

        #TODO find the closest visible traffic light (if one exists)

        if light:
            state = self.get_light_state(light)
            return light_wp, state
        self.waypoints = None
        return -1, TrafficLight.UNKNOWN '''

        if(self.pose):
            car_wp_idx = self.get_closest_waypoint(self.pose.pose.position.x, self.pose.pose.position.y)

            #TODO find the closest visible traffic light (if one exists)
            diff = len(self.waypoints.waypoints)
            for i, light in enumerate(self.lights):
                # Get stop line waypoint index
                line = stop_line_positions[i]
                temp_wp_idx = self.get_closest_waypoint(line[0], line[1])
                # Find closest stop line waypoint index
                d = temp_wp_idx - car_wp_idx
                if d >=0 and d < diff:
                    diff = d
                    closest_light = light
                    line_wp_idx = temp_wp_idx
        if (closest_light):
            state = self.get_light_state(closest_light) # Commmented for the test detector
            
            return line_wp_idx, state
        
        return -1, TrafficLight.UNKNOWN

if __name__ == '__main__':
    try:
        TLDetector()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start traffic node.')
