# 🎨 风格转换小工具（Style Transfer App）

这是一个基于 PyTorch 与 Tkinter 实现的桌面图像风格转换应用。你只需点击输入区域选择一张图片，即可一键生成具有艺术风格的图像效果。

---

## 🧠 项目亮点

- 💻 图形化界面（GUI）：简单易用，点击图片即可转换  
- 🖼️ 左右对比视图：原图与风格图并列展示，方便比较  
- 🎨 多种艺术风格：支持 `mosaic`、`candy`、`starry_night`、`udnie` 等  
- 💾 本地模型推理：无需联网，运行高效

---

## 📁 项目结构
```plaintext
style_transfer_app/
├── models/                     # 存放风格模型（.pth）
│   ├── mosaic.pth
│   ├── candy.pth
│   ├── starry_night.pth
│   └── udnie.pth
├── transformer_net.py         # TransformerNet 模型结构定义
├── style.py                   # 主程序入口（含GUI和风格迁移逻辑）
├── README.md                  # 项目说明文档
└── samples/                   # 示例图像（可选）
    ├── original.jpg
    └── mosaic.jpg
```


## 🧩 环境依赖

请确保已安装以下 Python 依赖（建议使用 Python 3.8+）：

```bash
pip install torch torchvision pillow
```

### 🎨 支持的风格模型

| 风格名称          | 模型文件名               |
|---------------|---------------------|
| Mosaic        | `mosaic.pth`        |
| Candy         | `candy.pth`         |
| Udnie         | `udnie.pth`         |
| Rain Princess | `rain_princess.pth` |
