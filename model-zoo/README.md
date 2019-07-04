# 模型动物园

## 模型
> 这里的模型都使用数据卷的方式打包后提交到Docker Hub上了。
* [压板开关：platen-switch](platen-switch/)
    > 检测压板开关的状态
* [安全帽：helmet](helmet/)
    > 检测戴着的安全帽

## 部署模型
1. 下载模型

```bash
sudo docker pull gouchicao/darknet-model-<name>:latest
<name>指上面模型的名字

例如：
$ sudo docker pull gouchicao/darknet-model-platen-switch:latest
$ sudo docker pull gouchicao/darknet-model-helmet:latest
```

2. 创建存储卷
```bash
$ sudo docker run --name darknet-model-platen-switch --volume /model \
    gouchicao/darknet-model-platen-switch:latest
```

3. 使用darknet-serving部署模型
```bash
$ sudo docker run --runtime=nvidia -it --name=darknet-serving-platen-switch -p 7713:7713 \
    --volumes-from darknet-model-platen-switch \
    gouchicao/darknet-serving:latest-gpu
```

## 创建自己的模型
```bash
使用您本机的绝对路径设置project_dir
$ project_dir=/home/wjunjian/github/gouchicao/darknet/model-zoo/platen-switch

设置您的模型名
$ darknet_model_name=darknet-model-platen-switch
```

1. 运行darknet容器（GPU）
```bash
$ sudo docker run --runtime=nvidia -it --rm --name=darknet \
    --volume=$project_dir:/darknet/project \
    gouchicao/darknet:latest-gpu
```

2. 训练模型
```bash
在容器内运行
$ mkdir backup
$ ../darknet detector train cfg/voc.data cfg/yolov3.cfg ../darknet53.conv.74
```

3. 生成模型部署数据
```bash
$ python3 generate_model_deploy_data.py -d $project_dir
```

4. 把生成的模型部署数据打包成数据卷镜像
```bash
$ sudo docker run -d --name $darknet_model_name alpine
$ cd $project_dir
$ sudo docker cp model/ $darknet_model_name:/
$ sudo docker commit -a 'wang-junjian@qq.com' -m 'darknet model [platen-switch recognition]' \
    $darknet_model_name gouchicao/$darknet_model_name:latest
$ sudo docker rmi darknet-model-platen-switch
```
