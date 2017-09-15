#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2017/9/15 下午12:17
# @Author : Matrix
# @Github : https://github.com/blackmatrix7/
# @Blog : http://www.cnblogs.com/blackmatrix/
# @File : huawei.py
# @Software: PyCharm
import gammu
from .isms import ISMSCenter
from config import current_config

__author__ = 'blackmatrix'


class HWSMSCenter(ISMSCenter):

    def __init__(self):
        self.state_machine = gammu.StateMachine()
        self.state_machine.ReadConfig(Filename=current_config['FILECONFIG'])
        # Connect to the phone
        self.state_machine.Init()

    def send_msg(self, targets, content):
        self.state_machine.GetSIMMS()

    def get_msg(self):
        pass


if __name__ == '__main__':
    pass