#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/9/5 21:25
# @Author  : BlackMatrix
# @Site : 
# @File : shoot.py
# @Software: PyCharm
import platform
from time import sleep
from tookit import retry
from functools import partial
from selenium import webdriver
from operator import itemgetter
from config import current_config
from extensions import rabbit, cache
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import Select as DefaultSelect

__author__ = 'blackmatrix'

custom_retry = partial(retry, max_retries=30, step=0.2)


class ErrorBuy(Exception):
    pass


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
        self.driver.set_window_size(1440, 900)

    def element_monkey_patch(self, element):

        for attr in dir(self):
            if attr.startswith('wait_'):
                setattr(element, attr, partial(getattr(self, attr), parent=element))
        # 针对dom元素的部分操作，加入重试方法
        for attr in ('click', 'submit', 'clear', 'send_keys'):
            setattr(element, attr, custom_retry()(getattr(element, attr)))

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

    def is_elements_by_xpath(self, xpath):
        """
        判断元素是否存在，有个2秒的延迟。
        :param xpath:
        :return:
        """
        try:
            WebDriverWait(
                driver=self.driver,
                timeout=1,
                poll_frequency=current_config['POLL_FREQUENCY']
            ).until(lambda x: x.find_elements_by_xpath(xpath))
            return True
        except ElementNotVisibleException:
            return False


class Select(DefaultSelect):

    def __init__(self, webelement):
        super().__init__(webelement)

    def select_by_index(self, index):
        return custom_retry()(super(Select, self).select_by_index)(index)

    def select_by_value(self, value):
        return custom_retry()(super(Select, self).select_by_value)(value)

    def select_by_visible_text(self, text):
        return custom_retry()(super(Select, self).select_by_visible_text)(text)

    def deselect_all(self):
        return custom_retry()(super().deselect_all)()

    def deselect_by_value(self, value):
        return custom_retry()(super().deselect_by_value)(value)

    def deselect_by_index(self, index):
        return custom_retry()(super().deselect_by_index)(index)

    def deselect_by_visible_text(self, text):
        return custom_retry()(super().deselect_by_visible_text)(text)


class Shoot(AutoTest):

    def __init__(self):
        self.model = None
        self.color = None
        self.space = None
        self.store = None
        self.first_name = None
        self.last_name = None
        self.idcard = None
        self.quantity = None
        self.send_message = partial(rabbit.send_message, exchange_name='iphone', queue_name='sms')
        super().__init__()

    @retry(max_retries=5, delay=1)
    def select_iphone(self, model, color, space, store, first_name, last_name, idcard, quantity):
        self.model = model
        self.color = color
        self.space = space
        self.store = store
        self.first_name = first_name
        self.last_name = last_name
        self.idcard = idcard
        self.quantity = quantity
        # 打开购买页面
        self.driver.get(current_config.get_buy_url(model=model, color=color, space=space))
        # 数量
        select_quantity = Select(self.wait_find_element_by_xpath(current_config.SELECT_QUANTITY))
        select_quantity.select_by_value(str(quantity))
        # 零售店
        select_store = Select(self.wait_find_element_by_xpath(current_config['SELECT_STORE']))
        select_store.select_by_value(store)
        # 继续
        btn_to_login = self.wait_find_element_by_xpath(current_config['BTN_TO_LOGIN'])
        btn_to_login.click()

    @retry(max_retries=5, delay=1)
    def login_apple_id(self):
        # 如果无需登录则直接购买
        if 'signin.apple.com' not in self.driver.current_url:
            self.send_reg_code()
        else:
            # 切换到iframe
            iframe = self.wait_find_element_by_xpath('//*[@id="aid-auth-widget-iFrame"]')
            self.driver.switch_to.frame(iframe)
            # 帐号
            input_apple_id = self.wait_find_element_by_xpath(current_config.APPLE_ID_XPATH)
            input_apple_id.send_keys(current_config.APPLE_ID)
            # 密码
            input_apple_pwd = self.wait_find_element_by_xpath(current_config.APPLE_PASS_XPATH)
            input_apple_pwd.send_keys(current_config.APPLE_ID_PASS)
            # 登录
            btn_login = self.wait_find_element_by_xpath(current_config.APPLE_LOGIN_XPATH)
            btn_login.click()
            self.send_reg_code()

    @retry(max_retries=5, delay=1)
    def send_reg_code(self):
        """
        申请注册码
        :return:
        """
        # 注册码
        reg_code = '123456'
        # 手机号
        phone_number = '18858888888'
        validate_reg_code = self.wait_find_element_by_xpath(current_config.VALIDATE_REG_CODE)
        BTN_CONTINUE = current_config.BTN_NEED_REG_CODE_XPATH
        # 需要申请注册码的情况
        if validate_reg_code.text == '申请并验证你的注册码。':
            BTN_CONTINUE = current_config.BTN_NEED_SEND_SMS_XPATH
            # 验证码
            sms_code = self.wait_find_element_by_xpath(current_config.SMS_CODE_XPATH)
            # 发送短信
            rabbit.connect()
            self.send_message(messages={'content': sms_code.text,
                                        'target': current_config.SEND_TO,
                                        'apple_id': current_config.APPLE_ID})
            rabbit.disconnect()
        # 遍历获取缓存注册码
        while True:
            sms_list = cache.get(current_config.APPLE_ID)
            if sms_list:
                break
        # 排序
        sms_list.sort(key=itemgetter('datetime'))
        for sms in sms_list:
            if '注册码' in sms['text']:
                phone_number = sms['send_from']
                reg_code = sms['text'][6:15]
        # 填写手机号码
        input_phone_number = self.wait_find_element_by_xpath(current_config.PHONE_NUMBER_XPATH)
        input_phone_number.clear()
        input_phone_number.send_keys(phone_number)
        # 填写注册码
        input_reg_code = self.wait_find_element_by_xpath(current_config.REG_CODE_XPATH)
        input_reg_code.clear()
        input_reg_code.send_keys(reg_code)
        # 继续
        btn_continue = self.wait_find_element_by_xpath(BTN_CONTINUE)
        btn_continue.click()
        # 如果出现注册码错误，清理缓存并重试
        # if self.is_elements_by_xpath(current_config.ERR_REG_CODE):
        #     err_reg_code = self.wait_find_element_by_xpath(current_config.ERR_REG_CODE)
        #     if err_reg_code.is_displayed() is True:
        #         cache.delete(current_config.APPLE_ID)
        #         raise ErrorBuy
        self.last_step()

    @retry(max_retries=5, delay=1)
    def last_step(self):
        select_time = Select(self.wait_find_element_by_xpath(current_config.SELECT_TIME_XPATH))
        select_time.select_by_visible_text('下午 9:00 - 下午 9:30')
        input_last_name = self.wait_find_element_by_xpath(current_config.LAST_NAME_XPATH)
        input_last_name.clear()
        input_last_name.send_keys(self.last_name)
        input_first_name = self.wait_find_element_by_xpath(current_config.FIRST_NAME_XPATH)
        input_first_name.clear()
        input_first_name.send_keys(self.first_name)
        input_email = self.wait_find_element_by_xpath(current_config.EMAIL_XPATH)
        input_email.clear()
        input_email.send_keys(current_config.APPLE_ID)
        select_idcard = Select(self.wait_find_element_by_xpath(current_config.GOV_ID_TYPE_XPATH))
        select_idcard.select_by_value('idCardChina')
        input_idcard = self.wait_find_element_by_xpath(current_config.GOV_ID_XPATH)
        input_idcard.clear()
        input_idcard.send_keys(self.idcard)
        btn_buy = self.wait_find_element_by_xpath(current_config.BTN_BUY_XPATH)
        btn_buy.click()



def hunting():

    # 为每个进程单独打开一个浏览器
    shoot = Shoot()

    # 从消息队列获取订购信息，如果
    # @rabbit.receive_from_rabbitmq(exchange_name='iphone', queue_name='stock', routing_key='apple')
    def start():
        shoot.select_iphone(model='iPhone 8', color='深空灰色', space='64GB', store='R581',
                            first_name='三', last_name='张', idcard='123456789', quantity=2)
        shoot.login_apple_id()
        # apple_stores = falcon.get_apple_stores()
        # iphone_stock = falcon.search_iphone()
        # for watch_store_key, watch_store_value in iphone_stock.items():
        #     # TODO 判断库存是否有需要购买的型号
        #     pass
        # quick_buy.select_iphone('R607')
    start()


if __name__ == '__main__':
    pass
