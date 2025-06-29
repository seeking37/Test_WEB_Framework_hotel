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
    def get_test_cases(yaml_file: str, case_key: str) -> List[Dict[str, Any]]:
        """
        通用的测试用例获取方法
        
        Args:
            yaml_file: YAML文件路径（相对于common目录），如：'../data/login_cases.yaml'
            case_key: 测试用例在YAML中的键名，如：'login_success_cases'
            
        Returns:
            测试用例列表
            
        Examples:
            # 获取登录成功用例
            TestDataLoader.get_test_cases('../data/login_cases.yaml', 'login_success_cases')
            
            # 获取注册失败用例  
            TestDataLoader.get_test_cases('../data/signup_cases.yaml', 'signup_failure_cases')
            
            # 获取个人页面预设用户用例
            TestDataLoader.get_test_cases('../data/mypage_cases.yaml', 'existing_users_cases')
        """
        data = TestDataLoader.load_yaml_data(yaml_file)
        return data.get(case_key, []) 