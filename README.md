A log collection project
=======================

收集应用服务器的日志到中心存储服务器

功能  
1:重启自动同步未同步的数据  
2:基于SCP,支持压缩，和限速等  
3:自动发现新文件和子文件夹  
4:同步完成自动删除老日志  

不支持  
1:同一个文件断点续传

----INSTALL-----  
python setup.py install

server  
1:cp broom/skel/broom.conf /etc/broom.conf  
2:安装xinetd  
3:cp broom/skel/broomd /etc/xinetd/broomd  
4:重启xinetd  
5:netstat -anlpt|grep 9999  
  
client  
1: cp broom/skel/broom.conf /etc/broom.conf  
2: 订制自己的broom.conf  
----USEAGE-----  
日志文件命名请遵循如下规则  
custom20160223 按日期切割  
custom2016022301 按小时切割  
broom -c /etc/broom.conf  
