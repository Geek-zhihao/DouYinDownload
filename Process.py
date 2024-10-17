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
import os


class Process:
    def __init__(self, framwork: Chromium_Framwork) -> None:
        self.framwork = framwork

    def scroll_page_until_end(self):
        '''
        滚动页面直到最底部

        '''
        # 获取滚动容器的位置信息
        scrollable_element = self.framwork.page.query_selector(
            '#douyin-right-container')
        bounding_box = scrollable_element.bounding_box()

        # 将鼠标移动到该元素上
        self.framwork.page.mouse.move(
            bounding_box['x'] + bounding_box['width'] / 2, bounding_box['y'] + bounding_box['height'] / 2)

        # 无限循环以滚动页面
        while True:
            self.framwork.scroll_page(
                delta_x=0, delta_y=-100)  # 回滚100像素以防卡死
            self.framwork.scroll_page(
                delta_x=0, delta_y=10000)  # 向下滚动页面10000像素
            element_text = None  # 提前赋值以完成判断

            try:
                element_text = self.framwork.page.locator("xpath=/html/body/div[2]/div[1]/div[4]/div[2]/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div").inner_text(
                    timeout=100)  # 尝试检查页面最底部提示文字，最大等待时间设为100ms
            except:
                pass

            # 如果网络中断，点击刷新
            if element_text == "服务异常，重新刷新拉取数据":
                self.framwork.page.locator(
                    "xpath=/html/body/div[2]/div[1]/div[4]/div[2]/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div/div/span").click()

            # 如果出现页面最底部提示文字，跳出无限循环，否则继续循环
            elif element_text == "暂时没有更多了":
                break
            else:
                continue

    def preliminary_sort_json(file_path: str, new_file_path: str):
        '''
        初步整理json文件

        Args:
            file_path(str):原文件的路径
            new_file_path(str):新文件的保存路径
        '''
        # 打开原文件进行读取
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()

        data = '[' + data + ']'  # 在原文件开头和末尾加上[]，使json文件数据成为一个标准的列表
        data = data.replace(',\n]', '\n]')  # 将原文件最后一个元素后的,删除，使json数据格式正确

        # 先直接将数据写入文件，暂不考虑json格式排版问题
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(data)

        # 读取json文件中的数据
        with open(new_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        formatted_data = json.dumps(
            data, indent=4, ensure_ascii=False)  # 将数据转换为格式化的字符串

        # 将排版好的json数据写入文件里
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(formatted_data)

        os.remove(file_path)  # 将原文件删除，仅保留整理好的文件
        print(f"文件已成功格式化并保存到 {new_file_path}")

    def merge_and_deduplicate(data_file: str, new_fetch_file: str):
        '''
        合并和重复数据删除，将个人主页发布的新作品加入作品数据库，以aweme_id为主要关键词进行去重

        Args:
            data_file(str):个人所有作品数据文件路径
            new_fetch_file(str):新抓取的个人主页所有作品数据文件路径
        '''

        # 加载两个文件的内容
        with open(data_file, 'r', encoding='utf-8') as file:
            old_data = json.load(file)
        with open(new_fetch_file, 'r', encoding='utf-8') as file:
            new_data = json.load(file)

        # 创建一个字典来存储以 aweme_id 为键的数据
        unique_data = {}

        # 合并数据并去除重复项
        for item in old_data + new_data:
            if item['aweme_id'] not in unique_data:
                unique_data[item['aweme_id']] = item

        # 将字典转换回列表
        merged_data = list(unique_data.values())

        # 将结果写入新的 JSON 文件
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, ensure_ascii=False, indent=4)

        os.remove(new_fetch_file)  # 将原文件删除，仅保留整理好的文件
