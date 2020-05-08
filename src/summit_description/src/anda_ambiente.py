#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist


def move():
    # Starts a new node
    rospy.init_node('comandante', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    #Receiveing the user's input
    print("Let's move your robot")

    vel_parado = Twist()
    vel_parado.linear.x = 0
    vel_parado.linear.y = 0
    vel_parado.linear.z = 0
    vel_parado.angular.x = 0
    vel_parado.angular.y = 0
    vel_parado.angular.z = 0
    t_parado = 1

    vel1 = Twist()
    vel1.linear.x = 0
    vel1.linear.y = 0
    vel1.linear.z = 0
    vel1.angular.x = 0
    vel1.angular.y = 0
    vel1.angular.z = -0.25
    t1 = 12

    vel2 = Twist()
    vel2.linear.x = 0.25
    vel2.linear.y = 0
    vel2.linear.z = 0
    vel2.angular.x = 0
    vel2.angular.y = 0
    vel2.angular.z = 0
    t2 = 12

    vel3 = Twist()
    vel3.linear.x = 0
    vel3.linear.y = 0.25
    vel3.linear.z = 0
    vel3.angular.x = 0
    vel3.angular.y = 0
    vel3.angular.z = 0.1
    t3 = 8




    comandos = [vel_parado, vel_parado, vel_parado,vel_parado, vel_parado, vel1, vel_parado, vel2, vel3, vel1, vel_parado]
    tempos = [t_parado, t_parado, t_parado, t_parado, t_parado, t1, t_parado, t2, t3, 2, t_parado]


    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        for i in range(len(comandos)):
            velocity_publisher.publish(comandos[i])

            time.sleep(tempos[i])
            if i == len(comandos)-1:
                return
        rate.sleep()


if __name__ == '__main__':
    try:
        #Testing our function
        move()
    except rospy.ROSInterruptException: pass