import unittest
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.main import create_app

class TestPredictAPI(unittest.TestCase):
    """预测API测试类"""
    
    def setUp(self):
        """测试前的设置"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """测试健康检查接口"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_predict_missing_data(self):
        """测试缺少数据的预测请求"""
        response = self.client.post('/api/predict/diabetes',
                                  data=json.dumps({}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_predict_empty_factors(self):
        """测试空因子的预测请求"""
        response = self.client.post('/api/predict/diabetes',
                                  data=json.dumps({'factors': {}}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_predict_with_factors(self):
        """测试带有风险因子的预测请求"""
        test_factors = {
            'age': 45,
            'bmi': 28.5,
            'waist_circumference': 95,
            'systolic_bp': 140,
            'family_history': 1,
            'physical_activity': 0
        }

        response = self.client.post('/api/predict/diabetes',
                                  data=json.dumps({'factors': test_factors}),
                                  content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('risk_score', data)
        self.assertIn('risk_level', data)
        self.assertEqual(data['status'], 'success')

    def test_predict_invalid_disease(self):
        """测试无效疾病ID的预测请求"""
        response = self.client.post('/api/predict/invalid_disease',
                                  data=json.dumps({'factors': {'age': 30}}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_index_page(self):
        """测试主页"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # 检查页面是否包含疾病分类
        self.assertIn(b'Disease Risk Assessment', response.data)

    def test_disease_page(self):
        """测试疾病预测页面"""
        response = self.client.get('/disease/diabetes')
        self.assertEqual(response.status_code, 200)

    def test_invalid_json(self):
        """测试无效的JSON数据"""
        response = self.client.post('/api/predict/diabetes',
                                  data='invalid json',
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_api_diseases(self):
        """测试疾病列表API"""
        response = self.client.get('/api/diseases')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('diseases', data)
        self.assertEqual(data['status'], 'success')

class TestRiskCalculation(unittest.TestCase):
    """风险计算测试类"""

    def test_diabetes_risk_calculation(self):
        """测试糖尿病风险计算"""
        from app.routes.predict import calculate_diabetes_risk

        # 测试低风险情况
        low_risk_factors = {
            'age': 25,
            'bmi': 22,
            'waist_circumference': 75,
            'systolic_bp': 110,
            'family_history': 0,
            'physical_activity': 2
        }
        risk_score = calculate_diabetes_risk(low_risk_factors)
        self.assertLess(risk_score, 30)

        # 测试高风险情况
        high_risk_factors = {
            'age': 65,
            'bmi': 32,
            'waist_circumference': 100,
            'systolic_bp': 150,
            'family_history': 1,
            'physical_activity': 0
        }
        risk_score = calculate_diabetes_risk(high_risk_factors)
        self.assertGreater(risk_score, 50)

    def test_lung_cancer_risk_calculation(self):
        """测试肺癌风险计算"""
        from app.routes.predict import calculate_lung_cancer_risk

        # 测试高风险情况（重度吸烟者）
        high_risk_factors = {
            'age': 60,
            'gender': 1,
            'smoking_years': 30,
            'smoking_amount': 20,
            'family_history': 1,
            'occupational_exposure': 1
        }
        risk_score = calculate_lung_cancer_risk(high_risk_factors)
        self.assertGreater(risk_score, 70)

if __name__ == '__main__':
    # 使用TestLoader代替已弃用的makeSuite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加测试用例
    suite.addTests(loader.loadTestsFromTestCase(TestPredictAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestRiskCalculation))

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 输出测试结果
    if result.wasSuccessful():
        print("\n所有测试通过!")
    else:
        print(f"\n测试失败: {len(result.failures)} 个失败, {len(result.errors)} 个错误")
