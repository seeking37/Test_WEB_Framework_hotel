import yaml
import os
from typing import List, Dict, Any


class TestDataLoader:
    """测试数据加载器"""
    
    @staticmethod
    def load_yaml_data(file_path: str) -> Dict[str, Any]:
        """从yaml文件加载测试数据"""
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(full_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    @staticmethod
    def get_login_success_cases() -> List[Dict[str, Any]]:
        """获取登录成功测试用例"""
        data = TestDataLoader.load_yaml_data('../data/login_cases.yaml')
        return data.get('login_success_cases', [])
    
    @staticmethod
    def get_login_failure_cases() -> List[Dict[str, Any]]:
        """获取登录失败测试用例"""
        data = TestDataLoader.load_yaml_data('../data/login_cases.yaml')
        return data.get('login_failure_cases', [])
    
    @staticmethod
    def get_signup_success_cases() -> List[Dict[str, Any]]:
        """获取注册成功测试用例"""
        data = TestDataLoader.load_yaml_data('../data/signup_cases.yaml')
        return data.get('signup_success_cases', [])
    
    @staticmethod
    def get_signup_failure_cases() -> List[Dict[str, Any]]:
        """获取注册失败测试用例"""
        data = TestDataLoader.load_yaml_data('../data/signup_cases.yaml')
        return data.get('signup_failure_cases', []) 