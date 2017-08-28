# beauty
[beauty](https://github.com/zhongjiajie/beauty)是图片网站[55156图库-高清套图](http://www.55156.com/gaoqingtaotu/)非官方的API。提供了更加清爽的套图浏览和下载接口，欢迎各位老司机使用，提issues或PR

## 安装依赖
项目根目录运行
```
pip install -r requirements.txt
```

## 快速入门
**以下命令均在项目根目录运行**
### 查看Usage及支持的套图类型
```
python beauty.py -h
```
* **Usage**： 得知项目主要有两个方法`scan`和`download`，其中`scan`是浏览指定种类和数量的封面图片（小图），`download`是下载指定种类和数量的套图（大图）。
* **Arguments**： 目前支持的套图种类，为`scan`和`download`方法的必填项
* **Options**： 参数的关键字及对应的解释

### 直接下载套图
```
# 下载秀人套图 默认数量为10 默认路径是./pic
python beauty.py download xiuren

# 下载秀人套图 指定数量为15 
python beauty.py download xiuren -n 15

# 下载秀人套图 指定路径为D:/
python beauty.py download xiuren -p D:/
```
完成后可在相应目录下看到下载结果

![image](https://github.com/zhongjiajie/beauty/raw/master/support_file/beauty_download.png)

### 先浏览小图，根据个人喜好（套图质量）下载对应的大图
```
# 浏览秀人套图 默认数量为10 默认路径是./pic/scan
python beauty.py scan xiuren

# 浏览秀人套图 指定数量为15
python beauty.py scan xiuren -n 15

# 浏览秀人套图 指定路径为D:/scan scan方法默认的图片会下载到指定（默认目录）的scan文件夹
python beauty.py download xiuren -p D:/
```
找到浏览套图文件夹`scan`，打开图片编辑器查看`scan`文件夹的图片

![image](https://github.com/zhongjiajie/beauty/raw/master/support_file/beauty_scan.png)

从上图中找到要完整下载的套图，运行下载命令
```
# -n参数要和scan方法的参数一样 -f参数列表内部不要留空格
python beauty.py download xiuren -n 10 -f [204774,204775,204832]
```
完成后可在相应目录下看到下载结果

![image](https://github.com/zhongjiajie/beauty/raw/master/support_file/beauty_scan_download.png)

## 注意事项
* 项目开发环境是Python2.7，如果发现项目不兼容的欢迎提[issues](https://github.com/zhongjiajie/beauty/issues/new) 

## TODO
* [x] 提供先浏览后选择下载的功能 finish at 20170827
* [ ] 下载图片失败后重试
* [ ] 重试失败后删除失效的图片，或者在单独的文件夹中备注下载失败的信息

## Change Log
* 20170828: 重写了repository，重命名为**beauty**，提供了更加人性化的api方法
* 20160220: 提供了re版本和BeautifulSoup版本的提取方法