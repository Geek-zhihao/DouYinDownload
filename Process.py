'''
Description  : 
Date         : 2024/07/25 10:16:56
Author       : Geek-Legend
Version      : 1.0
License      : 
Github       : 
Mail         : geek-legend@qq.com
'''
from Framwork import Chromium_Framwork
import json


class Process:
    def __init__(self, framwork: Chromium_Framwork) -> None:
        self.framwork = framwork

    def scroll_page_until_end(self):
        '''
        滚动页面直到最底部

        '''
        # 无限循环以滚动页面
        while True:
            self.framwork.scroll_page(
                delta_x=0, delta_y=-100)  # 回滚100像素以防卡死
            self.framwork.scroll_page(
                delta_x=0, delta_y=10000)  # 向下滚动页面10000像素
            element_text = None  # 提前赋值以完成判断

            try:
                element_text = self.framwork.find_element("B_mbw29p").inner_text(
                    timeout=1)  # 尝试检查页面最底部提示文字，最大等待时间设为1ms
            except:
                pass

            # 如果网络中断，点击刷新
            if element_text == "服务异常，重新刷新拉取数据":
                self.framwork.find_element("NLLHhkaY").click()

            # 如果出现页面最底部提示文字，跳出无限循环，否则继续循环
            elif element_text == "暂时没有更多了":
                break
            else:
                continue
