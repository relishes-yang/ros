# 📂 ROS学习与作业仓库
本仓库用于存放ROS1 (Noetic) 课程作业、功能包Demo与实验源码，包含机器人坐标变换、海龟仿真、话题通信等实战项目，遵循ROS标准工作空间规范，可直接编译运行。

## 📁 仓库结构
ros/ # 仓库根目录 (ROS 功能包集合)

├── posvel_control/ # 自定义话题通信功能包

├── turtle_formation/ # 多海龟编队控制功能包

├── robot_dh_tf/ # 六自由度机器人 DH 参数 TF 发布

└── README.md # 仓库说明文档


## 📦 已包含功能包
| 功能包名称 | 功能描述 | 运行命令 |
| :--- | :--- | :--- |
| [posvel_control](./posvel_control/) | 自定义位置-速度消息类型，实现ROS话题发布/订阅通信 | `rosrun posvel_control posvel_publisher.py`<br>`rosrun posvel_control posvel_subscriber.py` |
| [turtle_formation](./turtle_formation/) | 1只领航龟(键盘控制) + 2只跟随龟，实现三角形自动编队 | `roslaunch turtle_formation turtle_formation.launch` |
| [robot_dh_tf](./robot_dh_tf/) | 六自由度机器人改进DH参数计算，TF坐标变换广播+RViz可视化 | `rosrun robot_dh_tf robot_tf_publisher.py`<br>`rviz` |

## 🚀 快速开始
### 1. 准备ROS工作空间
```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
```

### 2. 克隆仓库
```bash
git clone https://github.com/relishes-yang/ros.git
```

### 3. 安装依赖并编译
```
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src -r -y
catkin_make
source devel/setup.bash
```

### 4. 配置环境永久生效（可选）
```
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## 🎯 功能包运行示例
### 示例 1：位置 - 速度话题通信
```
# 终端1
rosrun posvel_control posvel_publisher.py
# 终端2
rosrun posvel_control posvel_subscriber.py
```
### 示例 2：多海龟自动编队
```
roslaunch turtle_formation turtle_formation.launch
```

### 示例 3：机器人 DH 参数 TF 可视化
```
# 终端1 启动TF发布节点
rosrun robot_dh_tf robot_tf_publisher.py
# 终端2 打开RViz可视化
rviz
```



# 🛠 四、常见问题解决（他人可能遇到的）

### 问题1：rosrun: command not found
原因：未source环境

解决：
```
source ~/catkin_ws/devel/setup.bash
```

### 问题2：Package not found
原因：未编译工作空间 / 环境未生效

解决：
```
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

### 问题3：Python 脚本无法运行
原因：脚本无执行权限

解决：
```
chmod +x ~/catkin_ws/src/ros/功能包名/scripts/xxx.py
```
