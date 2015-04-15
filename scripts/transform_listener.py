#!/usr/bin/env python
import roslib
roslib.load_manifest('ar_track_alvar')
import rospy
import math
import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('alvar_listener')

    listener = tf.TransformListener()

    turtle_vel = rospy.Publisher('camera_position', geometry_msgs.msg.Twist,queue_size=1)

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/ar_pose_marker', '/usb_cam', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print "exception found"
            continue

        angular = 4 * math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel.publish(cmd)

        rate.sleep()