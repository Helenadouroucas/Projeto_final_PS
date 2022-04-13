#!/usr/bin/env python3
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
import random

class Andar:

   def _init__(self, lista, pub): 
      self.pub = pub
      self.lista = lista

   def start(self):
       self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
       self.lista = list(range(10))
       rospy.init_node('testando', anonymous=True) 
       rate = rospy.Rate(10) 
       while not rospy.is_shutdown():
          vetorvelocidade = Twist()
          vetorvelocidade.linear.y = 1
          vetorvelocidade.angular.z = 0
          rospy.loginfo(vetorvelocidade)
          self.pub.publish(vetorvelocidade)
          rate.sleep()
 
'''if __name__ == '__main__':
    try:
        t = Andar()
        t.start()
    except rospy.ROSInterruptException:
        pass'''