import os
import yaml
from typing import List, Set, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta

# 工具类，存放与页面无关的复用逻辑
class Utils:
    BASE_URL = os.getenv('BASE_URL', 'https://hotel-example-site.takeyaqa.dev/en-US')
    
    @staticmethod
    def get_new_window_handle(handles_before_open: Set[str], handles_after_open: Set[str]) -> str:
        """获取新窗口句柄"""
        handles = handles_after_open - handles_before_open
        if not handles:
            raise RuntimeError("找不到新窗口")
        elif len(handles) > 1:
            raise RuntimeError("存在多个窗口")
        else:
            return list(handles)[0]
        
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
            Utils.get_test_cases('../data/login_cases.yaml', 'login_success_cases')
        """
        data = Utils.load_yaml_data(yaml_file)
        return data.get(case_key, [])
    
    @staticmethod
    def clean_old_allure_results(days_to_keep: int = 3, reports_dir: str = "reports"):
        """清理指定天数之前的allure-results文件"""
        allure_results_dir = Path(reports_dir) / "allure-results"
        
        if not allure_results_dir.exists():
            return
        
        cutoff_time = datetime.now() - timedelta(days=days_to_keep)
        cleaned_count = 0
        
        # 清理旧的JSON文件
        for file_path in allure_results_dir.glob("*.json"):
            try:
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_time:
                    file_path.unlink()
                    cleaned_count += 1
            except Exception:
                # 忽略无法删除的文件
                continue
        
        if cleaned_count > 0:
            print(f"已清理 {cleaned_count} 个 {days_to_keep} 天前的allure结果文件") 