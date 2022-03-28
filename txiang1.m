figure;
a=xlsread('C:\Users\Administrator\Desktop\机械臂角度仿真数据\画图.xlsx','sheet1');
x1=a(:,1);
y1=a(:,2);
z1=a(:,3);
Q=plot3(x1,y1,z1,'k');
hold on
x2=a(:,1);
y2=a(:,2);
z2=a(:,4);
Y=plot3(x2,y2,z2,'p');
set(Y,'LineWidth',1.5); 
xlabel('Deviation angle');
ylabel('distance');
zlabel('angle of α0');
set(Q,'LineWidth',1.5); 
set(gca,'FontSize',10);
legend('Theoretical angle','Actual angle');
title('Chassis angle scatter plot')