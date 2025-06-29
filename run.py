import pytest
import os
from common.utils import Utils

if __name__ == "__main__":
    # 清理3天前的allure结果文件
    Utils.clean_old_allure_results(days_to_keep=1)
    
    pytest.main([
        "testcase/",
        "--alluredir=reports/allure-results",
        "--html=reports/report.html",
        "--self-contained-html",
        "-v"
    ])

    # 生成Allure HTML报告
    allure_cmd = "allure generate reports/allure-results -o reports/allure-html --clean"
    
    # 使用os.system执行命令
    result = os.system(allure_cmd)
    
    if result == 0:
        print("Allure报告生成成功")
    else:
        print("Allure报告生成失败")
