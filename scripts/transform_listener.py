#!/usr/bin/env python
"""
Created Apr 28th, 2015

@author: Sophia Li, contact: sophia.li@students.olin.edu

This script listens to the outputs from ar_track_alvar's tag finder and finds the
(x,y) location of the camera from a designated origin

Units is in meters until publishing step because publishing message only accepts integers
"""

import roslib
roslib.load_manifest('ar_track_alvar')
import rospy
import math

from std_msgs.msg import Int16MultiArray
import geometry_msgs.msg
import ar_track_alvar_msgs.msg

import tf
from tf.transformations import euler_from_quaternion

def callback(data):
    found_markers = []

    x_dists = []
    y_dists = []

    #Manually populate transform dictionary here, key is the tag ID, values are real world offsets from defined origin
    #transform_dict = {tagID:(x_dist, y_dist, angle, position)}
    transform_dict = {1:(0.3,1.6,"up"), 2:(1.25,0 , "left"), 3:(0.6,0, "right")}

    for i in range(len(data.markers)):
        angles = []
        marker_id = data.markers[i].id
        if marker_id > 200: #we're only expecting tag IDs up to 200. Anything larger is likely error and is ignored
            continue       #change threshold if we end up having lots of tags... but that shouldn't happen

        marker_position = data.markers[i].pose.pose.position #z is our real world x distance, x is real world y. Yep, it's confusing!
        marker_orientation = data.markers[i].pose.pose.orientation
        euler_marker = euler_from_quaternion((marker_orientation.x, marker_orientation.y, marker_orientation.z, marker_orientation.w))

        marker_yaw = euler_marker[1]

        calc_marker_y = marker_position.z*math.tan(marker_yaw)

        print "markery", marker_position.x, "markerx", marker_position.z
        print "pose y", calc_marker_y
        print "distance y", marker_position.x - calc_marker_y
        #marker_position.x = marker_y

        print 'rotation: ', marker_yaw*(180.0/math.pi)
        found_markers.append((marker_id, marker_position, marker_yaw, calc_marker_y))

    for marker in found_markers:
        try:
            dict_entry = transform_dict[marker[0]]
        except: #if a "tag" is found that we haven't defined, skip it
            continue
        if dict_entry[2] == "up":
            x_dist = marker[1].x - dict_entry[0]
            y_dist = marker[1].z - dict_entry[1]
        elif dict_entry[2] == "down":
            x_dist = dict_entry[0] - marker[1].x
            y_dist = dict_entry[1] - marker[1].z
        elif dict_entry[2] == "left":
            x_dist = marker[1].z - dict_entry[0]
            y_dist = marker[1].x - dict_entry[1]
        elif dict_entry[2] == "right":
            x_dist = dict_entry[0] - marker[1].z
            y_dist = dict_entry[1] - marker[1].x


        x_dists.append(x_dist)
        y_dists.append(y_dist)

    try:
        camera_location = [int(sum(x_dists)*100/len(x_dists)), int(sum(y_dists)*100/len(y_dists))] #making everything in terms of cm
        msg = Int16MultiArray()
        msg.data = camera_location
        pub.publish(msg)
        #print camera_location

    except:
        pass




if __name__ == '__main__':
    rospy.init_node('alvar_listener')

    pub = rospy.Publisher('camera_location', Int16MultiArray,queue_size=1)
    rospy.Subscriber("ar_pose_marker", ar_track_alvar_msgs.msg.AlvarMarkers, callback)
    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        rate.sleep()