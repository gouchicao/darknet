<div align="center">
  <img src="http://pjreddie.com/media/files/darknet-black-small.png">
</div>

-----------------

## [模型动物园](model-zoo)

## 获得darknet镜像（GPU）
> 有两种方式：拉取hub.docker上的镜像和自己在本地生成镜像。

### 1. 拉取darknet镜像
```bash
$ sudo docker pull gouchicao/darknet:latest-gpu
```

### 2. 构建darknet镜像
* 下载Darknet的源代码和基于Imagenet的预训练模型darknet53
```bash
$ ./get_darknet.sh
```

* 构建镜像
```bash
$ sudo docker build -t gouchicao/darknet:latest-gpu .
```

* 测试
```bash
$ sudo docker run --runtime=nvidia --rm gouchicao/darknet:latest-gpu ./darknet
usage: ./darknet <function>
```

## 运行darknet容器（GPU）
* 使用你的工程绝对路径替换$project_dir
```bash
$ sudo docker run --runtime=nvidia -it --name=darknet \
    --volume=$project_dir:/darknet/project \
    darknet:latest-gpu
```

## 训练自己的模型
* 工程目录结构
    ```
    project   　　　　　　　　　　工程目录
    ├── backup　　　　　　　　　　存储模型训练时权重值
    │   └── yolov3_final.weights 训练出来的模型
    ├── cfg　　　　　　　　　　　　配置目录
    │   ├── train.txt　　　　　　存储用于训练的图像路径
    │   ├── valid.txt　　　　　　存储用于验证的图像路径
    │   ├── voc.data　　　　　　 配置文件
    │   ├── voc.names　　　　　　标签名
    │   └── yolov3.cfg　　　　　 YOLOv3神经网络文件
    ├── data
    │   └── labels　　　　　　　　预测时用于显示标签名字
    │       ├── 100_0.png
    │       ├── 100_1.png
    │       ├── ......
    │       └── make_labels.py
    └── yolos　　　　　　　　　　　YOLOv3格式的标注
        ├── IMG_9255.JPG
        ├── IMG_9255.txt
        ├── IMG_9263.JPG
        ├── IMG_9263.txt
        ├── IMG_9266.JPG
        ├── IMG_9266.txt
        ├── IMG_9280.JPG
        └── IMG_9280.txt
    ```

1. 准备样本集
    > 使用YOLO格式标注样本集
    ```bash
    $ python3 labelImg.py [图像目录] [标注名字文件] [标注目录]
    ```

    > 元数据信息配置：cfg/voc.data
    ```
    classes= 2
    train  = cfg/train.txt
    valid  = cfg/valid.txt
    names = cfg/voc.names
    backup = backup
    ```

    > 标签名：cfg/voc.names
    ```
    close
    open
    ```

2. 分割训练集和验证集
    > 训练集的路径存储到文件：cfg/train.txt
    ```
    yolos/IMG_9255.JPG
    yolos/IMG_9266.JPG
    yolos/IMG_9280.JPG
    ```
    
    > 验证集的路径存储到文件：cfg/valid.txt
    ```
    yolos/IMG_9263.JPG
    ```

3. 配置超参数
    > YOLO神经网络文件：yolov3.cfg
    ```
    6行：batch=32
    20行：max_batches = 2000
    603行：filters=21    # (classes + 5)*3
    610行：classes=2
    689行：filters=21
    696行：classes=2
    776行：filters=21
    783行：classes=2
    ```

4. 运行darknet容器
    ```bash
    $ sudo docker run --runtime=nvidia -it --name=darknet \
        --volume=$project_dir:/darknet/project \
        darknet:latest-gpu
    ```

5. 训练模型
    ```bash
    $ ../darknet detector train cfg/voc.data cfg/yolov3.cfg ../darknet53.conv.74
    ```

6. 测试模型
    ```bash
    $ mkdir /darknet/project/data
    $ ln -s /darknet/data/labels /darknet/project/data/labels

    $ ../darknet detector test cfg/voc.data cfg/yolov3.cfg backup/yolov3_final.weights test.jpg
    ```
