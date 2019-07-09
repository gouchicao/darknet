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

## 运行darknet容器（GPU）进行模型训练
1. 训练前的数据准备
    * 工程目录结构
    ```
    project/            # 工程根目录
    ├── cfg             # 配置目录
    │   └── voc.names   # 标签名
    ├── images          # 样本
    │   ├── ...
    │   └── ...
    ├── labels          # YOLO标注格式
    │   ├── ...
    │   └── ...
    └── test            # 训练完后用于测试（非必须）
        ├── ...
        └── ...
    ```

    * 举例：这里以[platen-switch](model-zoo/platen-switch)为例
    ```
    platen-switch/
    ├── cfg
    │   └── voc.names
    ├── images
    │   ├── IMG_9255.JPG
    │   ├── IMG_9263.JPG
    │   ├── IMG_9266.JPG
    │   └── IMG_9280.JPG
    ├── labels
    │   ├── IMG_9255.txt
    │   ├── IMG_9263.txt
    │   ├── IMG_9266.txt
    │   └── IMG_9280.txt
    └── test
        ├── IMG_9256.JPG
        └── IMG_9271.JPG
    ```

2. 运行darknet容器
    * 将工程目录作为挂载点绑定到容器
    ```bash
    # 使用您的工程绝对路径设置变量 project_dir
    $ export project_dir='/home/wjunjian/github/gouchicao/darknet/model-zoo/platen-switch'
    $ sudo docker run --runtime=nvidia -it --name=darknet \
        --volume=$project_dir:/darknet/project \
        gouchicao/darknet:latest-gpu
    ```

3. 创建工程，用于模型训练
    * 创建工程，自动生成训练前需要的数据
    ```bash
    $ python3 create_project.py
    ```

    * 创建后的目录结构
    ```
    platen-switch/
    ├── backup                  # 存储模型训练时权重值
    ├── cfg
    │   ├── train.txt           # 存储用于训练的图像路径
    │   ├── valid.txt           # 存储用于验证的图像路径
    │   ├── voc.data            # 配置文件
    │   ├── voc.names
    │   └── yolov3.cfg          # YOLOv3神经网络文件
    ├── data
    │   └── labels              # 预测时，用来绘制标签名
    │       ├── 100_0.png
    │       ├── ...
    │       ├── 99_7.png
    │       └── make_labels.py
    ├── images
    │   ├── IMG_9255.JPG
    │   ├── IMG_9263.JPG
    │   ├── IMG_9266.JPG
    │   └── IMG_9280.JPG
    ├── labels
    │   ├── IMG_9255.txt
    │   ├── IMG_9263.txt
    │   ├── IMG_9266.txt
    │   └── IMG_9280.txt
    ├── predict                 # 用来保存预测的图片
    └── test
        ├── IMG_9256.JPG
        └── IMG_9271.JPG
    ```

4. 配置超参数
    * 编辑YOLO神经网络文件：yolov3.cfg
    ```
    20行：max_batches = 2000    # 训练的轮数
    603行：filters=21    # (classes + 5)*3  classes指cfg/voc.data中的值
    610行：classes=2
    689行：filters=21    # (classes + 5)*3
    696行：classes=2
    776行：filters=21    # (classes + 5)*3
    783行：classes=2
    ```

5. 训练模型
    ```bash
    $ cd /darknet/project/
    $ ../darknet detector train cfg/voc.data cfg/yolov3.cfg ../darknet53.conv.74

    # 使用多GPU训练
    $ ../darknet detector train cfg/voc.data cfg/yolov3.cfg ../darknet53.conv.74 -gpus 0,1,2,3
    ```

6. 测试模型
    ```bash
    $ ../darknet detector test cfg/voc.data cfg/yolov3.cfg backup/yolov3_final.weights test.jpg
    ```

## 生成部署模型的数据
* 运行命令generate_model_deploy_data.py
```bash
$ cd /darknet/
$ python3 generate_model_deploy_data.py
```

* 生成模型数据的目录结构
```bash
platen-switch/
└── model
    ├── voc.data
    ├── voc.names
    ├── yolov3.cfg
    └── yolov3_final.weights
```
