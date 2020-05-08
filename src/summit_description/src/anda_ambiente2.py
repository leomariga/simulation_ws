#!/usr/bin/env python  
import rospy, tf2_ros, geometry_msgs.msg, math
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion

ultimotempo = 0
velRobo = geometry_msgs.msg.Twist()
posRobo = geometry_msgs.msg.Pose()

def callbackVel(veldata):
    global velRobo
    print("Callbackou")
    velRobo = veldata


def calculaPosicao(dt):
    global velRobo
    global posRobo

    eulangulo = list(euler_from_quaternion([posRobo.orientation.x, posRobo.orientation.y, posRobo.orientation.z, posRobo.orientation.w]))

    eulangulo[2] =  eulangulo[2] + velRobo.angular.z * ((float) (dt.nsecs)/1000000000)

    posRobo.position.x =  posRobo.position.x + math.cos(eulangulo[2])*(velRobo.linear.x * ((float) (dt.nsecs)/1000000000))
    posRobo.position.y =  posRobo.position.y + math.sin(eulangulo[2])*(velRobo.linear.x * ((float) (dt.nsecs)/1000000000))

    posRobo.position.x =  posRobo.position.x + math.sin(eulangulo[2])*(velRobo.linear.y * ((float) (dt.nsecs)/1000000000))
    posRobo.position.y =  posRobo.position.y + math.cos(eulangulo[2])*(velRobo.linear.y * ((float) (dt.nsecs)/1000000000))

    quat = list(quaternion_from_euler(eulangulo[0], eulangulo[1], eulangulo[2]))

    posRobo.orientation.x = quat[0]
    posRobo.orientation.y = quat[1]
    posRobo.orientation.z = quat[2]
    posRobo.orientation.w = quat[3]
    print("---------\n"+str(eulangulo))


def transformaframe():
    global ultimotempo
    global posRobo
    dt = rospy.Time.now()-ultimotempo
    #print("Callbackou "+ str(dt.nsecs))
    calculaPosicao(rospy.Time.now()-ultimotempo)
    ultimotempo = rospy.Time.now()
    tf2Broadcast = tf2_ros.TransformBroadcaster()
    tf2Stamp = geometry_msgs.msg.TransformStamped()
    tf2Stamp.header.stamp = rospy.Time.now()
    tf2Stamp.header.frame_id = 'map'
    tf2Stamp.child_frame_id = 'rs200_camera'
    tf2Stamp.transform.translation.x = posRobo.position.x
    tf2Stamp.transform.translation.y = posRobo.position.y
    tf2Stamp.transform.translation.z = posRobo.position.z
    tf2Stamp.transform.rotation.x = posRobo.orientation.x
    tf2Stamp.transform.rotation.y = posRobo.orientation.y
    tf2Stamp.transform.rotation.z = posRobo.orientation.z
    tf2Stamp.transform.rotation.w = posRobo.orientation.w
    tf2Broadcast.sendTransform(tf2Stamp)

def transformaFramesThread():
    rate = rospy.Rate(100) # 20hz
    while not rospy.is_shutdown():
        
        transformaframe()
        rate.sleep()



if __name__ == '__main__':
    print("Vamos comecar o teste")
    rospy.init_node("transformador")
    rospy.Subscriber('cmd_vel', geometry_msgs.msg.Twist, callbackVel)
    ultimotempo = rospy.Time.now()
    transformaFramesThread()
    rospy.spin()


