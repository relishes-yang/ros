# 📂ROS学习与作业仓库
本仓库用于存放ROS相关课程作业与功能包Demo。

## 已包含功能包 📦

| 功能包名称 | 功能描述 | 运行命令 |
|-----------|----------|----------|
| [posvel_control](./posvel_control/) | 自定义位置-速度消息类型，实现 Python 节点通信 | `rosrun posvel_control posvel_publisher.py  # 终端1             rosrun posvel_control posvel_subscriber.py  # 终端2`  |
| [turtle_formation](./turtle_formation/) | 1 只领航龟（键盘控制）+ 2 只跟随龟，保持三角形编队 | `roslaunch turtle_formation turtle_formation.launch` |

## 快速开始 🚀

### 1. 创建ROS工作空间（如果尚未创建）
```mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
```

### 2. 克隆仓库
```bash
git clone https://github.com/relishes-yang/ros.git
```
### 3. 重命名目录(可选)（你取个名字XXXX）
```
mv ros_posvel_control XXXX
```

### 4. 返回工作空间根目录
```
cd ~/catkin_ws
```

### 5. 安装ROS依赖（关键！）
```
rosdep install --from-paths src --ignore-src -r -y
```
### 6. 编译与环境配置
```
catkin_make
source devel/setup.bash
(或者)
source ~/catkin_ws/devel/setup.bash
```

### 7. 运行节点（在source后）
```
示例：发布者-订阅者
source devel/setup.bash
rosrun posvel_control posvel_publisher.py  # 终端1
rosrun posvel_control posvel_subscriber.py  # 终端2
示例：（以乌龟编队为例）
roslaunch turtle_formation（包） turtle_formation.launch（启动文件）
```


# 🛠 四、常见问题解决（他人可能遇到的）

### 问题1：rosrun: command not found
原因：未source环境

解决：
```
source ~/catkin_ws/devel/setup.bash
```

### 问题2：Package not found: posvel_control
原因：未重命名目录

解决：
```
cd ~/catkin_ws/src
mv github的功能包 posvel_control
catkin_make  # 重新编译
```

### 问题3：ImportError: No module named 'posvel_control'
原因：未安装依赖

解决：
```
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src -r -y
catkin_make
```
