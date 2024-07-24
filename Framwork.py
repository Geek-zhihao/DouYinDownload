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
            headless=False, args=['--disable-blink-features=AutomationControlled'])
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

    def find_element(self, attribute: str):
        '''
        使用选择器寻找指定元素

        Arg:
            locator(str):元素的id

        Return:
            locator(element):选择对象
        '''
        locator = self.page.locator(f".{attribute}")
        return locator

    def add_cookies(self, cookies_filepath: str):
        '''
        携带Cookie进行访问

        Arg:
            cookies_filepath(str):Cookie文件的路径

        '''
        with open(cookies_filepath, 'r') as f:
            Cookies = json.load(f)
        self.context.add_cookies(Cookies)

    def filter_responses(self, request_url: str, callback=None):
        '''
        筛选特定的响应，将响应返回给回调函数处理

        Arg:
            request_url(str):请求的部分URL
            callback(None):回调函数，抓取到响应立即执行回调函数

        '''
        self.page.on(
            "response", lambda response: handle_response(response))  # 订阅响应

        def handle_response(response):

            # 检查响应的URL是否包含所需的请求URL
            if request_url in response.url:
                try:
                    result = response.json()  # 将响应内容解析为JSON格式
                except ValueError:
                    result = None  # 如果响应内容不是有效的JSON，捕获异常并设置 result 为 None

                # 如果提供了回调函数，且解析成功，调用回调函数并传递结果
                if callback:
                    callback(result)

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


# 使用示例
if __name__ == '__main__':
    manager = Chromium_Framwork()
    manager.start_browser()
    manager.add_cookies("Cookie_1.json")
    manager.intercept_requests([
        ".*-sign\.douyinpic\.com.*",  # lf3-cdn-tos.bytegoofy.com
        ".*lf3-cdn-tos\.bytegoofy\.com.*",  # *-sign.douyinpic.com
        # lf6-cdn-tos.bytegoofy.com/obj/goofy/ies/douyin_web/async/9635*
        "lf6-cdn-tos\.bytegoofy\.com/obj/goofy/ies/douyin_web/async/9635.*",
        # lf6-cdn-tos.bytegoofy.com/obj/goofy/ies/douyin_web/async/feelgood*
        "lf6-cdn-tos\.bytegoofy\.com/obj/goofy/ies/douyin_web/async/feelgood.*",
        # lf6-cdn-tos.bytegoofy.com/obj/goofy/ies/douyin_web/async/FlowSDK*
        "lf6-cdn-tos\.bytegoofy\.com/obj/goofy/ies/douyin_web/async/FlowSDK.*",
        "lf3-pendah\.bytetos\.com",  # lf3-pendah.bytetos.com
        # lf6-cdn-tos.bytegoofy.com/obj/goofy/ies/douyin_web/chunks/*
        "lf6-cdn-tos\.bytegoofy\.com/obj/goofy/ies/douyin_web/chunks/.*",
        ".*(png|ico)",
        "data:"
    ])
    # manager.goto(
    #     "https://www.douyin.com/user/MS4wLjABAAAA4OBM5NbxBG-b75Ty_ecsGjdCztO77e3YS9WW242tbLA")
    manager.goto(
        "https://www.douyin.com/user/MS4wLjABAAAAQizVwBD-8xw0ml6kjPhwFglH1TdiEIqziMJIZRielMCAEUHnCq6_hHVR-IXIG4k3")
    # manager.keep_intercepting()  # 保持拦截功能常驻在后台
    # manager.scroll_page(0, 70000)
    # manager.page_wait(1)
    # manager.scroll_page(0, 70000)

    def handle_status(status):
        with open("filename.json", 'a', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False)
        print(f"Saved response to filename.json")
    manager.filter_responses(
        "https://www.douyin.com/aweme/v1/web/aweme/post/", callback=handle_status)
    manager.page_wait(4)

    manager.page_wait(4)
    manager.find_element("dy-account-close")
    manager.page_wait(30)
    title = manager.get_title()
    print(f"Page title: {title}")
    manager.close()
