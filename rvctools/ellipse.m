%% 实验3：Puma560逆运动学轨迹仿真
% 适配：MATLAB 2018a + Peter Corke Robotics Toolbox 9.x
clc; clear; close all;  

%% ===================== 1. 定义目标椭圆形轨迹（仅修改这里！） =====================
N = (0:0.5:100)';  
center = [0.5 0 0.3];  
% 椭圆参数：X轴长半径，Y轴短半径
rx = 0.3;   % 椭圆X方向半径
ry = 0.15;  % 椭圆Y方向半径
theta = ( N / N(end) ) * 2*pi;  

% 生成椭圆轨迹（核心修改行）
points = ( center + [rx*cos(theta) ry*sin(theta) zeros(size(theta))] )';  

% 绘制目标轨迹
figure('Name','目标轨迹');
plot3(points(1,:), points(2,:), points(3,:), 'r', 'LineWidth',1.5);
hold on; grid on; axis equal; view(3);
xlabel('X/m'); ylabel('Y/m'); zlabel('Z/m');
title('目标椭圆形轨迹');

%% ===================== 2. 加载Puma560机器人模型 =====================
mdl_puma560;  
disp('Puma560机械臂模型加载完成！');

%% ===================== 3. 逆运动学求解（已修复求解失败bug） =====================
q = zeros(length(theta), 6);  
q0 = qz;  % 初始关节角（零位）

for i = 1:length(theta)
    % 修复1：更换为Puma560兼容的姿态（核心修复点）
    T = transl(points(:,i)) * troty(pi);  

    % 修复2：增加求解参数，提升成功率，杜绝报错
    % mask=[1 1 1 0 0 0]：只跟踪位置，忽略姿态（轨迹专用）
    q(i,:) = p560.ikine(T, q0, 'mask', [1 1 1 0 0 0], 'ilimit', 1500, 'tol', 1e-6);  
    q0 = q(i,:);  
end
disp('逆运动学求解完成！');

%% ===================== 4. 正运动学验证 =====================
actual_points = zeros(3, length(theta));  
for i = 1:length(theta)
    T_actual = p560.fkine(q(i,:));  
    actual_points(:,i) = transl(T_actual);  
end

% 轨迹对比
figure('Name','轨迹对比');
plot3(points(1,:), points(2,:), points(3,:), 'r--', 'LineWidth',1.5); hold on;
plot3(actual_points(1,:), actual_points(2,:), actual_points(3,:), 'b', 'LineWidth',1.5);
grid on; axis equal; view(3);
xlabel('X/m'); ylabel('Y/m'); zlabel('Z/m');
legend('目标轨迹','实际轨迹','Location','best');
title('目标轨迹与机械臂实际末端轨迹对比');

%% ===================== 5. 机械臂运动动画 =====================
figure('Name','Puma560轨迹仿真');
plot3(points(1,:), points(2,:), points(3,:), 'r--', 'LineWidth',1.5); hold on;
grid on; axis equal; view(3);
xlabel('X/m'); ylabel('Y/m'); zlabel('Z/m');
title('Puma560跟踪椭圆形轨迹仿真');
p560.plot(q, 'trail', 'b', 'delay', 0.02);