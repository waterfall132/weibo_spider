## 微博爬虫代码介绍 (Python)

一个使用Python编写的微博爬虫代码，该代码可以爬取指定用户的微博数据，包括微博内容、发布时间、转发数、评论数、点赞数、来源和链接，并将数据保存到Excel文件中。

### 1. 代码概述

该代码使用`requests`库发送HTTP请求，`re`库进行正则表达式匹配，`pandas`库处理数据并保存到Excel，以及`json`库解析JSON数据。

核心功能包括：

*   **获取用户微博列表：** 根据用户ID和页码获取微博数据。
*   **获取长文本内容：** 对于长微博，单独获取完整文本。
*   **处理单条微博：** 提取微博关键信息，包括发布时间、内容、转发数、评论数、点赞数、来源和链接。
*   **清理文本内容：** 使用正则表达式去除HTML标签和`<br>`换行符。
*   **获取所有微博：** 循环获取所有页面的微博数据。
*   **保存到Excel：** 将爬取到的数据保存到Excel文件，并进行列名中文化。

### 2. 代码结构

```
WeiboSpider
├── __init__
├── get_long_text
├── get_user_weibo
├── process_weibo
├── clean_text
├── get_all_weibo
└── save_to_excel
main
```

### 3. 类和方法介绍

#### 3.1 `WeiboSpider` 类

*   `__init__(self)`: 初始化方法，设置请求头、会话和存储微博数据的列表。
*   `get_long_text(self, id)`: 获取长文本内容。
*   `get_user_weibo(self, uid, page=1)`: 获取用户微博列表。
*   `process_weibo(self, mblog)`: 处理单条微博数据。
*   `clean_text(self, text)`: 清理文本内容，去除HTML标签。
*   `get_all_weibo(self, uid)`: 获取所有微博数据。
*   `save_to_excel(self, uid)`: 保存数据到Excel文件。

#### 3.2 `main` 函数

*   `main()`: 主函数，接收用户ID参数，调用`WeiboSpider`类的方法完成微博爬取和保存。

### 4. 代码详解

#### 4.1 初始化

在`__init__`方法中，设置了请求头，包括`User-Agent`、`Accept`、`Referer`和`Cookie`。**请务必替换`Cookie`为你自己的Cookie。**

#### 4.2 获取微博数据

`get_user_weibo`方法根据用户ID和页码获取微博数据，返回JSON格式的响应。`get_long_text`方法用于获取长微博的完整文本。

#### 4.3 处理微博数据

`process_weibo`方法提取微博的关键信息，包括发布时间、内容、转发数、评论数、点赞数、来源和链接。`clean_text`方法用于清理微博文本，去除HTML标签和`<br>`换行符。

#### 4.4 获取所有微博

`get_all_weibo`方法循环调用`get_user_weibo`方法，获取所有页面的微博数据，直到没有更多数据为止。

#### 4.5 保存到Excel

`save_to_excel`方法将爬取到的数据保存到Excel文件，并进行列名中文化。文件名包含用户ID和时间戳，以`weibo_data_{uid}_{timestamp}.xlsx`的格式命名。

#### 4.6 主函数

`main`函数接收用户ID参数，创建`WeiboSpider`对象，调用相应方法完成微博爬取和保存。

### 5. 使用方法

1.  **安装依赖库：**
    ```bash
    pip install requests pandas openpyxl
    ```
2.  **替换Cookie：** 将代码中的`Cookie`替换为你自己的Cookie。
3.  **运行代码：**
    *   **命令行参数：**
        ```bash
        python weibo_spider.py <user_id>
        ```
    *   **交互式输入：**
        ```bash
        python weibo_spider.py
        ```
        然后根据提示输入用户ID。

### 6. 注意事项

*   请确保你的Cookie有效，否则无法获取数据。
*   爬取速度不宜过快，以免被微博反爬虫机制限制。
*   本代码仅用于学习交流，请勿用于商业用途。


