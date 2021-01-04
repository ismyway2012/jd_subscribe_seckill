# -*- coding: utf-8 -*-

from playwright import sync_playwright
from playwright_stealth import stealth_sync

from jd_logger import logger

playwright = sync_playwright().start()

from util import (
    wait_some_time,
    open_image
)


class TbSeckill(object):
    def __init__(self):
        # 初始化信息
        self.executablePath = 'C:\\Google\\Chrome\\Application\\chrome.exe'
        self.args = ['--no-sandbox', '--disable-infobars', '--lang=zh-CN', '--window-size=1920,1080', '--start-maximized']
        self.ignoreDefaultArgs = ['--enable-automation']

        self.qr_code_img = './qrcode-img.png'
        self.max_retry = 100

    def seckill(self):
        browser = playwright.chromium.launch(executablePath=self.executablePath, args=self.args, ignoreDefaultArgs=self.ignoreDefaultArgs, headless=False)
        page = browser.newPage()
        stealth_sync(page)

        self.login_tb(page)
        page.click('#J_SelectAll1')
        page.waitForTimeout(1000)
        page.click('#J_Go')
        page.waitForTimeout(50)
        current_time = 0
        while not page.querySelector('.go-btn'):
            page.reload()
            page.waitForTimeout(100)
            if current_time > self.max_retry:
                break
            current_time = current_time + 1

        a_submit = page.querySelector('.go-btn')
        a_submit.click()

        browser.close()
        playwright.stop()

    def login_tb(self, page):
        page.waitForTimeout(2000)
        page.goto('https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fcart.taobao.com%2Fcart.htm%3F%26from%3Dmini')
        page.waitForSelector('.icon-qrcode')
        page.click('.icon-qrcode')
        page.waitForSelector('.qrcode-img')
        qrcode_div = page.querySelector('.qrcode-img')
        qrcode_div.screenshot(path=self.qr_code_img)
        open_image(self.qr_code_img)
        page.waitForSelector('#J_OrderList')
        if page.querySelector('#J_OrderList'):
            print('进入购物车成功')

    def _seckill(self):
        """
        抢购
        """
        while True:
            try:
                pass
            except Exception as e:
                logger.info('抢购发生异常，稍后继续执行！', e)
            wait_some_time()
