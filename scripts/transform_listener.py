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

    transform_dict = {}

    while not rospy.is_shutdown():
        for i in range(1,2):
            try:
                (trans,rot) = listener.lookupTransform('/ar_marker_'+str(i), '/world', rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue                 #if tag not found, we move on to next tag
            print rot
            # br = tf.TransformBroadcaster()
            # br.sendTransform((trans[0], trans[1], 0),
            #          tf.transformations.quaternion_from_euler(0, 0, rot[0]),
            #          rospy.Time.now(),
            #          '/ar_marker_' + str(i),
            #          'world')

            #angular = 4 * math.atan2(trans[1], trans[0])
            #linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
            # cmd = geometry_msgs.msg.Twist()
            # cmd.linear = trans
            # cmd.angular = rot
            # turtle_vel.publish(cmd)

        rate.sleep()