#!/usr/bin/env python2.7

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import numpy as np

bridge = CvBridge()


def image_callback(ros_image):
  print ('got an image')
  global bridge
  #convert ros_image into an opencv-compatible image
  try:
    image_frame = bridge.imgmsg_to_cv2(ros_image, "8UC3")
    cv2.imshow('kamera2',image_frame)
    cv2.waitKey(3)
  except CvBridgeError as e:
      print(e)

def main(args):
  rospy.init_node('show_cv_frames_node2', anonymous=True)
  image_sub = rospy.Subscriber("show_topic2",Image, image_callback)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
