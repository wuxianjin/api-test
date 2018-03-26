第一步：检查安装相关依赖包:
pip install pytest==2.8.2
pip install xlrd==0.9.4
pip install requests==2.5.0
第二步：更改配置文件
创建配置文件conf/apiconf.py
修改配置文件，特别注意：
a) API_HOST
   API_PORT
b) API_USER
   API_PASS

c) OPENDS_HOST
   OPENDS_PORT
   OPENDS_TOKEN

第五步：并发执行case
python main.py

python main.py -k test_xxxxx
