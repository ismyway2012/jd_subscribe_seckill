# -*- coding: utf-8 -*-
import json
from urllib.parse import  quote,urlencode
activity_id = '3S53g25ji4mzEGVoeRiXxpmpAYjs'
args = 'key=3CF9A614611B32207E8BBC194F3E5B7738A155696C5E3F56E9E0E07235F17D90F303B26F9C35123E006713687B01391C_babel,roleId=A0BAF3B922198E20E8A068B1FFD943ED_babel'
eid = '2LAFNHDGXK7DFUHSL7LM4ZJQYEH2HNFL6C4VKXRWHOQCHOF6QU5Z4OLVCZW2SVA7PO2JT5JFVY2GX2UVALF7FZ4MNQ'
fp = 'e3e04bcb478bc50f19f40382fa45298f'
body = {"activityId":"%s" % activity_id,"scene":"1","args":"%s" % args,"eid":"%s" % eid,"fp":"%s" % fp,"pageClick":"Babel_Coupon","mitemAddrId":"","geo":{"lng":"","lat":""}}
quote_body = quote(json.dumps(body))
print(quote_body)
