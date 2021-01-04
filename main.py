import sys
from spiders.jd_order_requests import JdSubscribe
from spiders.jd_seckill_requests import JdSeckill
from spiders.jd_coupon_requests import JdCoupon

if __name__ == '__main__':
    a = r"""
     ____.________            ________            .___                       _________              __   .__.__  .__   
    |    |\______ \           \_____  \_______  __| _/___________           /   _____/ ____   ____ |  | _|__|  | |  |  
    |    | |    |  \   ______  /   |   \_  __ \/ __ |/ __ \_  __ \  ______  \_____  \_/ __ \_/ ___\|  |/ /  |  | |  |  
/\__|    | |    `   \ /_____/ /    |    \  | \/ /_/ \  ___/|  | \/ /_____/  /        \  ___/\  \___|    <|  |  |_|  |__
\________|/_______  /         \_______  /__|  \____ |\___  >__|            /_______  /\___  >\___  >__|_ \__|____/____/
                  \/                  \/           \/    \/                        \/     \/     \/     \/             
功能列表：                                                                                
 1.预约茅台
 2.秒杀茅台
 3.京东超级全城购，满199-198优惠券
 4.预约小米11白8G-256
 5.秒杀小米11白8G-256
    """
    print(a)

    choice_function = input('请选择:')
    if choice_function == '1':
        jd_subscribe = JdSubscribe()
        jd_subscribe.reserve()
    elif choice_function == '2':
        jd_seckill = JdSeckill()
        jd_seckill.seckill_by_proc_pool()
    elif choice_function == '3':
        jd_coupon = JdCoupon()
        jd_coupon.receive()
    elif choice_function == '4':
        jd_coupon = JdSubscribe()
        jd_coupon.reserve_xiaomi()
    elif choice_function == '5':
        jd_coupon = JdSeckill()
        jd_coupon.seckill_by_proc_pool_xiaomi()
    else:
        print('没有此功能')
        sys.exit(1)
