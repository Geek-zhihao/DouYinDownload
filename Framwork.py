'''
Description  : 
Date         : 2024/05/13 22:02:16
Author       : Geek-Legend
Version      : 1.0
License      : 
Github       : 
Mail         : geek-legend@qq.com
'''
from playwright.sync_api import sync_playwright
import json


class Framwork:
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
        print("浏览器启动")

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
            time(int):页面等待时间

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

    def click_element(self, locator: str):
        '''
        使用CSS选择器寻找指定元素,并点击

        Arg:
            locator(str):元素的id

        '''
        self.page.locator(f".{locator}").click()

    # 携带Cookie进行访问
    def add_cookies(self, Cookies_filepath: str):
        '''
        携带Cookie进行访问

        Arg:
            Cookies_filepath(str):Cookie文件的路径

        '''
        with open(Cookies_filepath, 'r') as f:
            Cookies = json.load(f)
        self.context.add_cookies(Cookies)

    def close(self):
        '''
        关闭浏览器

        '''
        self.context.close()
        self.browser.close()
        self.playwright.stop()
        print("浏览器关闭")


# 使用示例
if __name__ == '__main__':

    manager = Framwork()
    manager.start_browser()
    manager.add_cookies("Cookie_1.json")
    manager.goto(
        "https://www.douyin.com/user/MS4wLjABAAAA4OBM5NbxBG-b75Ty_ecsGjdCztO77e3YS9WW242tbLA")
    # manager.scroll_page(0, 70000)
    # manager.page_wait(1)
    # manager.scroll_page(0, 70000)
    manager.page_wait(10)
    manager.click_element("dy-account-close")
    manager.page_wait(10)
    title = manager.get_title()
    print(f"Page title: {title}")
    manager.close()
    # manager = Framwork()
    # manager.start()
    # manager.goto("https://www.baidu.com")
    # title = manager.get_title()
    # print(f"Page title: {title}")
    # manager.creat_new_page()
    # manager.goto("https://www.bing.com")
    # title = manager.get_title()
    # print(f"Page title: {title}")
    # manager.close()
