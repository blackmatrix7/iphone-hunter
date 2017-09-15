#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 21:25
# @Author  : BlackMatrix
# @Site : 
# @File : shoot.py
# @Software: PyCharm
import platform
from functools import partial
from extensions import rabbit
from selenium import webdriver
from config import current_config
from tookit import retry as default_retry
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import Select as DefaultSelect

__author__ = 'blackmatrix'

retry = partial(default_retry, max_retries=30, step=0.2)


class AutoTest:

    def __init__(self):
        # 初始化浏览器
        options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        if platform.system() == 'Darwin':
            executable_path = '{0}/{1}'.format(current_config.PROJ_PATH, 'chromedriver')
        else:
            executable_path = 'chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=options)
        self.driver.implicitly_wait(current_config['TIME_OUT'])
        self.driver.set_window_size(1024, 768)

    def element_monkey_patch(self, element):

        for attr in dir(self):
            if attr.startswith('wait_'):
                setattr(element, attr, partial(getattr(self, attr), parent=element))
        # 针对dom元素的部分操作，加入重试方法
        for attr in ('click', 'submit', 'clear', 'send_keys'):
            setattr(element, attr, retry()(getattr(element, attr)))

    def elements_monkey_patch(self, elements):
        try:
            iter(elements)
        except ValueError:
            elements = [elements]
        finally:
            for element in elements:
                self.element_monkey_patch(element)

    def wait_find_element_by_id(self, element_id, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_id(element_id))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_xpath(self, xpath, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_xpath(xpath))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_class_name(self, class_name, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_class_name(class_name))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_link_text(self, link_text, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_link_text(link_text))
        self.element_monkey_patch(element)
        return element

    def wait_find_element_by_name(self, name, parent=None):
        element = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_element_by_name(name))
        self.element_monkey_patch(element)
        return element

    def wait_find_elements_by_xpath(self, xpath, parent=None):
        elements = WebDriverWait(
            driver=parent or self.driver,
            timeout=current_config['TIME_OUT'],
            poll_frequency=current_config['POLL_FREQUENCY']
        ).until(lambda x: x.find_elements_by_xpath(xpath))
        self.elements_monkey_patch(elements)
        return elements


class Select(DefaultSelect):

    def __init__(self, webelement):
        super().__init__(webelement)

    def select_by_index(self, index):
        return retry(max_retries=30, step=0.5)(super().select_by_index)

    def select_by_value(self, value):
        return retry(max_retries=30, step=0.5)(super().select_by_value)

    def select_by_visible_text(self, text):
        return retry(max_retries=30, step=0.5)(super().select_by_visible_text)

    def deselect_all(self):
        return retry(max_retries=30, step=0.5)(super().deselect_all)

    def deselect_by_value(self, value):
        return retry(max_retries=30, step=0.5)(super().deselect_by_value)

    def deselect_by_index(self, index):
        return retry(max_retries=30, step=0.5)(super().deselect_by_index)

    def deselect_by_visible_text(self, text):
        return retry(max_retries=30, step=0.5)(super().deselect_by_visible_text)


class Shoot(AutoTest):

    def select_iphone(self, store):
        # 打开购买页面
        self.driver.get(current_config.get_buy_url(model='iPhone 8 Plus', color='深空灰色', space='256GB'))
        pass
        add_btn = self.wait_find_element_by_xpath('//*[@id="tabnav-dimensionCapacity"]')
        add_btn.click()
        pass
        self.driver.close()


def hunting():

    # 为每个进程单独打开一个浏览器
    shoot = Shoot()

    # 从消息队列获取订购信息，如果
    @rabbit.receive_from_rabbitmq(exchange_name='iphone', queue_name='stock', routing_key='apple')
    def start():
        shoot.select_iphone('R607')
        # apple_stores = falcon.get_apple_stores()
        # iphone_stock = falcon.search_iphone()
        # for watch_store_key, watch_store_value in iphone_stock.items():
        #     # TODO 判断库存是否有需要购买的型号
        #     pass
        # quick_buy.select_iphone('R607')
    start()


if __name__ == '__main__':
    pass