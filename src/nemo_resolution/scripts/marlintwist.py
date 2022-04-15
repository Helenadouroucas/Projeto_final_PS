#!/usr/bin/env python3
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
import math
from geometry_msgs.msg import PointStamped

rospy.init_node("nadar", anonymous=True)

class angulomarlin():
    def __init__(self, model_name):
        self.model_name = model_name
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.callback)
        rospy.wait_for_message("/gazebo/model_states", ModelStates)


    def callback(self, msg):
        index = msg.name.index(self.model_name)
        self.pos = msg.pose[index]
        self.z = self.pos.orientation.z
        self.w = self.pos.orientation.w
        self.arco = math.acos(self.z)
        self.ang = 2*(self.arco-(np.pi)/2)+(np.pi)/2
        self.angg = np.degrees(self.ang)
        if (self.w>0):
            self.angg=((-1)*(self.angg-90))+90

class angulovetor():
    def __init__(self):      
        rospy.Subscriber("sonar_data",PointStamped,self.callback)
        rospy.wait_for_message("sonar_data", PointStamped)
    def callback(self,msg):
        self.y=msg.point.y
        self.x=msg.point.x
        self.tang = self.y/self.x
        self.ang=math.atan(self.tang)
        self.angg = np.degrees(self.ang)
        if(self.x>0):
            self.angg+=180

marlin = angulomarlin("marlin")
vetor = angulovetor()


vel = Twist()
vel.linear.x=0
vel.linear.y=2
vel.linear.z=0
vel.angular.x=0
vel.angular.y=0
rate = rospy.Rate(20)
pub = rospy.Publisher("cmd_vel", Twist,queue_size=10)

while not rospy.is_shutdown():
    
    d = vetor.angg-marlin.angg
    if(d>180):
        d-=360
    elif(d<-180):
        d+=360
    vel.angular.z=d/16
    pub.publish(vel)
    rate.sleep()

rospy.spin()