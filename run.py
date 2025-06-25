import pytest

if __name__ == "__main__":
    pytest.main([
        "testcase/",
        "--alluredir=reports/allure-results",
        "--html=reports/report.html",
        "--self-contained-html",
        "-v"
    ]) 