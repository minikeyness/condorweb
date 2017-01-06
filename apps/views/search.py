#-*- coding: UTF-8 -*-
import sys
from flask import Flask, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from apps.models import User
from flask import render_template, flash, redirect, session, url_for, request, g
from apps.webservice import schedd, collector, status_enum
import base64, os, re

reload(sys)
sys.setdefaultencoding('utf8')

search = Blueprint('search', __name__)
job_status_dict = {'1': 'Idle', '2': 'Running', '3': 'Removed',
                   '4': 'Completed', '5': 'Held', '6': 'Transferring Output', '7': 'Suspended'}


@search.route('/search/home')
def home():
    uname = "whz"
    user_name = "condor"
    str_query = '(Owner=?=' + '"' + user_name + '"' + ')'
    print(str_query)
    tran_status = schedd.service.beginTransaction(30)

    if tran_status.status.code != status_enum.SUCCESS:
        error = "无法创建服务,查询失败！"
        schedd.service.abortTransaction(tran_status.transaction)
        return render_template('search.html', errors=error)

    jobs = schedd.service.getJobAds(None, str_query)
    job_info = []
    classad_struct_array = jobs[1]

    if classad_struct_array is not None:
        item = classad_struct_array.item  # ClassAdStruct arrays

        print(item)

        for i in range(len(item)):
            class_ad_struct_item = item[i].item  # ClassAdStructAttr arrays
            job_info_item = {}       # used to store job information:clusterId, duration, run_time
            job_status = 0
            server_time = 0
            time_enter_current_status = 0
            duration = 0
            clu_id = 0

            for j in range(len(class_ad_struct_item)):
                if class_ad_struct_item[j].name == "ClusterId":
                    clu_id = class_ad_struct_item[j].value
                    job_info_item.setdefault('ClusterId', clu_id)

                if class_ad_struct_item[j].name == "duration":
                    duration = int(class_ad_struct_item[j].value)

                if class_ad_struct_item[j].name == "ServerTime":
                    server_time = class_ad_struct_item[j].value

                if class_ad_struct_item[j].name == "JobStatus" and job_status == 0:
                    job_status = class_ad_struct_item[j].value
                    job_info_item.setdefault('JobStatus', job_status_dict.get(job_status, None))

                if time_enter_current_status == 0 and class_ad_struct_item[j].name == "EnteredCurrentStatus" :
                    time_enter_current_status = class_ad_struct_item[j].value

            job_run_time = 0
            if job_status == "2" and duration != 0:  # representing running state
                rate = (int(server_time) - int(time_enter_current_status)) / duration
                job_info_item.setdefault("progress", str((rate * 100)) + '%')

            else:
                job_info_item.setdefault("progress", 0)

            if job_status == "4":
                result_files = schedd.service.listSpool(tran_status.transaction, int(clu_id), 0)
                result_files = result_files.info.item
                print(result_files)
                for out in result_files:
                    print(out)
                    if re.search(r"out$", out.name) is not None:
                        sta3 = schedd.service.getFile(tran_status.transaction, clu_id, 0, out.name, 0, out.size)
                        updir = os.path.join("upload", uname)
                        updir = os.path.join(updir, str(clu_id))
                        if not os.path.exists(updir):
                            os.mkdir(updir)
                        filewithpath = os.path.join(updir, out.name)
                        fp = open(filewithpath, 'wb')
                        fp.write(base64.decodestring(sta3.data))
                        job_info_item.setdefault("JobOut", out.name)
            else:
                job_info_item.setdefault("JobOut", '-----')

            job_info.append(job_info_item)
            print(job_info)

    schedd.service.commitTransaction(tran_status.transaction)

    return render_template('search.html', job_info=job_info)
