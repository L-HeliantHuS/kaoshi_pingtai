采用Django2.1.7 + Sqlite3 + Python3 + Bootstrap4 + Jquery。

进入后台将要考试的数据放入, 前端即可做题, 并分析题目, 进行错误提示.

run.py  一键启动脚本. (需要按需求更改.  默认以只能127.0.0.1访问.

强烈推荐!!!! 内网穿透echosite: https://www.echosite.cn/    大约2元一个月.

批量创建用户.  /create_users
    可以批量创建用户, 请在manage.py同级目录下创建一个users.csv, 第一列第一行写username, 第二列第一行写password。(已经写好了.
    然后分别在两列里面写入对应的用户名和密码.  (推荐使用 用户名不一样， 密码一样.  密码里面不可以包含用户名.
    username    password
    test1       password123.com
    test2       password123.com
    test3       password123.com
    test4       password123.com
    test5       password123.com
    test6       password123.com
    test7       password123.com
    以上内容是示例.   请在excel中编辑.

