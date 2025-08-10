# Web Disease Prediction Project

## 项目说明

这是一个基于Web的疾病预测系统，使用机器学习模型进行疾病预测。

## 项目结构

```
Web/
│
├── README.md                # 项目说明
├── requirements.txt         # 依赖包
├── app/                     # 核心后端代码
│   ├── __init__.py
│   ├── main.py               # 入口
│   ├── models/               # 预测模型
│   │   ├── __init__.py
│   │   └── disease_model.pkl
│   ├── routes/               # API 路由
│   │   ├── __init__.py
│   │   └── predict.py
│   └── static/               # 静态文件（CSS/JS/图片）
│       ├── css/
│       ├── js/
│       └── images/
│
├── templates/                # 前端模板（HTML）
│   ├── base.html
│   └── predict.html
│
└── tests/                    # 单元测试
    └── test_predict.py
```

## 安装和运行

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行应用：
   ```bash
   python app/main.py
   ```

## 功能特性

- 疾病预测模型
- Web界面
- API接口
- 单元测试
