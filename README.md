# ar_tags_localization
AR tags are super cool :D

To run, make sure usb_cam is running so ar_track_ar has a camera message to listen to.

Run:
    roslaunch ar_track_alvar robot.launch
    rosrun ar_track_alvar transform_listener.py

Edit robot.launch file to change camera and tag characteristics.
Edit transform_listener.py to change tag locations to origin and to add new tags

Transform listener broadcasts the location of the camera in the world frame with
(x,y) and angle to the /camera_location node
