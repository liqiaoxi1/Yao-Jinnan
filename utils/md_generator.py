#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
from datetime import datetime
from typing import List, Dict, Any
import importlib.util
import re

def extract_docstring(obj: Any) -> str:
    """提取对象的文档字符串"""
    if hasattr(obj, '__doc__') and obj.__doc__:
        return obj.__doc__.strip()
    return ""

def extract_schema_info(schema_path: str) -> Dict[str, Any]:
    """从 Schema 文件中提取信息"""
    spec = importlib.util.spec_from_file_location("schema", schema_path)
    if not spec or not spec.loader:
        return {}
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    schemas = {}
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and hasattr(obj, '__doc__'):
            schemas[name] = {
                'docstring': extract_docstring(obj),
                'fields': []
            }
            # 提取字段信息
            if hasattr(obj, '__fields__'):
                for field_name, field in obj.__fields__.items():
                    field_info = {
                        'name': field_name,
                        'type': str(field.type_),
                        'description': field.description or ''
                    }
                    schemas[name]['fields'].append(field_info)
    
    return schemas

def extract_api_info(api_path: str) -> Dict[str, Any]:
    """从 API 文件中提取信息"""
    spec = importlib.util.spec_from_file_location("api", api_path)
    if not spec or not spec.loader:
        return {}
    
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    endpoints = {}
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and hasattr(obj, '__doc__'):
            # 提取路由装饰器信息
            if hasattr(obj, '__wrapped__'):
                wrapped = obj.__wrapped__
                if hasattr(wrapped, '__route__'):
                    route_info = wrapped.__route__
                    endpoints[name] = {
                        'docstring': extract_docstring(obj),
                        'method': route_info.get('methods', ['GET'])[0],
                        'path': route_info.get('path', ''),
                        'parameters': []
                    }
    
    return endpoints

def create_module_docs(module_name: str, api_path: str, schema_path: str, output_dir: str = "docs"):
    """
    为指定模块创建 API 文档
    
    Args:
        module_name (str): 模块名称
        api_path (str): API 文件路径
        schema_path (str): Schema 文件路径
        output_dir (str): 输出目录
    """
    # 确保输出目录存在
    module_doc_dir = os.path.join(output_dir, module_name)
    os.makedirs(module_doc_dir, exist_ok=True)
    
    # 提取信息
    schemas = extract_schema_info(schema_path)
    endpoints = extract_api_info(api_path)
    
    # 生成文档内容
    content = f"""# {module_name} 模块文档

## 数据模型

"""
    
    # 添加 Schema 信息
    for schema_name, schema_info in schemas.items():
        content += f"""### {schema_name}
{schema_info['docstring']}

#### 字段
| 字段名 | 类型 | 描述 |
|--------|------|------|
"""
        for field in schema_info['fields']:
            content += f"| {field['name']} | {field['type']} | {field['description']} |\n"
        content += "\n"
    
    # 添加 API 端点信息
    content += """## API 接口

"""
    for endpoint_name, endpoint_info in endpoints.items():
        content += f"""### {endpoint_name}
**请求方法**: {endpoint_info['method']}
**路径**: {endpoint_info['path']}

{endpoint_info['docstring']}

"""
    
    # 添加更新日志
    content += f"""
## 更新日志
### {datetime.now().strftime('%Y-%m-%d')}
- 初始版本
"""
    
    # 写入文件
    filepath = os.path.join(module_doc_dir, "README.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"模块文档已创建: {filepath}")

def create_markdown(title: str, output_dir: str = "docs"):
    """
    创建一个基本的 Markdown 文档结构
    
    Args:
        title (str): 文档标题
        output_dir (str): 输出目录，默认为 docs
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文件名（使用标题的小写形式，空格替换为下划线）
    filename = f"{title.lower().replace(' ', '_')}.md"
    filepath = os.path.join(output_dir, filename)
    
    # 生成文档内容
    content = f"""# {title}

## 简介
[在这里添加简介]

## 目录
1. [背景](#背景)
2. [功能](#功能)
3. [使用方法](#使用方法)
4. [注意事项](#注意事项)

## 背景
[在这里添加背景信息]

## 功能
- 功能1
- 功能2
- 功能3

## 使用方法
### 安装
```bash
# 安装步骤
```

### 配置
```bash
# 配置说明
```

### 运行
```bash
# 运行命令
```

## 注意事项
- 注意事项1
- 注意事项2

## 更新日志
### {datetime.now().strftime('%Y-%m-%d')}
- 初始版本

## 贡献
欢迎提交 Issue 和 Pull Request

## 许可证
[添加许可证信息]
"""
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Markdown 文档已创建: {filepath}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使用方法:")
        print("1. 创建基本文档: python md_generator.py '文档标题' [输出目录]")
        print("2. 创建模块文档: python md_generator.py --module 模块名 API文件路径 Schema文件路径 [输出目录]")
        sys.exit(1)
    
    if sys.argv[1] == "--module":
        if len(sys.argv) < 5:
            print("使用方法: python md_generator.py --module 模块名 API文件路径 Schema文件路径 [输出目录]")
            sys.exit(1)
        module_name = sys.argv[2]
        api_path = sys.argv[3]
        schema_path = sys.argv[4]
        output_dir = sys.argv[5] if len(sys.argv) > 5 else "docs"
        create_module_docs(module_name, api_path, schema_path, output_dir)
    else:
        title = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "docs"
        create_markdown(title, output_dir) 