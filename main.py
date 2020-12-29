import sys
from spiders.jd_order_requests import JdSubscribe
from spiders.jd_seckill_requests import JdSeckill

if __name__ == '__main__':
    a = r"""
     ____.________            ________            .___                       _________              __   .__.__  .__   
    |    |\______ \           \_____  \_______  __| _/___________           /   _____/ ____   ____ |  | _|__|  | |  |  
    |    | |    |  \   ______  /   |   \_  __ \/ __ |/ __ \_  __ \  ______  \_____  \_/ __ \_/ ___\|  |/ /  |  | |  |  
/\__|    | |    `   \ /_____/ /    |    \  | \/ /_/ \  ___/|  | \/ /_____/  /        \  ___/\  \___|    <|  |  |_|  |__
\________|/_______  /         \_______  /__|  \____ |\___  >__|            /_______  /\___  >\___  >__|_ \__|____/____/
                  \/                  \/           \/    \/                        \/     \/     \/     \/             
功能列表：                                                                                
 1.预约商品
 2.秒杀抢购商品
    """
    print(a)

    choice_function = input('请选择:')
    if choice_function == '1':
        jd_subscribe = JdSubscribe()
        jd_subscribe.reserve()
    elif choice_function == '2':
        jd_seckill = JdSeckill()
        jd_seckill.seckill_by_proc_pool()
    else:
        print('没有此功能')
        sys.exit(1)
