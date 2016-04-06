from suds.client import Client
# import logging
# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)

# boot_url = 'http://10.1.1.103:80/'
boot_url = 'http://10.1.1.103:9623/'

wsdl_url = '%scondorSchedd.wsdl' % boot_url
schedd = Client(wsdl_url, cache=None, location=boot_url)


# tran_status = schedd.service.beginTransaction(30)
# status_enum = schedd.factory.create("StatusCode")
# universe_enum = schedd.factory.create("UniverseType")
# if tran_status.status.code != status_enum.SUCCESS:
#     exit(1)
#
# schedd_tran = tran_status.transaction
# clu_id = schedd.service.newCluster(schedd_tran)
# job_id = schedd.service.newJob(schedd_tran, clu_id.integer)
# class_ad = schedd.service.createJobTemplate(clu_id.integer, job_id.integer, "whz",
#                                             universe_enum.VANILLA, "/bin/date", "+%m", "")
#
# schedd.service.submit(schedd_tran, clu_id.integer, job_id.integer, class_ad.classAd)
# schedd.service.commitTransaction(schedd_tran)
