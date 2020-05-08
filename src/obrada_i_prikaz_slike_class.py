#!/usr/bin/env python2.7

import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys
import os, shutil
import numpy as np

bridge = CvBridge()

def empty_folder(folder):  #folder path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try :
            if os.path.isfile(file_path) or ps.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree (file_path)
        except Exception as e :
            print('Faild to delete %s. Reason : %s' %(file_path,e))

class ImageFeature:

    def __init__(self, dir,n):
        self.n = n
        self.image_sub = rospy.Subscriber("/camera_topic"+str(self.n), Image, self.image_callback)
        self.image_pub = rospy.Publisher('show_topic'+str(self.n), Image, queue_size = 10 )


    def image_callback(self,ros_image):
        global i
        i+=1
        print('Got image from /camera_topic'+str(self.n))
        global bridge
        try :
            cv_image = bridge.imgmsg_to_cv2(ros_image, "8UC3")
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(cv_image, 'Ovo je slika s kamere'+str(self.n), (10,350), font, 1, (255,255,255),2, cv2.LINE_AA)
            cv2.imwrite(dir+'cam'+str(self.n)+'_obradeno/'+str(i)+'obradeno.jpg',cv_image)


            cv_image = np.uint8(cv_image)
            image_message = bridge.cv2_to_imgmsg(cv_image,encoding="passthrough")
            rospy.loginfo(cv_image)
            self.image_pub.publish(image_message)
        except CvBridgeError as e :
            print(e)


if __name__ == '__main__':
    rospy.init_node('obrada_slike', anonymous = True)
    i = 0
    #dir = rospy.get_param('~dir')
    print(dir)
    dir = '/home/ivan/catkin2_workspace/src/image_features/images/'

    for j in range(1,3):
            if not os.path.exists(dir+'/cam'+str(j)+'_obradeno'):
                os.makedirs(dir+'/cam'+str(j)+'_obradeno')
            else :
                 empty_folder(dir+'/cam'+str(j)+'_obradeno')


    ic1 = ImageFeature(dir,1)
    ic2 = ImageFeature(dir,2)

    try:
      rospy.spin()
    except KeyboardInterrupt:
       print("Shutting down")
    cv2.destroyAllWindows()
