# -*- coding: utf-8 -*-
import sys

from spiders.tb_seckill_requests import TbSeckill

if __name__ == '__main__':
    a = r"""
  __ ___.                              .___                                           __   .__.__  .__   
_/  |\_ |__             ___________  __| _/___________            ______ ____   ____ |  | _|__|  | |  |  
\   __\ __ \   ______  /  _ \_  __ \/ __ |/ __ \_  __ \  ______  /  ___// __ \_/ ___\|  |/ /  |  | |  |  
 |  | | \_\ \ /_____/ (  <_> )  | \/ /_/ \  ___/|  | \/ /_____/  \___ \\  ___/\  \___|    <|  |  |_|  |__
 |__| |___  /          \____/|__|  \____ |\___  >__|            /____  >\___  >\___  >__|_ \__|____/____/
          \/                            \/    \/                     \/     \/     \/     \/             
 脚本要求安装playwright
 
 功能列表：                                                                                
 1.抢购茅台(需先把购物车清空，并把茅台添加到购物车中)
    """
    print(a)

    choice_function = input('请选择:')
    if choice_function == '1':
        jd_subscribe = TbSeckill()
        jd_subscribe.seckill()
    else:
        print('没有此功能')
        sys.exit(1)
