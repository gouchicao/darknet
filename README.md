<div align="center">
  <img src="http://pjreddie.com/media/files/darknet-black-small.png">
</div>

-----------------

## 构建Darknet的Docker镜像
* 下载Darknet的源代码和基于Imagenet的预训练模型darknet53
```shell
./get_darknet.sh
```

* 构建Docker镜像
```shell
sudo docker build -t darknet .
```

* 测试
```shell
sudo docker run --runtime=nvidia --rm darknet:latest ./darknet

usage: ./darknet <function>
```

* 运行Darknet容器
```shell
sudo docker run --runtime=nvidia -it darknet:latest
```
