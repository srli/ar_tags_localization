#!/usr/bin/env python
import roslib
roslib.load_manifest('ar_track_alvar')
import rospy
import math
import tf
import geometry_msgs.msg
import ar_track_alvar_msgs.msg

def callback(data):
    found_markers = []
    x_dist = 0
    y_dist = 0

    transform_dict = {1:(0, 1.7), 2:(1,1.4)}
    #We populate dictionary here

    for i in range(len(data.markers)):
        marker_id = data.markers[i].id
        marker_position = data.markers[i].pose.pose.position #z is our real world x distance, x is real world y.
        found_markers.append((marker_id, marker_position))

    for marker in found_markers:
        if marker[0] == 2:
            x_dist = marker[1].z - transform_dict[i][1] #something of the sort
            print marker[1]

if __name__ == '__main__':
    rospy.init_node('alvar_listener')

    pub = rospy.Publisher('camera_location', geometry_msgs.msg.Twist,queue_size=1)
    rospy.Subscriber("ar_pose_marker", ar_track_alvar_msgs.msg.AlvarMarkers, callback)

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        rate.sleep()