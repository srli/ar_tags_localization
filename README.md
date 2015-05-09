# ar_tags_localization
AR tags are super cool :D

To run, make sure usb_cam is running so ar_track_ar has a camera message to listen to.

Run:
	roslaunch usb_cam usb_camera.launch

    roslaunch ar_track_alvar robot.launch

    rosrun ar_track_alvar transform_listener.py

Edit robot.launch file to change camera and tag characteristics.
Edit transform_listener.py to change tag locations to origin and to add new tags

Transform listener broadcasts the location of the camera in the world frame with
(x,y) and angle to the /camera_location node

We considered various ways to faciliate indoor localization, initially starting with the idea of beacon detection. By finding various light beacons placed in strategic locations around the area, we would be able to extrapolate the location of the camera in the world frame through triangulation. However, issues with color filitering in noisy conditions made beacon detection a rather poor choice for reliable detection.

Localization through use of fiducials allows for reliable tag detection in a variety of lighting conditions. Given a fiducial of a known size, we can compute the position of the camera relative to said fiducial based on the distortion of the detected tag. As we know the location of each tag relative to the real world, we can then extract the location of the camera in the world frame. We are basing the majority of the math from the ar_track_alvar library.

Fiducials bring with them many advantages, the greatest of which is reliable detection. A fiducial can also encode data additional to just IDs, including URLs or short bytes of messages, allowing users to provide the robot more information than just tag IDs. Adding additional tags to a system requires running an interactive script that will automatically create new tag images. A robot needs only to see one tag to know where it is in the world, but strategic placement of tags is necessary for more accurate calculations (i.e tags seen at great distances will naturally have more uncertainty).

However, as fiducials are two-dimensional, more tags are needed for the robot to succesfully localize compared to beacons. This problem can be addressed by placing tags on various sides of a pillar or cube and treating the group of tags as a bundle that discribe the same thing in space.
