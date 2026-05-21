#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import math
import rosservice
from turtlesim.srv import Spawn
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class TurtleFormation:
    def __init__(self):
        """初始化ROS节点和编队参数"""
        rospy.init_node('turtle_formation_node', anonymous=True)
        
        # 🔥 自动生成turtle2和turtle3（核心修复！）
        self.spawn_turtle(5.0, 5.0, 0.0, "turtle2")
        self.spawn_turtle(6.0, 4.0, 0.0, "turtle3")

        # 编队参数（可调整）
        self.formation_distance = 1.5  # 乌龟间距离（米）
        self.angle_offset2 = -120      # turtle2相对于主乌龟的偏移角度（度）
        self.angle_offset3 = 120       # turtle3相对于主乌龟的偏移角度（度）
        
        # 控制参数（可调整）
        self.k_linear = 1.0    # 线速度比例系数
        self.k_angular = 4.0   # 角速度比例系数
        
        # 存储三只乌龟的位姿（位置和方向）
        self.leader_pose = Pose()   # 主乌龟(turtle1)位姿
        self.turtle2_pose = Pose()  # turtle2位姿
        self.turtle3_pose = Pose()  # turtle3位姿
        
        # 订阅位姿（每只乌龟的实时位置）
        rospy.Subscriber('/turtle1/pose', Pose, self.leader_cb)
        rospy.Subscriber('/turtle2/pose', Pose, self.turtle2_cb)
        rospy.Subscriber('/turtle3/pose', Pose, self.turtle3_cb)
        
        # 发布速度（控制乌龟移动）
        self.pub2 = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
        self.pub3 = rospy.Publisher('/turtle3/cmd_vel', Twist, queue_size=10)
        
        rospy.loginfo("✅ 3只乌龟生成成功！编队已启动")

    # 🔥 生成乌龟的函数（调用ROS官方服务）
    def spawn_turtle(self, x, y, theta, name):
        """在指定位置生成乌龟"""
        try:
            rospy.wait_for_service('/spawn', timeout=3)  # 等待服务可用
            spawn = rospy.ServiceProxy('/spawn', Spawn)
            spawn(x, y, theta, name)  # 调用服务生成乌龟
            rospy.loginfo(f"生成 {name} 成功！")
        except rospy.ROSException as e:
            rospy.logerr(f"生成 {name} 失败：{e}")

    # 位姿回调函数（存储乌龟位置）
    def leader_cb(self, msg): self.leader_pose = msg  # 主乌龟(turtle1)位姿回调
    def turtle2_cb(self, msg): self.turtle2_pose = msg  # turtle2位姿回调
    def turtle3_cb(self, msg): self.turtle3_pose = msg  # turtle3位姿回调

    # 编队控制核心算法
    def calculate_formation(self):
        """计算turtle2和turtle3的目标位置并控制移动"""
        # 获取主乌龟位置和方向
        x0, y0, theta = self.leader_pose.x, self.leader_pose.y, self.leader_pose.theta

        # 计算turtle2的目标位置（偏移角度-120°）
        angle2 = math.radians(self.angle_offset2) + theta  # 转换为弧度并计算实际角度
        x2 = x0 + self.formation_distance * math.cos(angle2)
        y2 = y0 + self.formation_distance * math.sin(angle2)

        # 计算turtle3的目标位置（偏移角度120°）
        angle3 = math.radians(self.angle_offset3) + theta
        x3 = x0 + self.formation_distance * math.cos(angle3)
        y3 = y0 + self.formation_distance * math.sin(angle3)

        # 控制turtle2移动到目标位置
        self.move_turtle(self.pub2, self.turtle2_pose, x2, y2)
        # 控制turtle3移动到目标位置
        self.move_turtle(self.pub3, self.turtle3_pose, x3, y3)

    # 定点移动控制函数
    def move_turtle(self, pub, pose, tx, ty):
        """控制单个乌龟移动到目标点"""
        twist = Twist()
        # 计算当前位置到目标点的偏移
        dx = tx - pose.x
        dy = ty - pose.y
        dist = math.hypot(dx, dy)  # 计算欧氏距离

        # 如果距离很近（小于0.1米），停止移动
        if dist < 0.1:
            pub.publish(twist)
            return

        # 计算目标方向角度
        target_theta = math.atan2(dy, dx)
        # 计算当前朝向与目标方向的误差（归一化到[-π, π]）
        angle_err = target_theta - pose.theta
        angle_err = math.atan2(math.sin(angle_err), math.cos(angle_err))

        # 计算速度指令（比例控制）
        twist.linear.x = self.k_linear * dist  # 线速度 = 比例系数 × 距离
        twist.angular.z = self.k_angular * angle_err  # 角速度 = 比例系数 × 角度误差

        pub.publish(twist)  # 发布速度指令

    def run(self):
        """主循环：持续执行编队控制"""
        rate = rospy.Rate(10)  # 10Hz控制频率
        while not rospy.is_shutdown():
            self.calculate_formation()  # 计算并控制编队
            rate.sleep()  # 保持控制频率

if __name__ == '__main__':
    try:
        node = TurtleFormation()
        node.run()
    except rospy.ROSInterruptException:
        pass
