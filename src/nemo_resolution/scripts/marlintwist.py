#!/usr/bin/env python3
# Projeto Final Nautilus
# Helena e Wagner

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
        self.vel=msg.twist[index]
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
rate = rospy.Rate(15)
pub = rospy.Publisher("cmd_vel", Twist,queue_size=10)
modo=False

while not rospy.is_shutdown():
    if(modo==False):

        d = vetor.angg-marlin.angg
        if(d>180):
            d-=360
        elif(d<-180):
            d+=360
        vel.angular.z=d/12
        pub.publish(vel)

        if((marlin.vel.linear.x<0.05)and(marlin.vel.linear.y<0.05)and(marlin.vel.linear.x>-0.05)and(marlin.vel.linear.y>-0.05)):
            modo=True
            t=0
    else:
        if(t<18):
            vel.linear.y=0
            vel.angular.z=90/16
        else:
            vel.linear.y=2
            vel.angular.z=0
        pub.publish(vel)
        t+=1
        if(t>74):
            modo=False


    rate.sleep()

rospy.spin()