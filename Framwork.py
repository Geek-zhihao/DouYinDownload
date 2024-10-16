'''
Description  :
Date         : 2024/05/13 22:02:16
Author       : Geek-Legend
Version      : 1.0
License      : MIT
Github       :
Mail         : geek-legend@qq.com
'''
from playwright.sync_api import sync_playwright
import json
import re


class Chromium_Framwork:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start_browser(self):
        '''
        启动浏览器

        '''
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False, args=['--disable-blink-features=AutomationControlled', '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'])
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def creat_new_page(self):
        '''
        创建一个新页面

        '''
        self.page = self.context.new_page()

    def goto(self, url: str):
        '''
        跳转指定页面

        Arg:
            Url(str):欲跳转页面的网址

        '''
        self.page.goto(url)

    def page_wait(self, time: int):
        '''
        页面等待

        Arg:
            time(int):页面等待时间，单位为s

        '''
        time = time * 1000
        self.page.wait_for_timeout(time)

    def scroll_page(self, delta_x: int, delta_y: int):
        '''
        滚动页面

        Args:
            delta_x(int):水平方向滚动页面的像素距离
            delta_y(int):竖直方向滚动页面的像素距离

        '''
        self.page.mouse.wheel(delta_x, delta_y)

    def get_title(self):
        '''
        获取页面标题

        Return:
            title(str):页面标题

        '''
        title = self.page.title()
        return title

    def add_cookies(self, cookies_filepath: str):
        '''
        携带Cookie进行访问

        Arg:
            cookies_filepath(str):Cookie文件的路径

        '''
        with open(cookies_filepath, 'r') as f:
            Cookies = json.load(f)
        self.context.add_cookies(Cookies)

    def filter_and_save_responses(self, request_url: str, file_path: str, file_name: str):
        '''
        筛选特定的响应，将响应保存等待后续处理

        Arg:
            request_url(str):请求的部分URL
            file_path(str):文件保存路径
            file_name(str):文件名

        '''
        save_path = file_path + file_name
        self.page.on(
            "response", lambda responses: save_responses(responses))  # 订阅响应

        def save_responses(response):

            # 检查响应的URL是否包含所需的请求URL
            if request_url in response.url:
                try:
                    result = response.json().get('aweme_list', [])  # 将响应内容解析为JSON格式
                except ValueError:
                    result = []  # 如果响应内容不是有效的JSON，捕获异常并设置 result 为 None

                with open(save_path, 'a', encoding='utf-8') as file:
                    for item in result:
                        json.dump(item, file, ensure_ascii=False, indent=4)
                        file.write(',\n')
                    print(f"Saved response to {file_name}")

    def intercept_requests(self, url_patterns: list):
        '''
        拦截特定的请求

        Arg:
            url_patterns(list):需拦截的请求的部分URL列表，列表元素需为正则表达形式

        '''
        regex_patterns = [re.compile(pattern)
                          for pattern in url_patterns]  # 将列表元素转换成正则匹配对象

        # 处理请求逻辑
        def handle_route(route, request):
            # 如果请求符合输入则拦截。反之则放行
            if any(pattern.match(request.url) for pattern in regex_patterns):
                route.abort()  # 拦截请求
            else:
                route.continue_()  # 放行请求

        self.page.route("**/*", handle_route)  # 拦截和处理所有网络请求

    def close(self):
        '''
        关闭浏览器

        '''
        self.context.close()
        self.browser.close()
        self.playwright.stop()
