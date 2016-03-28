from suds.client import Client

boot_url = 'http://10.1.1.103:9623/'  # service address

#if __name__ == '__main__':
wsdl_url = '%scondorCollector.wsdl' % boot_url
collector = Client(wsdl_url, cache=None, location=boot_url)
# print(collector.service.getVersionString())
# print(collector)
