import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

rospy.init_node("testando",anonymous=True)

class Camera():
    def __init__(self):
        self.bridge = CvBridge()
        self.pub = rospy.Subscriber("camera/image_raw",Image, self.start)
        rospy.wait_for_message("camera/image_raw", Image)

    def start(self, msg):
        msg = rospy.wait_for_message("camera/image_raw",Image)
        self.img = self.bridge.imgmsg_to_cv2(msg,"bgr8")
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            cv2.imshow("Frontal Camera", self.img)
            cv2.waitKey()
            rate.sleep()

if __name__ == '__main__':
    try:
        image = Camera()
        image.start()
    except rospy.ROSInterruptException:
        pass
