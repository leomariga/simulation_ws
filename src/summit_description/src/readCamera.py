#!/usr/bin/env python

# Ros Messages
from sensor_msgs.msg import Image, CameraInfo


import message_filters
import cv2
import rospy
import numpy as np
from cv_bridge import CvBridge

def callback(depth_msg, rgb_msg, camera_info):
    depth_image = CvBridge().imgmsg_to_cv2(depth_msg, desired_encoding="16UC1")
    rgb_image = CvBridge().imgmsg_to_cv2(rgb_msg, desired_encoding="rgb8")
    # The depth image is a single-channel float32 image
    # the values is the distance in mm in z axis
    # Convert the depth image to a Numpy array since most cv2 functions
    # require Numpy arrays.
    depth_array = np.array(depth_image, dtype=np.float32)
    # Normalize the depth image to fall between 0 (black) and 1 (white)
    cv2.normalize(depth_array, depth_array, 0, 1, cv2.NORM_MINMAX)
    # At this point you can display the result properly:
    #cv2.imshow('Depth Image', rgb_image)
    # If you write it as it si, the result will be a image with only 0 to 1 values.
    # To actually store in a this a image like the one we are showing its needed
    # to reescale the otuput to 255 gray scale.
    cv2.imwrite('1_depth.png',depth_array*255)
    cv2.imwrite('1_rgb.png',rgb_image)
    #cv2.normalize(d_image, d_image, 0, 1, cv2.NORM_MINMAX)
    #cv2.imshow('a', d_image)
    cv2.waitKey(2)

if __name__ == '__main__':
    rospy.init_node('my_node', anonymous=True)
    depth_sub = message_filters.Subscriber('/r200/camera/depth/image_raw', Image)
    rgb_sub = message_filters.Subscriber('/r200/camera/color/image_raw', Image)
    info_sub = message_filters.Subscriber('/r200/camera/depth/camera_info', CameraInfo)
    ts = message_filters.ApproximateTimeSynchronizer([depth_sub, rgb_sub, info_sub], 10, 0.2)
    ts.registerCallback(callback)
    rospy.spin()