"""
全局异常处理
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger('apps')


def custom_exception_handler(exc, context):
    """
    自定义异常处理器
    """
    # 调用默认的异常处理器
    response = exception_handler(exc, context)
    
    # 记录异常日志
    logger.error(f"Exception occurred: {exc}", exc_info=True)
    
    # 自定义响应格式
    if response is not None:
        custom_response_data = {
            'code': response.status_code,
            'message': '操作失败',
            'data': None,
        }
        
        # 处理验证错误
        if response.status_code == 400:
            if 'detail' in response.data:
                custom_response_data['message'] = response.data['detail']
            elif isinstance(response.data, dict):
                # 处理字段验证错误
                errors = []
                for field, messages in response.data.items():
                    if isinstance(messages, list):
                        errors.extend([f"{field}: {msg}" for msg in messages])
                    else:
                        errors.append(f"{field}: {messages}")
                custom_response_data['message'] = '; '.join(errors)
            else:
                custom_response_data['message'] = str(response.data)
        
        # 处理认证错误
        elif response.status_code == 401:
            custom_response_data['message'] = '未授权，请先登录'
        
        # 处理权限错误
        elif response.status_code == 403:
            custom_response_data['message'] = '权限不足'
        
        # 处理未找到错误
        elif response.status_code == 404:
            custom_response_data['message'] = '资源不存在'
        
        response.data = custom_response_data
    
    return response
