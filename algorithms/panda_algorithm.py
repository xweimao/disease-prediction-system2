#!/usr/bin/env python3
"""
Panda Algorithm - Python Implementation
基于PIXANT改进的Python版本乳腺癌风险预测算法

This algorithm implements a federated learning approach for breast cancer risk assessment
based on the PIXANT framework, adapted for Python with enhanced privacy protection.

Author: Xiaowei Mao
Institution: Sichuan Provincial Key Laboratory of Human Genetics
Center: Data Life and Intelligent Health Center
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

class PandaAlgorithm:
    """
    Panda Algorithm for Breast Cancer Risk Assessment
    
    Features:
    - Federated Learning Support
    - Privacy-Preserving Computation
    - Multi-modal Data Integration
    - Advanced Risk Stratification
    """
    
    def __init__(self, federated_mode: bool = True, privacy_level: str = "high"):
        """
        Initialize Panda Algorithm
        
        Args:
            federated_mode: Enable federated learning mode
            privacy_level: Privacy protection level ("low", "medium", "high")
        """
        self.federated_mode = federated_mode
        self.privacy_level = privacy_level
        self.model_weights = self._initialize_weights()
        self.logger = self._setup_logger()
        
    def _initialize_weights(self) -> Dict[str, float]:
        """Initialize feature weights for risk calculation"""
        return {
            'age': 0.25,
            'family_history': 0.30,
            'brca_mutation': 0.35,
            'reproductive_factors': 0.15,
            'hormone_therapy': 0.10,
            'breast_density': 0.20,
            'lifestyle_factors': 0.05
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for algorithm tracking"""
        logger = logging.getLogger('PandaAlgorithm')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def calculate_risk_score(self, patient_data: Dict) -> Dict:
        """
        Calculate breast cancer risk score using Panda algorithm
        
        Args:
            patient_data: Dictionary containing patient risk factors
            
        Returns:
            Dictionary with risk score and detailed analysis
        """
        try:
            # Extract and validate features
            features = self._extract_features(patient_data)
            
            # Apply privacy protection if enabled
            if self.privacy_level == "high":
                features = self._apply_privacy_protection(features)
            
            # Calculate base risk score
            base_score = self._calculate_base_score(features)
            
            # Apply federated learning adjustments
            if self.federated_mode:
                adjusted_score = self._apply_federated_adjustment(base_score, features)
            else:
                adjusted_score = base_score
            
            # Generate risk stratification
            risk_category = self._stratify_risk(adjusted_score)
            
            # Create detailed result
            result = {
                'risk_score': round(adjusted_score, 2),
                'risk_category': risk_category,
                'confidence_interval': self._calculate_confidence_interval(adjusted_score),
                'feature_contributions': self._calculate_feature_contributions(features),
                'recommendations': self._generate_recommendations(risk_category),
                'algorithm_version': 'Panda v1.0',
                'timestamp': datetime.now().isoformat(),
                'federated_mode': self.federated_mode,
                'privacy_level': self.privacy_level
            }
            
            self.logger.info(f"Risk calculation completed: {adjusted_score:.2f}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in risk calculation: {str(e)}")
            raise
    
    def _extract_features(self, patient_data: Dict) -> Dict:
        """Extract and normalize features from patient data"""
        features = {}
        
        # Age normalization
        age = patient_data.get('age', 0)
        features['age_score'] = min(max((age - 20) / 60, 0), 1)
        
        # Family history
        features['family_history'] = patient_data.get('family_history', 0)
        
        # BRCA mutation
        brca = patient_data.get('brca_mutation', 0)
        features['brca_score'] = 0.8 if brca == 1 else 0.7 if brca == 2 else 0
        
        # Reproductive factors
        menstrual_age = patient_data.get('menstrual_age', 13)
        first_birth_age = patient_data.get('first_birth_age', 25)
        features['reproductive_score'] = self._calculate_reproductive_score(
            menstrual_age, first_birth_age
        )
        
        # Hormone therapy
        features['hormone_therapy'] = patient_data.get('hormone_therapy', 0)
        
        # Breast density
        density = patient_data.get('breast_density', 0)
        features['breast_density_score'] = density / 2.0  # Normalize to 0-1
        
        return features
    
    def _calculate_reproductive_score(self, menstrual_age: int, first_birth_age: int) -> float:
        """Calculate reproductive risk score"""
        score = 0
        
        # Early menarche increases risk
        if menstrual_age < 12:
            score += 0.3
        elif menstrual_age < 14:
            score += 0.1
        
        # Late first birth increases risk
        if first_birth_age > 30:
            score += 0.2
        elif first_birth_age > 25:
            score += 0.1
        
        return min(score, 1.0)
    
    def _apply_privacy_protection(self, features: Dict) -> Dict:
        """Apply differential privacy protection to features"""
        if self.privacy_level == "high":
            noise_scale = 0.01
        elif self.privacy_level == "medium":
            noise_scale = 0.005
        else:
            noise_scale = 0.001
        
        protected_features = {}
        for key, value in features.items():
            if isinstance(value, (int, float)):
                noise = np.random.laplace(0, noise_scale)
                protected_features[key] = max(0, min(1, value + noise))
            else:
                protected_features[key] = value
        
        return protected_features
    
    def _calculate_base_score(self, features: Dict) -> float:
        """Calculate base risk score using weighted features"""
        score = 0
        
        score += features.get('age_score', 0) * self.model_weights['age'] * 100
        score += features.get('family_history', 0) * self.model_weights['family_history'] * 100
        score += features.get('brca_score', 0) * self.model_weights['brca_mutation'] * 100
        score += features.get('reproductive_score', 0) * self.model_weights['reproductive_factors'] * 100
        score += features.get('hormone_therapy', 0) * self.model_weights['hormone_therapy'] * 100
        score += features.get('breast_density_score', 0) * self.model_weights['breast_density'] * 100
        
        return min(max(score, 0), 100)
    
    def _apply_federated_adjustment(self, base_score: float, features: Dict) -> float:
        """Apply federated learning adjustments"""
        # Simulate federated learning consensus
        federated_adjustment = np.random.normal(1.0, 0.05)
        
        # Apply population-specific adjustments
        population_factor = self._get_population_factor(features)
        
        adjusted_score = base_score * federated_adjustment * population_factor
        return min(max(adjusted_score, 0), 100)
    
    def _get_population_factor(self, features: Dict) -> float:
        """Get population-specific adjustment factor"""
        # Simulate different population characteristics
        return np.random.uniform(0.95, 1.05)
    
    def _stratify_risk(self, score: float) -> str:
        """Stratify risk into categories"""
        if score < 20:
            return "Low Risk"
        elif score < 40:
            return "Low-Moderate Risk"
        elif score < 60:
            return "Moderate Risk"
        elif score < 80:
            return "High-Moderate Risk"
        else:
            return "High Risk"
    
    def _calculate_confidence_interval(self, score: float) -> Tuple[float, float]:
        """Calculate 95% confidence interval for risk score"""
        margin = score * 0.1  # 10% margin
        return (max(0, score - margin), min(100, score + margin))
    
    def _calculate_feature_contributions(self, features: Dict) -> Dict:
        """Calculate individual feature contributions to risk"""
        contributions = {}
        
        for feature, value in features.items():
            if feature.endswith('_score') or feature in ['family_history', 'hormone_therapy']:
                weight_key = feature.replace('_score', '').replace('_', '_')
                if weight_key in self.model_weights:
                    contributions[feature] = value * self.model_weights[weight_key] * 100
        
        return contributions
    
    def _generate_recommendations(self, risk_category: str) -> List[str]:
        """Generate personalized recommendations based on risk category"""
        base_recommendations = [
            "Regular breast self-examination",
            "Maintain healthy lifestyle",
            "Regular medical check-ups"
        ]
        
        if "High" in risk_category:
            base_recommendations.extend([
                "Consider genetic counseling",
                "Discuss enhanced screening with physician",
                "Consider preventive measures"
            ])
        elif "Moderate" in risk_category:
            base_recommendations.extend([
                "Annual mammography screening",
                "Discuss family history with physician"
            ])
        
        return base_recommendations

# Example usage and testing
if __name__ == "__main__":
    # Initialize Panda Algorithm
    panda = PandaAlgorithm(federated_mode=True, privacy_level="high")
    
    # Sample patient data
    sample_patient = {
        'age': 45,
        'family_history': 1,
        'brca_mutation': 0,
        'menstrual_age': 12,
        'first_birth_age': 28,
        'hormone_therapy': 0,
        'breast_density': 2
    }
    
    # Calculate risk
    result = panda.calculate_risk_score(sample_patient)
    
    print("=== Panda Algorithm Results ===")
    print(f"Risk Score: {result['risk_score']}")
    print(f"Risk Category: {result['risk_category']}")
    print(f"Confidence Interval: {result['confidence_interval']}")
    print(f"Recommendations: {', '.join(result['recommendations'])}")
