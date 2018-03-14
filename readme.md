第一步：检查安装相关依赖包:
sudo easy_install pip
sudo pip install pytest==2.8.2
sudo pip install xlrd==0.9.4
sudo pip install requests==2.5.0
第二步：更改配置文件
创建配置文件conf/bdpconf.py
修改配置文件，特别注意：
a) BDP_HOST
   BDP_PORT
b) BDP_USER
   BDP_PASS
   BDP_DOMAIN
c) OPENDS_HOST
   OPENDS_PORT
   OPENDS_TOKEN

第五步：并发执行case
python main.py

ps: 模糊匹配执行case(case名称或文件名称:test_xxxx)：
python main.py -k test_xxxxx
