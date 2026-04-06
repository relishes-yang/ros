#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import math
import tf2_ros
import geometry_msgs.msg
from tf.transformations import quaternion_from_euler

class RobotTFPublisher:
    def __init__(self):
        # 初始化节点，节点名称严格符合实验要求：robot_tf_publisher
        rospy.init_node('robot_tf_publisher', anonymous=True)
        
        # TF广播器
        self.tf_broadcaster = tf2_ros.TransformBroadcaster()
        
        # 实验给定的改进型DH参数（单位：m/rad）
        # 格式：[a_i, alpha_i(°), d_i, theta_i(rad)]
        self.dh_params = [
            [0,    0,    0.1,  0.5],   # 关节1：a1, alpha1, d1, theta1
            [-0.2, 0,    0,   -0.3],   # 关节2：a2, alpha2, d2, theta2
            [0,    0,    0.3,  0.7],   # 关节3：a3, alpha3, d3, theta3
            [0,   -90,  -0.1, -0.2],   # 关节4：a4, alpha4, d4, theta4
            [0,    90,   0,    0.4],   # 关节5：a5, alpha5, d5, theta5
            [0,    0,    0.1, -0.1]    # 关节6：a6, alpha6, d6, theta6
        ]
        
        # 🔥 修复：坐标系列表多加一个末端，避免越界，前6个完全符合实验要求
        self.frame_names = ["base_link", "link2", "link3", "link4", "link5", "link6", "end_effector"]
        
        # 发布频率10Hz
        self.rate = rospy.Rate(10)
        
        rospy.loginfo("✅ 机器人TF发布节点已启动，改进DH参数已加载")

    # 改进型DH参数变换矩阵计算（核心！Modified DH公式）
    def modified_dh_transform(self, a, alpha_deg, d, theta):
        """
        改进型DH变换矩阵：T_{i-1}^i = RotX(alpha_{i-1}) * TransX(a_{i-1}) * RotZ(theta_i) * TransZ(d_i)
        """
        alpha = math.radians(alpha_deg)  # 角度转弧度
        # 变换矩阵的平移和旋转分量
        trans_x = a
        trans_z = d
        rot_x = alpha
        rot_z = theta
        return trans_x, trans_z, rot_x, rot_z

    # 发布TF变换
    def publish_tf(self):
        while not rospy.is_shutdown():
            # 遍历6个关节，依次发布base_link→link2→link3→link4→link5→link6→end_effector
            for i in range(6):
                a, alpha, d, theta = self.dh_params[i]
                # 计算改进DH变换的平移和旋转
                trans_x, trans_z, rot_x, rot_z = self.modified_dh_transform(a, alpha, d, theta)
                
                # 创建TF消息
                t = geometry_msgs.msg.TransformStamped()
                # 时间戳
                t.header.stamp = rospy.Time.now()
                # 父坐标系：前一个连杆，第一个父坐标系是base_link
                t.header.frame_id = self.frame_names[i]
                # 子坐标系：后一个连杆
                t.child_frame_id = self.frame_names[i+1]
                
                # 平移分量（改进DH的平移）
                t.transform.translation.x = trans_x
                t.transform.translation.y = 0.0
                t.transform.translation.z = trans_z
                
                # 旋转分量：先绕X转alpha，再绕Z转theta，转四元数
                q = quaternion_from_euler(rot_x, 0.0, rot_z)
                t.transform.rotation.x = q[0]
                t.transform.rotation.y = q[1]
                t.transform.rotation.z = q[2]
                t.transform.rotation.w = q[3]
                
                # 广播TF
                self.tf_broadcaster.sendTransform(t)
            
            # 保持发布频率
            self.rate.sleep()

if __name__ == '__main__':
    try:
        node = RobotTFPublisher()
        node.publish_tf()
    except rospy.ROSInterruptException:
        pass
