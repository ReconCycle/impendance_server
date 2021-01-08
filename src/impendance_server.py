#!/usr/bin/env python

# TEMPLATE FOR ROS1

# IMPORT ROS
import rospy

# IMPORT REQUIRED ROS SERVICES
#from beginner_tutorials.srv import AddTwoInts,AddTwoIntsResponse

# IMPORT REQUIRED ROS TOPICS

# IMPORT APLICATION SPECIFIC





# DEFFINE NODE CLASS

class ImpendanceServer(object):

    def __init__(self):

        # CREATE NODE SERVICES (name, service type, service callback)


        self.node_srv=[] 

        command_srv=rospy.Service('~change_cart_imp', ChangeCartesianImpendance,self.callback_change_cart_imp)
        self.node_srv.append()

        # CREATE NODE SERVICE CLIENTS

        # CREATE NODE PUBLISHERS

        # CREATE NODE SUBSCRIBERS

        



    def clean(self):

        # DELETE ALL SERVICES

        for i in self.node_srv:

            i.shotdown('shoting down node')  


    def  callback_change_cart_imp(self,request):
        pass










def handle_add_two_ints(req):
    print("Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
    return AddTwoIntsResponse(req.a + req.b)

def add_two_ints_server():
    rospy.init_node('add_two_ints_server')
    s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
    print("Ready to add two ints.")
    rospy.spin()

if __name__ == "__main__":

    # CREATE APLICATION NODE
    active_node = ImpendanceServer()

    # RUN ROS
    rospy.spin()

    # CLEAN ON NODE SHOTDOWN
    rospy.on_shutdown(active_node.clean)
