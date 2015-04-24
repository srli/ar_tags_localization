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

    for i in range(len(data.markers)):
        marker_id = data.markers[i].id
        marker_position = data.markers[i].pose.pose.position #z is our real world x distance, x is real world y.
        found_markers.append((marker_id, marker_position))

    for marker in found_markers:
        if marker[0] == 2:
            x_dist = marker[1].z - 1
            print marker[1]
    #print x_dist

    #print data.markers
    # try:
    #     # i = 2
    #     # if "id: "+str(i) in data.markers[0]:
    #     #     print "id!: "+str(i)
    #     # elif "id: "+str(i) not in data.markers[0]:
    #     #     print "not here!"
    #     #print data.markers[0]
    #     print type(data.markers[0].id)
    #         #print "hello"
    # except:
    #     print "exception raised"
    #     pass

if __name__ == '__main__':
    rospy.init_node('alvar_listener')

    listener = tf.TransformListener()

    turtle_vel = rospy.Publisher('camera_position', geometry_msgs.msg.Twist,queue_size=1)
    rospy.Subscriber("ar_pose_marker", ar_track_alvar_msgs.msg.AlvarMarkers, callback)

    rate = rospy.Rate(10.0)

    #transform_dict = {}
    marker1_transform = (0, 1.7) #x, y from origin
    marker2_transform = (-1.2, 0)

    x_dist = 0
    y_dist = 0

    while not rospy.is_shutdown():
        for i in range(1,3):
            try:
                (trans,rot) = listener.lookupTransform('/usb_cam', '/ar_marker_'+str(i), rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue                 #if tag not found, we move on to next tag
            distance = trans[2]
            if i == 1:
                x_dist = 0
                y_dist = marker1_transform[1] - distance
            elif i==2:
                x_dist = marker2_transform[0] + distance
        origin_dist = (x_dist, y_dist)
        #print "distance from origin is ", origin_dist



            #print rot
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