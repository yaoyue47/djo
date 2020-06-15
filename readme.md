# 项目环境：

python：3.8

django：3.02





# 版本信息

V1.0 正式发布版

v2.0 正式发布版



# 如何部署？

按要求安装部署django，uwsgi，nginx后（过程自行参考网络教程）



需要对于本GitHub项目文件中进行如下修改：

* /djo/djo/settings.py文件中：

  `DEBUG=True` 改为 `DEBUG=False`

  关闭debug模式，使得项目出错时不会显示错误信息，且django不再接受静态文件的请求工作（将由nginx代为管理）

* /djo/djo/settings.py文件中：

  ```
  ALLOWED_HOSTS = [
      '127.0.0.1',
  ]
  ```

  添加自己的域名

* /djo/djo/settings.py文件中：

  ``` 
  EMAIL_HOST_USER = '2359240697@qq.com'
  EMAIL_HOST_PASSWORD = ''
  ```

  替换为自己的邮箱账号和邮箱授权码以使用发送邮箱功能

* /djo/shumeipai/module/captcha.py 文件中

  ```
  self.font_path = 'msyhbd.ttc'
  ```

  修改为部署系统中任意一个字体。linux系统需要使用绝对路径，否则index界面中的验证码功能将不可用。



以上修改完成后，命令行输入：

```
python manage.py collectstatic
```

收集静态文件

```
uwsgi --reload uwsgi.pid
```

重启uwsgi



至此完成部署。