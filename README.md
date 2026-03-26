
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
