#!/usr/bin/env python

# TEMPLATE FOR ROS1

# IMPORT ROS
import rospy

# IMPORT REQUIRED ROS SERVICES (from beginner_tutorials.srv import AddTwoInts,AddTwoIntsResponse)

from robot_module_msgs.srv import SetCartImpendance, SetCartImpendanceResponse

from std_srvs.srv import Trigger, TriggerResponse
from std_msgs.msg import Empty
# IMPORT REQUIRED ROS TOPICS

from robot_module_msgs.msg import ImpedanceParameters

# IMPORT APLICATION SPECIFIC PYTHON PACKAGES

import numpy as np



# DEFFINE NODE CLASS

class ImpendanceServer(object):

    stiff_robot_pos_stf=300
    stiff_robot_or_stf=30

    soft_robot_pos_stf=20
    soft_robot_or_stf=20

    change_rate=20



    name_space='test'
    def __init__(self):

        print('test')

        # INIT NODE

        rospy.init_node('impendance_server')


        # CREATE NODE SERVICES rospy.Service(name, service type, service callback)


        self.node_srv=[] 

        command_srv=rospy.Service('~change_cart_imp', SetCartImpendance,self.callback_change_cart_imp)
        self.node_srv.append(command_srv)

        command_srv=rospy.Service('~make_robot_stiff', Trigger,self.callback_make_robot_stiff)
        self.node_srv.append(command_srv)

        command_srv=rospy.Service('~make_robot_soft', Trigger,self.callback_make_robot_soft)
        self.node_srv.append(command_srv)


        # CREATE NODE SERVICE CLIENTS

        #client = rospy.ServiceProxy('stiffness', 
       

        # CREATE NODE PUBLISHERS  rospy.Publisher(name, type, queue_size=)

        self.pub_stiff = rospy.Publisher('stiffness', ImpedanceParameters,queue_size=10)
        self.pub_reset = rospy.Publisher('reset_target', Empty,queue_size=10)
        # CREATE NODE SUBSCRIBERS

        self.callback_make_robot_soft(1)



    def clean(self):

        # DELETE ALL SERVICES

        for i in self.node_srv:

            i.shutdown('shuting down node')  

    def callback_make_robot_stiff(self,request):

        self.change_cart_impendance(self.stiff_robot_pos_stf,self.stiff_robot_or_stf,self.change_rate)

        response = TriggerResponse()
        response.success = True
        response.message = 'All ok'

        return response


    def callback_make_robot_soft(self,request):

        
        self.change_cart_impendance(self.soft_robot_pos_stf,self.soft_robot_or_stf, self.change_rate)

        response = TriggerResponse()
        response.success = True
        response.message = 'All ok'

        return response


    def  callback_change_cart_imp(self,request):
        



        # send response


        pass

    def change_cart_impendance(self, desired_pos_impedance, desired_or_impendance, change_rate):


        # read actual impendance
        actual_pos_impedance=100
        actual_or_impedance=100

        # calculate changing function
        number_of_steps=10*abs(actual_pos_impedance-desired_pos_impedance)/change_rate #because we send each 0.1 s

        function_pos = np.linspace(actual_pos_impedance, desired_pos_impedance,number_of_steps)
        function_or = np.linspace(actual_pos_impedance, desired_pos_impedance,number_of_steps)


        # reset robot neural position

        self.pub_reset.publish(Empty())
        print('reset_response')
        # change impendance
        stiffness = ImpedanceParameters()
        for i in range(0,len(function_pos)):
            
            stiffness.k=[function_pos[i]]
            self.pub_stiff.publish(stiffness)
            rospy.sleep(0.1)

        return 1




if __name__ == "__main__":

    # CREATE APLICATION NODE
    active_node = ImpendanceServer()

    # RUN ROS
    rospy.spin()

    # CLEAN ON NODE SHOTDOWN
    rospy.on_shutdown(active_node.clean)
