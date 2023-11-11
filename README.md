# File Center <br /> 文件服务器  
基于 Python 的轻量化、图形美化文件分享服务器  

## **功能/使用说明**  
- 安装/运行  
  - 进入待分享文件夹：`cd /path/to/dir`  
  - 克隆本存储库：`git clone https://github.com/Geraniol/FileServer.git`  
  - 运行：`python3 fileserver.py`  
  - 从浏览器访问：`http://ip:port/`  
- 快速分享  
  - 在 `~/.bashrc` 或 `~/.zshrc` 中添加别名：`alias fs='python3 /path/to/fileserver.py'`  
- 默认挂载至 `0.0.0.0:80`  
  - 可在 `fileserver.py` 中修改  
  - 修改为 `127.0.0.1`：仅本机可访问  

## **参数**  
- 程序 `fileserver.py` 中可自定义参数  
- 内部参数  
  - `SERVER_NAME` = `Shiro-chan` 服务器名称  
  - `FILTER` = `["MP4", "MOV", "MKV"]` 文件过滤器  
- 外部参数  
  - `PATH_INDEX` = `./lib/index.html` 网页框架模版之文件路径  
  - `PATH_SAMPLE` = `./lib/sample.html` 网页模块模版之文件路径  
  - `PATH_ROOT` = `..` 服务器主目录路径  

## **区别**  
- 与 `python3 -m http.server`  
  - 美化的的网页界面  
- 与 `beautify-http-server`  
  - 提供安全权限控制  
  - 尚不支持上传文件  
- 与 `Apache`、`Nginx` 或 `Flask` 等  
  - 无需安装依赖、框架、配置服务器  

## **问题**  
- 提示权限不足  
  - 更改所用端口（1024+）  
  - 使用管理员权限运行：`sudo python3 fileserver.py`  

## **改进方向**  
- 支持文件夹树状图搜索  
- 支持修改模版（`HTML`、`CSS`）  
- 支持自定义输出、端口等参数  
- 代码待优化  
- 优化项目目录结构  
- 支持添加为网页应用  
- 提供更多文件过滤选项  
- 解决 `gethostbyname_ex` 在部分环境中的异常  
- 支持 `HTTPS` 协议  
- 支持密码访问（实验性功能）  