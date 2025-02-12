#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re
import sys
import time
import json
import pandas as pd
from datetime import datetime


class WeiboSpider:
    def __init__(self):
        self.headers = {
            'User-Agent': '换你自己的',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://weibo.com/',
            'Cookie': '换你自己的'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.weibo_data = []  # 存储所有微博数据

    def get_long_text(self, id):
        """获取长文本内容"""
        try:
            url = f'https://weibo.com/ajax/statuses/longtext?id={id}'
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                json_data = response.json()
                if 'data' in json_data and 'longTextContent' in json_data['data']:
                    return json_data['data']['longTextContent']
            return None
        except Exception as e:
            print(f"获取长文本失败: {e}")
            return None

    def get_user_weibo(self, uid, page=1):
        """获取用户微博列表"""
        try:
            url = f'https://weibo.com/ajax/statuses/mymblog?uid={uid}&page={page}'
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"获取微博列表失败: {e}")
            return None

    def process_weibo(self, mblog):
        """处理单条微博"""
        try:
            created_at = mblog.get('created_at', '')
            text = mblog.get('text', '')

            # 如果是长文本
            if mblog.get('isLongText'):
                long_text = self.get_long_text(mblog['id'])
                if long_text:
                    text = long_text

            return {
                'created_at': created_at,
                'text': self.clean_text(text),
                'reposts_count': mblog.get('reposts_count', 0),
                'comments_count': mblog.get('comments_count', 0),
                'attitudes_count': mblog.get('attitudes_count', 0),
                'weibo_url': f"https://weibo.com/{mblog.get('user', {}).get('id', '')}/{mblog.get('id', '')}",
                'source': mblog.get('source', ''),
            }
        except Exception as e:
            print(f"处理微博失败: {e}")
            return None

    def clean_text(self, text):
        """清理文本内容"""
        if not text:
            return ""
        text = re.sub(r'<br\s*/?>', '\n', text)
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

    def get_all_weibo(self, uid):
        """获取所有微博"""
        page = 1
        while True:
            print(f"正在获取第 {page} 页的微博...")
            data = self.get_user_weibo(uid, page)
            if not data or 'data' not in data or 'list' not in data['data']:
                break

            weibo_list = data['data']['list']
            if not weibo_list:
                break

            for weibo in weibo_list:
                result = self.process_weibo(weibo)
                if result:
                    self.weibo_data.append(result)

            page += 1
            time.sleep(2)  # 添加延时避免被封

    def save_to_excel(self, uid):
        """保存数据到Excel文件"""
        if not self.weibo_data:
            print("没有获取到任何微博数据")
            return

        # 创建DataFrame
        df = pd.DataFrame(self.weibo_data)

        # 重新排序列
        columns_order = [
            'created_at',
            'text',
            'reposts_count',
            'comments_count',
            'attitudes_count',
            'source',
            'weibo_url'
        ]
        df = df[columns_order]

        # 设置列名的中文别名
        columns_map = {
            'created_at': '发布时间',
            'text': '微博内容',
            'reposts_count': '转发数',
            'comments_count': '评论数',
            'attitudes_count': '点赞数',
            'source': '来源',
            'weibo_url': '微博链接'
        }
        df.rename(columns=columns_map, inplace=True)

        # 生成文件名（包含用户ID和时间戳）
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'weibo_data_{uid}_{timestamp}.xlsx'

        # 保存到Excel
        try:
            df.to_excel(filename, index=False, engine='openpyxl')
            print(f"数据已保存到文件: {filename}")

            # 输出基本统计信息
            print(f"\n基本统计信息:")
            print(f"总微博数: {len(df)}")
            print(f"平均转发数: {df['转发数'].mean():.2f}")
            print(f"平均评论数: {df['评论数'].mean():.2f}")
            print(f"平均点赞数: {df['点赞数'].mean():.2f}")

        except Exception as e:
            print(f"保存Excel文件时出错: {e}")


def main():
    if len(sys.argv) < 2:
        uid = input("请输入用户ID: ")
    else:
        uid = sys.argv[1]

    spider = WeiboSpider()
    try:
        print(f"开始获取用户 {uid} 的微博数据...")
        spider.get_all_weibo(uid)
        spider.save_to_excel(uid)
        print("数据获取完成！")
    except Exception as e:
        print(f"运行出错: {e}")


if __name__ == '__main__':
    main()
