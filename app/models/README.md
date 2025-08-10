# 模型文件说明

## disease_model.pkl

这个文件应该包含训练好的机器学习模型。

### 创建模型的示例代码：

```python
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
import numpy as np

# 生成示例数据
X, y = make_classification(n_samples=1000, n_features=5, n_classes=2, random_state=42)

# 分割数据
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练模型
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 保存模型
joblib.dump(model, 'disease_model.pkl')
```

### 模型输入特征：
1. 特征1: 年龄
2. 特征2: 血压
3. 特征3: 血糖
4. 特征4: 胆固醇
5. 特征5: BMI

### 模型输出：
- 预测类别 (0 或 1)
- 各类别的概率

注意：请将实际训练好的模型文件放在此目录下，命名为 `disease_model.pkl`
