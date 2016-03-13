# crawler-beauty
</p>应舍友要求，帮其爬取某个图片分享网站的小黄图</p>
<br/>
<B>1.运行前操作</B>
<p>请在E盘创建一个目录Photo，即路径为：E:\Photo</p>
<p>当然路径可以修改，具体修改方式在程序的注释中已说明</p>
<p>为什么不在程序中自动生成文件夹？------- 我只是怕你不知道哪个是你要的小黄图而已，自己新建的文件夹你总会记得吧</p>
<br/>
<B>2.程序完善时间列表</B>
<p>[16.02.23]  发现程序xiuren_useful.py爬到第十五个秀人图片时产生错误，正在研究为什么会有这样的错误产生</p>
<p>[16.03.13]  修正了正则表达式上的错误，实现了全部的爬取，正在验证是否还存在问题</p>
<br/>
<B>3.下载完后的目录情况（其中****视网站更新情况有所不同）</B>
<div class="cnblogs_Highlighter">
<pre class="brush:html;gutter:true;">E:
  /Photo
    /[秀人网]********
           _1.jpg
           _2.jpg
           ......
           10.jpg
           ......
           n.jpg
    /[秀人网]********
           _1.jpg
           _2.jpg
           ......
           10.jpg
           ......
           n.jpg
    .................
</pre>
</div>
<p>　　</p>

<B>4.截图目录如下</B>
<p>![image](https://github.com/zhongjiajie/crawler-beauty/raw/master/SampleResult.jpg)</p>
