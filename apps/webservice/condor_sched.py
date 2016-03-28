from suds.client import Client

# import logging
# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)

# boot_url = 'http://10.1.1.103:80/'
boot_url = 'http://10.1.1.103:9623/'

#if __name__ == '__main__':
# wsdl_url = '%swebservice/condorSchedd.wsdl' % boot_url   # 通过webservice获取wsdl,
# schedd = Client(wsdl_url, cache=None)                  # 使用wdls定义的Service address

wsdl_url = '%scondorSchedd.wsdl' % boot_url     # 直接通过service获取wsdl，但是不知道service的端口是否是一直固定的
schedd = Client(wsdl_url, cache=None, location=boot_url)  # 覆盖wsdl自定义的service address
# print(schedd)
# print(collector.service.getPlatformString())
# collector.service.removeJob()

