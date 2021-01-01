import functools
import random
import time

from concurrent.futures import ProcessPoolExecutor

from config import global_config
from exception import SKException
from jd_logger import logger
from spiders.jd_login import SpiderSession, QrLogin
from timer import Timer
from util import (
    parse_json,
    wait_some_time,
)

"""京东抢购优惠券"""
class JdCoupon(object):
    def __init__(self):
        self.spider_session = SpiderSession()
        self.spider_session.load_cookies_from_local()

        self.qrlogin = QrLogin(self.spider_session)

        # 初始化信息
        self.sku_id = global_config.getRaw('config', 'sku_id')
        self.seckill_num = 2
        self.seckill_init_info = dict()
        self.seckill_url = dict()
        self.seckill_order_data = dict()
        self.timers = Timer()

        self.session = self.spider_session.get_session()
        self.user_agent = self.spider_session.user_agent
        self.nick_name = None

    def login_by_qrcode(self):
        """
        二维码登陆
        :return:
        """
        if self.qrlogin.is_login:
            logger.info('登录成功')
            return

        self.qrlogin.login_by_qrcode()

        if self.qrlogin.is_login:
            self.nick_name = self.get_username()
            self.spider_session.save_cookies_to_local(self.nick_name)
        else:
            raise SKException("二维码登录失败！")

    def check_login(func):
        """
        用户登陆态校验装饰器。若用户未登陆，则调用扫码登陆
        """

        @functools.wraps(func)
        def new_func(self, *args, **kwargs):
            if not self.qrlogin.is_login:
                logger.info("{0} 需登陆后调用，开始扫码登陆".format(func.__name__))
                self.login_by_qrcode()
            return func(self, *args, **kwargs)

        return new_func

    @check_login
    def receive(self, work_count=8):
        """
        领取优惠券，纯甄满199-198
        """
        with ProcessPoolExecutor(work_count) as pool:
            for i in range(work_count):
                pool.submit(self._receive)

    def _receive(self):
        """
        预约
        """
        while True:
            try:
                break_this_loop = self.make_reserve()
                if break_this_loop:
                    logger.info('退出领取')
                    break
            except Exception as e:
                logger.info('领券发生异常!', e)
            wait_some_time()

    def make_reserve(self):
        """优惠券领取"""
        activity_id = '3S53g25ji4mzEGVoeRiXxpmpAYjs'
        args = 'key%3D3CF9A614611B32207E8BBC194F3E5B7738A155696C5E3F56E9E0E07235F17D90F303B26F9C35123E006713687B01391C_babel%2CroleId%3DA0BAF3B922198E20E8A068B1FFD943ED_babel'
        # 在config.ini配置自己的 eid, fp
        eid = global_config.getRaw('config', 'eid')
        fp = global_config.getRaw('config', 'fp')
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://pro.jd.com/',
        }
        # https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%223S53g25ji4mzEGVoeRiXxpmpAYjs%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22key%3D3CF9A614611B32207E8BBC194F3E5B7738A155696C5E3F56E9E0E07235F17D90F303B26F9C35123E006713687B01391C_babel%2CroleId%3DA0BAF3B922198E20E8A068B1FFD943ED_babel%22%2C%22eid%22%3A%222LAFNHDGXK7DFUHSL7LM4ZJQYEH2HNFL6C4VKXRWHOQCHOF6QU5Z4OLVCZW2SVA7PO2JT5JFVY2GX2UVALF7FZ4MNQ%22%2C%22fp%22%3A%22e3e04bcb478bc50f19f40382fa45298f%22%2C%22pageClick%22%3A%22Babel_Coupon%22%2C%22mitemAddrId%22%3A%22%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%7D&screen=750*1334&client=wh5&clientVersion=1.0.0&sid=&uuid=&area=&loginType=3&callback=jsonp1
        url = 'https://api.m.jd.com/client.action?functionId=newBabelAwardCollection&body=%7B%22activityId%22%3A%22' + activity_id + '%22%2C%22scene%22%3A%221%22%2C%22args%22%3A%22' + args + '%22%2C%22eid%22%3A' + eid + '%2C%22fp%22%3A' + fp + '%2C%22pageClick%22%3A%22Babel_Coupon%22%2C%22mitemAddrId%22%3A%22%22%2C%22geo%22%3A%7B%22lng%22%3A%22%22%2C%22lat%22%3A%22%22%7D%7D&screen=750*1334&client=wh5&clientVersion=1.0.0&sid=&uuid=&area=&loginType=3&callback=jsonp1'
        resp = self.session.get(url=url, params=None, headers=headers)
        print(resp.url)
        resp_json = parse_json(resp.text)
        code = resp_json.get('code')
        if code == '1':
            logger.info('优惠券领取失败: {}'.format(resp_json.get('errmsg')))
        if code == '0':
            logger.info('优惠券领取结果: {}, {}'.format(resp_json.get('msg'), resp_json.get('subCodeMsg')))
        self.timers.start()
        break_flag = False
        return break_flag

    def get_username(self):
        """获取用户信息"""
        url = 'https://passport.jd.com/user/petName/getUserInfoForMiniJd.action'
        payload = {
            'callback': 'jQuery{}'.format(random.randint(1000000, 9999999)),
            '_': str(int(time.time() * 1000)),
        }
        headers = {
            'User-Agent': self.user_agent,
            'Referer': 'https://order.jd.com/center/list.action',
        }

        resp = self.session.get(url=url, params=payload, headers=headers)

        try_count = 5
        while not resp.text.startswith("jQuery"):
            try_count = try_count - 1
            if try_count > 0:
                resp = self.session.get(url=url, params=payload, headers=headers)
            else:
                break
            wait_some_time()
        # 响应中包含了许多用户信息，现在在其中返回昵称
        # jQuery2381773({"imgUrl":"//storage.360buyimg.com/i.imageUpload/xxx.jpg","lastLoginTime":"","nickName":"xxx","plusStatus":"0","realName":"xxx","userLevel":x,"userScoreVO":{"accountScore":xx,"activityScore":xx,"consumptionScore":xxxxx,"default":false,"financeScore":xxx,"pin":"xxx","riskScore":x,"totalScore":xxxxx}})
        return parse_json(resp.text).get('nickName')
