cmake_minimum_required(VERSION 3.0.2)
project(posvel_control)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

add_message_files(
  FILES
  Posvel.msg
)

catkin_python_setup()  # ✅ 必须在 generate_messages 之后

generate_messages(  # ✅ 必须在 catkin_python_setup 之前
  DEPENDENCIES
  std_msgs
)



catkin_package(
  CATKIN_DEPENDS rospy std_msgs message_runtime
)
