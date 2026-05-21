%% 实验3：Puma560逆运动学轨迹仿真
% 适配：MATLAB 2018a + Peter Corke Robotics Toolbox 9.x
clc;                  % 清空命令行窗口
clear;                % 清空工作区所有变量
close all;            % 关闭所有绘图窗口
%% ===================== 1. 定义【垂直圆形】轨迹（仅修改这里！） =====================
N = (0:0.5:100)';     % 生成轨迹采样点序列，步长0.5
center = [0.5 0 0.5]; % 垂直圆圆心坐标(X,Y,Z)，抬高Z避免碰撞
radius = 0.15;         % 垂直圆半径
theta = ( N / N(end) ) * 2*pi;  % 计算轨迹角度，范围0~2π

% ? 核心修改：垂直圆（XZ平面）Y固定，X和Z变化
points = ( center + radius*[cos(theta) zeros(size(theta)) sin(theta)] )';  

% 绘制目标轨迹
figure('Name','目标轨迹');  % 新建图形窗口
plot3(points(1,:), points(2,:), points(3,:), 'r', 'LineWidth',1.5);  % 绘制3D圆形轨迹
hold on;              % 保持绘图窗口
grid on;              % 显示网格
axis equal;           % 坐标轴等比例显示
view(3);              % 切换3D视角
xlabel('X/m');        % X轴标签
ylabel('Y/m');        % Y轴标签
zlabel('Z/m');        % Z轴标签
title('目标垂直圆形轨迹'); % 图形标题

%% ===================== 2. 加载Puma560机器人模型 =====================
mdl_puma560;          % 调用工具箱，加载Puma560机械臂模型
disp('Puma560机械臂模型加载完成！');  % 命令行打印提示信息

%% ===================== 3. 逆运动学求解 =====================
q = zeros(length(theta), 6);  % 初始化6关节角度矩阵
q0 = qz;                      % 设置机械臂初始关节角（零位姿态）

for i = 1:length(theta)       % 循环遍历所有轨迹点
    T = transl(points(:,i)) * trotz(0);  % 构建末端位姿矩阵(位置+姿态)
    % 逆运动学求解，获取当前轨迹点的关节角
    q(i,:) = p560.ikine(T, q0, 'mask', [1 1 1 0 0 0], 'ilimit', 1500, 'tol', 1e-6);  
    q0 = q(i,:);              % 更新初始关节角，保证运动平滑
end
disp('逆运动学求解完成！');   % 命令行打印提示信息

%% ===================== 4. 正运动学验证 =====================
actual_points = zeros(3, length(theta));  % 初始化实际轨迹坐标矩阵
for i = 1:length(theta)                   % 循环遍历所有关节角
    T_actual = p560.fkine(q(i,:));         % 正运动学计算末端位姿
    actual_points(:,i) = transl(T_actual); % 提取实际轨迹坐标
end

% 轨迹对比绘图
figure('Name','轨迹对比');  % 新建图形窗口
plot3(points(1,:), points(2,:), points(3,:), 'g--', 'LineWidth',1.5); hold on; % 绘制目标轨迹
plot3(actual_points(1,:), actual_points(2,:), actual_points(3,:), 'b', 'LineWidth',1.5); % 绘制实际轨迹
grid on; axis equal; view(3); % 网格、等比例、3D视角
xlabel('X/m'); ylabel('Y/m'); zlabel('Z/m'); % 坐标轴标签
legend('目标轨迹','实际轨迹','Location','best'); % 图例
title('目标轨迹与机械臂实际末端轨迹对比'); % 标题

%% ===================== 5. 机械臂运动动画 =====================
figure('Name','Puma560轨迹仿真'); % 新建动画窗口
plot3(points(1,:), points(2,:), points(3,:), 'r--', 'LineWidth',1.5); hold on; % 绘制目标轨迹
grid on; axis equal; view(3); % 网格、等比例、3D视角
xlabel('X/m'); ylabel('Y/m'); zlabel('Z/m'); % 坐标轴标签
title('Puma560跟踪垂直圆形轨迹仿真'); % 标题
p560.plot(q, 'trail', 'b', 'delay', 0.02); % 播放机械臂运动动画
