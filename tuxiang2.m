figure;
a=xlsread('C:\Users\Administrator\Desktop\��е�۽Ƕȷ�������\��ͼ.xlsx','sheet1');
x1=a(:,1);
y1=a(:,2);
z1=a(:,5);
Q=plot3(x1,y1,z1,'k');
hold on
x2=a(:,1);
y2=a(:,2);
z2=a(:,6);
Y=plot3(x2,y2,z2,'p');
set(Y,'LineWidth',1.5); 
xlabel('Deviation angle');
ylabel('distance');
zlabel('angle of ��1');
set(Q,'LineWidth',1.5); 
set(gca,'FontSize',10);
legend('Theoretical angle','Actual angle');
title('Arm angle scatter plot')