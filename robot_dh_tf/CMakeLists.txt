cmake_minimum_required(VERSION 3.0.2)
project(robot_dh_tf)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
  std_msgs
  tf2
  tf2_ros
)

catkin_package(
  CATKIN_DEPENDS geometry_msgs rospy std_msgs tf2 tf2_ros
)

# 关键：安装Python脚本到ROS可执行目录
catkin_install_python(PROGRAMS
  scripts/robot_tf_publisher.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)
