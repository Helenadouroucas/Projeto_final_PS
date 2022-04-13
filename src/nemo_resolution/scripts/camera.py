import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from marlintwist import Andar

rospy.init_node("testando", anonymous=True)

class Camera():
    def __init__(self):
        self.bridge = CvBridge()
        self.subs = rospy.Subscriber("camera/image_raw", Image, self.start)
        rospy.wait_for_message("camera/image_raw", Image)

    def start(self, msg):
        greenLower = (29, 86, 6)
        greenUpper = (64, 255, 255)
        rate = rospy.Rate(10)
        #msg = rospy.wait_for_message("camera/image_raw", Image)
        self.img = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        maskGreen = cv2.inRange(self.hsv, greenLower, greenUpper)
        maskGreen = cv2.erode(maskGreen, None, iterations=2) 
        maskGreen = cv2.dilate(maskGreen, None, iterations=2)
        cntGreen = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        
        if len(cntGreen) > 0:
            marlin = Andar()
            marlin.start()

        rate.sleep()

if __name__ == '__main__':
    try:

       while True: 
         msg = Image()
         msg.header.stamp = rospy.Time.now()
         msg = rospy.wait_for_message("camera/image_raw", Image)
         image = Camera()
         image.start(msg)

    except rospy.ROSInterruptException:
        pass    
