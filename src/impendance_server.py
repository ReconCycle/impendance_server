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

    stiff_robot_pos_stf=100
    stiff_robot_or_stf=10

    soft_robot_pos_stf=0
    soft_robot_or_stf= 0

    change_rate=20

    damping=2



    name_space='/cartesian_impedance_controller/'
    def __init__(self):

      
        self.last_pos_impedence = 100
        self.last_or_impedence = 10
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

        self.pub_stiff = rospy.Publisher(self.name_space+'stiffness', ImpedanceParameters,queue_size=10)
        self.pub_reset = rospy.Publisher(self.name_space+'reset_target', Empty,queue_size=10)
        # CREATE NODE SUBSCRIBERS





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

    def change_cart_impendance(self, desired_pos_impedance, desired_or_impedance, change_rate):


        # read actual impendance
        actual_pos_impedance=self.last_pos_impedence
        actual_or_impedance=self.last_or_impedence

        # calculate changing function
        number_of_steps=10*abs(actual_pos_impedance-desired_pos_impedance)/change_rate #because we send each 0.1 s

        function_pos = np.linspace(actual_pos_impedance, desired_pos_impedance,number_of_steps)
        function_or = np.linspace(actual_or_impedance, desired_or_impedance,number_of_steps)


        # reset robot neural position

        self.pub_reset.publish(Empty())
        print('reset_response')
        # change impendance
        stiffness = ImpedanceParameters()
        for i in range(0,len(function_pos)):
            stiffness.n=9

            vector_k=np.zeros(2*stiffness.n)
            vector_d=np.zeros(2*stiffness.n)
            for j in [0,4,8]:
                vector_k[j]=function_pos[i]
                vector_k[j+stiffness.n]=function_or[i]
                vector_d[j]=self.damping
                vector_d[j+stiffness.n]=self.damping

            stiffness.k=vector_k
            stiffness.d=vector_d

            self.pub_stiff.publish(stiffness)

            #save last published impendance
            self.last_pos_impedence=function_pos[i]
            self.last_or_impedence=function_or[i]

            rospy.sleep(0.1)

        return 1




if __name__ == "__main__":

    # CREATE APLICATION NODE
    active_node = ImpendanceServer()

    # RUN ROS
    rospy.spin()

    # CLEAN ON NODE SHOTDOWN
    rospy.on_shutdown(active_node.clean)
