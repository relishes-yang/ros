# ROS 学习与作业仓库
本仓库用于存放ROS相关课程作业与功能包Demo。
## 目录结构 📂

ros/ # 等价于 ROS 工作空间的 src/ 目录├── posvel_control/ # 位置 - 速度控制功能包（自定义消息 + Python 节点）├── turtle_formation/ # 三只乌龟键盘控制 + 自动三角形编队实验└── new_demo_pkg/ # 未来新增功能包示例


## 已包含功能包 📦

| 功能包名称 | 功能描述 | 运行命令 |
|-----------|----------|----------|
| [posvel_control](./posvel_control/) | 自定义位置-速度消息类型，实现 Python 节点通信 | `rosrun posvel_control <your_script.py>` |
| [turtle_formation](./turtle_formation/) | 1 只领航龟（键盘控制）+ 2 只跟随龟，保持三角形编队 | `roslaunch turtle_formation turtle_formation.launch` |

## 快速开始 🚀

### 1. 克隆仓库
```bash
git clone https://github.com/relishes-yang/ros.git
```
### 2. 编译与环境配置
将仓库放入你的 ROS 工作空间 src/ 目录下：
假设你的工作空间为 ~/catkin_ws
```
mv ros ~/catkin_ws/src/
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```

### 3. 运行 Demo（以乌龟编队为例）
```
roslaunch turtle_formation turtle_formation.launch
```


# 📝 他人操作指南（直接复制粘贴即可）
### 1. 创建ROS工作空间（如果尚未创建）
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src

### 2. 克隆你的仓库（SSH方式，无需密码）
git clone git@github.com:relishes-yang/ros_posvel_control.git

### 3. 重命名目录（ROS包名必须为 posvel_control）
mv ros_posvel_control posvel_control

### 4. 返回工作空间根目录
cd ~/catkin_ws

### 5. 安装ROS依赖（关键！）
rosdep install --from-paths src --ignore-src -r -y

### 6. 编译ROS包
catkin_make

### 7. 运行节点（在source后）
source devel/setup.bash

rosrun posvel_control posvel_publisher.py  # 终端1

rosrun posvel_control posvel_subscriber.py  # 终端2

# 🛠 四、常见问题解决（他人可能遇到的）

### 问题1：rosrun: command not found
原因：未source环境
解决：
source ~/catkin_ws/devel/setup.bash

### 问题2：Package not found: posvel_control
原因：未重命名目录
解决：
cd ~/catkin_ws/src
mv ros_posvel_control posvel_control
catkin_make  # 重新编译

### 问题3：ImportError: No module named 'posvel_control'
原因：未安装依赖
解决：
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src -r -y
catkin_make
