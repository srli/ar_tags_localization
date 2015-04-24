#!/usr/bin/env python
import roslib
roslib.load_manifest('ar_track_alvar')
import rospy
import math
import tf
from std_msgs.msg import Int16MultiArray
import geometry_msgs.msg
import ar_track_alvar_msgs.msg

def callback(data):
    found_markers = []

    x_dists = []
    y_dists = []

    #Manually populate transform dictionary here
    transform_dict = {2:(0, 1, "up"), 3:(1,0, "right")}

    for i in range(len(data.markers)):
        marker_id = data.markers[i].id
        marker_position = data.markers[i].pose.pose.position #z is our real world x distance, x is real world y.
        found_markers.append((marker_id, marker_position))

    for marker in found_markers:
        try:
            dict_entry = transform_dict[marker[0]]
        except: #if a "tag" is found that we haven't defined, skip it
            continue
        if dict_entry[2] == "up":
            x_dist = marker[1].x - dict_entry[0]
            y_dist = marker[1].z - dict_entry[1]
        elif dict_entry[2] == "right":
            x_dist = marker[1].z - dict_entry[0]
            y_dist = marker[1].x - dict_entry[1]
        x_dists.append(x_dist)
        y_dists.append(y_dist)

    try:
        camera_location = [int(sum(x_dists)*100/len(x_dists)), int(sum(y_dists)*100/len(y_dists))] #making everything in terms of cm
        msg = Int16MultiArray()
        msg.data = camera_location
        pub.publish(msg)
        print camera_location

    except:
        pass




if __name__ == '__main__':
    rospy.init_node('alvar_listener')

    pub = rospy.Publisher('camera_location', Int16MultiArray,queue_size=1)
    rospy.Subscriber("ar_pose_marker", ar_track_alvar_msgs.msg.AlvarMarkers, callback)

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        rate.sleep()