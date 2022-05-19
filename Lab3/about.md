## 如何构建本项目？

PB19030888 张舒恒

### flask

> [Flask web development,one drop at a time](https://flask.palletsprojects.com)

​	`flask`是一个优秀的`web`框架，依赖 [Jinja](https://www.palletsprojects.com/p/jinja/) 模板引擎和 [Werkzeug](https://www.palletsprojects.com/p/werkzeug/) `WSGI` 套件。

​	我们可以调用`Flask`创建并运行`app`，`@app.route` `python`装饰器可以将函数绑定到`url`，通过判断`HTTP`消息方法可以选择返回静态页面或者进行页面重定向。

```python
from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    return redirect('/')

if __name__ == '__main__':
    app.run()
```

### jinja

> [Jinja2 2.7 documentation](http://docs.jinkan.org/docs/jinja2/)

​	`Jinja2` 是一个仿照 `Django` 模板的 `Python` 模板语言，我们可以用它来实现`HTML`模板继承和前后端数据交互。由于`flask`依赖`jinja`，所以如果你也是`flask`框架则可以直接使用`jinja`，否则需要下载并引入。

```bash
sudo pip install Jinja2
```

```python
from jinja2 import Template
```

#### `HTML`模板继承

​	模板文件`layout.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <!--Add your CSS source here-->
    <!--Add your JavaScript source here-->
</head>
<body>
    <div>
    	{% block content %}
        {% endblock %}
	</div>
</body>
</html>
```

​	继承`layout.html`

```html
{% extends 'layout.html' %}
{% block content %}
	<!--Add your HTML block here-->
{% endblock %}
```

#### 前后端数据交互

​	以user_list为例，后端返回静态页面时将数据data_list传给前端，前端利用迭代器从data_list容器中取出元素。

```html
{% for obj in data_list %}
<tr>
    <td>{{ obj.User_Name }}</td>
    <td>{{ obj.User_Password }}</td>
    <td>

        <a class="btn btn-primary btn-sm" href="/user/edit/{{ obj.User_Name }}">
            edit<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
        </a>

        <a class="btn btn-danger btn-sm" href="/user/delete/{{ obj.User_Name }}">
            delete<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
        </a>
    </td>
</tr>
{% endfor %}
```

```python
return render_template('user_list.html', data_list=data_list)
```

​	前端设置input标签获取用户输入，后端利用request.form.get获取input。

```html
<form method="post">
	<div class="form-group">
        <label for="User_Name">User_Name</label>
        <input type="text" class="form-control" id="User_Name" placeholder="User_Name" name="User_Name">
    </div>
    <div class="form-group">
        <label for="User_Password">User_Password</label>
        <input type="password" class="form-control" id="User_Password" placeholder="User_Password"
             name="User_Password">
    </div>
</form>
```

```python
username = request.form.get("User_Name")
password = request.form.get("User_Password")
```

### pymysql

> [PyMySQL · PyPI](https://pypi.org/project/PyMySQL/)

​	`pymysql`提供了从`Python`连接到`MySQL`数据库服务器的接口，并支持原生的`sql`语句增删改查。

​	连接数据库需要指定服务器`IP`，端口`MySQL`默认`3306`，用户名与密码，以及编码和数据库名；接着就是获取游标，执行`sql`语句；最后一定不要忘了提交和关闭。

```python
conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd="1234", charset='utf8', db='bank')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
sql = "insert into user(User_Name,User_Password) values(%s,%s)"
cursor.execute(sql, [username, password])
datalist = cursor.fetchall()
conn.commit()
cursor.close()
conn.close()
```

### bootstrap.css

> [Bootstrap · The most popular HTML, CSS, and JS library in the world.](https://getbootstrap.com/)

#### 引入

​	第一步我们要引入`bootstrap.css`，笔者写这篇文档的时候不巧这段时间`jedelivr`挂了，于是改用[cdnjs](https://cdnjs.com/)。

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.2.0-beta1/css/bootstrap.min.css">
```

#### 按钮

​	`btn-primary`和`btn-lg`分别是按钮的样式和尺寸，可以自定义

```html
<a class="btn btn-primary btn-lg" href="/login" role="button">login</a>
```

#### 导航栏

​	`class="navbar-header"`和`class="collapse navbar-collapse"`分别是导航栏的栏头和栏目，这里我设置了标题`Bank Management System`和选项`Department`，`User`等等。

```html
<nav class="navbar navbar-default">
    <div class="container">
        <div class="navbar-header">
            <a class="navbar-brand" href="/"> Bank Management System </a>
        </div>
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
            <ul class="nav navbar-nav">
                <li><a href="/department/list">Department</a></li>
                <li><a href="/user/list">User</a></li>
                ...
            </ul>
          
        </div>
    </div>
</nav>
```

#### 表单

​	`bootstrap`的表单样式简洁美观，只需设置`class="table table-bordered"`。

```html
<!-- Table -->
<table class="table table-bordered">
    <thead>
    <tr>
        <th>User_Name</th>
        <th>User_Password</th>
        <th>Operating</th>
    </tr>
    </thead>
    <tbody>
    {% for obj in queryset %}
        <tr>
            <th>{{ obj.User_Name }}</th>
            <td>{{ obj.User_Password }}</td>
            <td>
                <a class="btn btn-primary btn-xs" href="/user/{{ obj.id }}/edit/">编辑</a>
                <a class="btn btn-danger btn-xs" href="/user/delete/?nid={{ obj.id }}">删除</a>
            </td>
        </tr>
    {% endfor %}
    </tbody>
</table>
```

#### 搜索框

​	搜索栏需要注意的问题是`CSS`布局，这里可以在盒子中设置靠右排列，设置好间距。另外不要忘了外层加上`post`方法。

```html
<div style="float: right;width: 800px;">
    <form method="post">
        <div style="float: right;width: 70px;">
            <input type="submit" value="Search" class="btn btn-success">
        </div>

        <div style="float: right;width: 10px;">
            &nbsp
        </div>

        <div style="float: right;width: 100px;">
            <div class="input-group">
                <input type="text" style="border-radius: 5px" name="Client_Address" class="form-control" placeholder="Client_Address">
            </div>
        </div>

        <div style="float: right;width: 20px;">
            <div style="position: relative; top: 5px; left: 6px">
                &
            </div>
        </div>

        <div style="float: right;width: 100px;">
            <div class="input-group">
                <input type="text" style="border-radius: 5px" name="Client_Tel" class="form-control" placeholder="Client_Tel">
            </div>
        </div>
    </form>
</div>
```

#### 下拉选择框

​	这个组件比较简单，设置好`select`和`option`标签即可。

```html
<div class="form-group">
    <label>Account_Type</label>
    <select class="form-control" name="Account_Type">
        <option value="Saving">Saving</option>
        <option value="Checking">Checking</option>
    </select>
</div>
```

#### 图标

​	`bootstrap.css`的图标库不算丰富，但本项目中用到的图标不多，这里列举了增加，修改，删除，列表的图标。

```html
<span class="glyphicon glyphicon-plus-sign" aria-hidden="true"></span>
<span class="glyphicon glyphicon-th-list" aria-hidden="true"></span>
<span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
```

### 自定义CSS

#### 卡片

​	在`CSS`中设置盒子的长宽，位置，边缘阴影效果等等。

```css
<style>
    .card {
        width: 630px;
        height: 220px;
        border: 1px solid #dddddd;
        border-radius: 5px;
        box-shadow: 5px 5px 20px #aaa;

        margin-left: auto;
        margin-right: auto;
        margin-top: 100px;
        padding: 20px 40px;
    }
</style>
```

#### 背景

​	这里样式设置为覆盖填充整个页面，置于底层，图片使用的是谷歌主题中的一张高清图，并且放在了我自己的图床上。

```css
<style>
body {
    background-size:cover;
    background: #CCCCCC url("https://s1.328888.xyz/2022/05/12/HPpNZ.png") no-repeat fixed center center;
}
</style>
```

### bootstrap.js

> [JavaScript · Bootstrap](https://getbootstrap.com/docs/3.3/javascript/)

#### 引入

​	由于`bootstrap.js`依赖于`jquery.js`，所以在引入`bootstrap.js`之前还需要引入`jquery.js`，并且由于`JavaScript`的语言特性，顺序不能调换，否则会出错。

```html
<script src="/static/js/jquery-3.6.0.min.js"></script>
<script src="/static/plugins/bootstrap-3.4.1/js/bootstrap.js"></script>
```

#### 错误响应

​	在这个项目中唯一用到`JavaScript`的功能大概就是响应用户的错误操作，可以先预置一个容器，然后`JavaScript`从后端检测错误信息，将`HTML`代码插入容器中。

```js
<div id="error1"></div>
<script>
    const error1_html = "<div class=\"alert alert-danger alert-dismissible\" role=\"alert\">\n" +
        "            <button type=\"button\" class=\"close\" data-dismiss=\"alert\" aria-label=\"Close\"><span\n" +
        "                    aria-hidden=\"true\">&times;</span></button>\n" +
        "            <strong>Error!</strong> {{error1}} " +
        "        </div>";
    const error1 = '{{error1}}';
    if (error1)
        document.getElementById('error1').innerHTML = error1_html;
</script>
```

### 部署

​	笔者尝试了在`vercel`自动化部署，结果失败了，于是改用自己的云服务器部署到自己的子域名下。在宝塔面板的`python`项目管理器中新建`flask`项目，安装相应的环境依赖，通过`FTP`上传源码以及图片等资源，启动项目，设置域名映射到自己的域名下。

​	此时还不能使用因为数据库还没有连接，好在宝塔提供了数据库管理，我们可以新建数据库，并通过`sql`语句导入本地的数据库，`sql`语句或者`CSV`格式导入本地数据库的数据。

```bash
pip freeze >requirements.txt
```

![D1n2J.png](https://s1.328888.xyz/2022/05/19/D1n2J.png)

### 其他开源库

> [Spacing.js](https://spacingjs.com/)

一个 `JavaScript` 实用程序，用于测量网页上元素之间的间距。

> [SweetAlert2](https://www.sweetalert2.cn/)

一个美观，响应，可定制，可访问（`WAI-ARIA`）替代`JAVASCRIPT`的弹出框，零依赖。

> [WebGradients.com💎](https://webgradients.com/)

非常好看的渐变色生成网站，可导出`SVG`和`CSS`，开箱即用。

### 鸣谢

​	`pycharm`-后端+`webstorm`-前端+`datagrip`-数据库
