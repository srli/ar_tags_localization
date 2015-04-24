#!/usr/bin/env python
import roslib
roslib.load_manifest('ar_track_alvar')

import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('marker_static_transforms')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        br.sendTransform((0.0, 0.0, 0),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "origin",
                         "world")
        br.sendTransform((0.0, 0.0, 1.7),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "ar_marker_1",
                         "origin")
        br.sendTransform((0, 0.0, 1.25), #need to repeat these transform broadcasters for each ar_tag we've coded
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "ar_marker_2",
                         "origin")

        rate.sleep()