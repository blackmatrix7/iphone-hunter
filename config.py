#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/7/31 下午10:19
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: config
# @Software: PyCharm
import os
from datetime import datetime
from toolkit import BaseConfig, get_current_config

__author__ = 'blackmatrix'


class CommonConfig(BaseConfig):

    # 项目路径
    PROJ_PATH = os.path.abspath('')
    # 接受预约邮件的邮箱
    EMAIL = 'xxxxxxxx@hotmail.com'
    # Cache
    CACHE_MEMCACHED_SERVERS = ['10.10.10.100:32770']
    # ServerChan
    SEC_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    # Apple Store Url
    APPLE_STORES_URL = 'https://reserve-prime.apple.com/CN/zh_CN/reserve/iPhone/stores.json'
    # iPhone库存
    IPHONE_MODELS_URL = 'https://reserve-prime.apple.com/CN/zh_CN/reserve/iPhone/availability.json'
    # iPhone 型号
    MODELS = {
        'iPhone Xs 银色 64GB': 'MT9Q2CH/A',
        'iPhone Xs 金色 64GB': 'MT9R2CH/A',
        'iPhone Xs 深空灰色 64GB': 'MT9P2CH/A',
        'iPhone Xs Max 深空灰色 256GB': 'MT742CH/A',
        'iPhone Xs Max 银色 256GB': 'MT742CH/A',
        'iPhone Xs Max 金色 256GB': 'MT762CH/A'
    }

    # 监控时间段
    WATCH_START = datetime.strptime('0:01:00', '%H:%M:%S').time()
    WATCH_END = datetime.strptime('23:59:59', '%H:%M:%S').time()
    # 购买者信息
    BUYERS = [
        {
            'first_name': '修智', 'last_name': '单', 'idcard': '12345678901',
            'city': '上海', 'stores': None, 'email': 'xxxxxxxxx@hotmail.com',
            'apple_id': 'xxxxxxxxxx', 'apple_id_pass': 'xxxxxxx',
            'models':
                [
                    {'model': 'iPhone Xs Max', 'color': '银色', 'space': '256GB', 'quantity': 1},
                    {'model': 'iPhone Xs Max', 'color': '金色', 'space': '256GB', 'quantity': 1},
                    {'model': 'iPhone Xs Max', 'color': '深空灰色', 'space': '256GB', 'quantity': 1},
                    # {'model': 'iPhone Xs', 'color': '银色', 'space': '64GB', 'quantity': 1},
                    # {'model': 'iPhone Xs', 'color': '金色', 'space': '64GB', 'quantity': 1},
                    # {'model': 'iPhone Xs', 'color': '深空灰色', 'space': '64GB', 'quantity': 1},
                ]
        }
    ]

    # Apple Xpath
    SELECT_QUANTITY = '//*[@id="quantity"]'
    SELECT_STORE = '//*[@id="anchor-store"]'
    # 跳转到登录页面
    BTN_TO_LOGIN = '//*[@id="pricebox"]/div[3]/div/p/button'
    # 登录页面
    APPLE_ID_XPATH = '//*[@id="appleId"]'
    APPLE_PASS_XPATH = '//*[@id="pwd"]'
    APPLE_LOGIN_XPATH = '//*[@id="sign-in"]'
    # 申请注册码页面
    SMS_CODE_XPATH = '//*[@id="form"]/div/div/div[2]/div/p/strong'
    PHONE_NUMBER_XPATH = '//*[@id="phoneNumber"]'
    REG_CODE_XPATH = '//*[@id="registrationCode"]'
    # 两个继续按钮，一个是需要发送短信的
    BTN_NEED_SEND_SMS_XPATH = '//*[@id="form"]/div/div/div[3]/div[3]/div/div/button'
    # 一个是不需要发送短信，直接输入注册码的
    BTN_NEED_REG_CODE_XPATH = '//*[@id="form"]/div/div/div[2]/div[2]/div/div/button'
    # 验证你的注册码。
    VALIDATE_REG_CODE = '//*[@id="main"]/section[1]/div/div/div/h1'
    # 错误的注册码
    ERR_REG_CODE = '//*[@id="registrationCode-error"]/div[2]'

    # 选择时间
    SELECT_TIME_XPATH = '//*[@id="timeslot"]'
    # 姓
    LAST_NAME_XPATH = '//*[@id="lastName"]'
    # 名
    FIRST_NAME_XPATH = '//*[@id="firstName"]'
    # 邮箱
    EMAIL_XPATH = '//*[@id="email"]'
    # 证件类型，只支持身份证照， idCardChina
    GOV_ID_TYPE_XPATH = '//*[@id="governmentIDType"]'
    # 身份证号
    GOV_ID_XPATH = '//*[@id="governmentID"]'
    # 预约
    BTN_BUY_XPATH = '//*[@id="pricebox"]/div[3]/div/p/button'

    # 申请帐号、邮箱、手机
    '''
    中国移动：(106) 5751-6068-401
    中国电信：(106) 5902-1005-6601
    中国联通：(106) 5502-1837-0001
    '''
    SEND_TO = '106550218370001'
    PHONE_NUMBER = '18888888888'

    APPLE_INDEX = 'https://www.apple.com/cn/'
    APPLE_FLYOUT_AJAX = 'https://www.apple.com/cn/shop/bag/flyout?apikey={}&l=https%3A%2F%2Fwww.apple.com%2Fcn%2F'
    APPLE_SING_IN = 'https://{}/cn/shop/sentryx/sign_in'

    API_KEY_XPATH = '//*[@name="ac-gn-store-key"]/@content'

    # selenium 配置
    # 全局超时时间
    TIME_OUT = 600
    # 轮询间隔
    POLL_FREQUENCY = 0.2
    # 进程数，不建议超过CPU核数
    MULTIPROCESSING = 1

    # GAMMU
    FILECONFIG = os.path.abspath('.gammurc')

    # RabbitMQ
    RABBITMQ_HOST = '127.0.0.1'
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = 'user'
    RABBITMQ_PASS = '123456'

    def get_buy_url(self, model, color, space):

        screen_size = {
            'iPhone 8': '4.7-英寸屏幕',
            'iPhone 8 Plus': '5.5-英寸屏幕',
            'iPhone X': '5.8-英寸显示屏',
        }.get(model, '5.8-英寸显示屏')

        buy_url = 'https://reserve-prime.apple.com/CN/zh_CN/reserve/{model_name}/availability?channel=1&' \
                  'appleCare=N&iPP=N&partNumber={model}&path=/cn/shop/buy-iphone/{model_url}/' \
                  '{screen_size}-{space}-{color}&rv=1'.format(model_name='iPhoneX' if model == 'iPhone X' else 'iPhone',
                                                              model=self.MODELS['{0} {1} {2}'.format(model, color, space)],
                                                              model_url=model.lower().replace(' ', '-'),
                                                              screen_size=screen_size, color=color, space=space)
        return buy_url


commoncfg = CommonConfig()

configs = {
    'default': commoncfg
}

# 读取配置文件的名称，在具体的应用中，可以从环境变量、命令行参数等位置获取配置文件名称
config_name = 'default'

current_config = get_current_config(configs, config_name)
