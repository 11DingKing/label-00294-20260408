#!/bin/bash
# 运行测试脚本

echo "开始运行Django测试用例..."

# 运行所有测试
python manage.py test apps.authentication apps.orders apps.users --verbosity=2

echo "测试完成！"
