from flask import Flask, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from apps.models import User
from flask import render_template, flash, redirect, session, url_for, request, g
from apps.webservice import schedd, collector


search = Blueprint('search', __name__)
job_status_dict = {'1': 'Idle', '2': 'Running', '3': 'Removed',
                   '4': 'Completed', '5': 'Held', '6': 'Transferring Output', '7': 'Suspended'}


@search.route('/search/home')
def home():
    user_name = "condor"
    str_query = '(Owner=?=' + '"' + user_name + '"' + ')'
    print(str_query)
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

            for j in range(len(class_ad_struct_item)):
                if class_ad_struct_item[j].name == "ClusterId":
                    job_info_item.setdefault('ClusterId', class_ad_struct_item[j].value)

                if class_ad_struct_item[j].name == "duration":
                    duration = int(class_ad_struct_item[j].value)

                if class_ad_struct_item[j].name == "ServerTime":
                    server_time = class_ad_struct_item[j].value

                if class_ad_struct_item[j].name == "JobStatus" and job_status == 0:
                    job_status = class_ad_struct_item[j].value
                    job_info_item.setdefault('JobStatus', job_status_dict.get(job_status, None))

                if class_ad_struct_item[j].name == "EnteredCurrentStatus" and time_enter_current_status == 0:
                    time_enter_current_status = class_ad_struct_item[j].value

            job_run_time = 0
            if job_status == "2" and duration != 0:  # representing running state
                rate = (int(server_time) - int(time_enter_current_status)) / duration
                job_info_item.setdefault("progress", str((rate * 100)) + '%' )

            else:
                job_info_item.setdefault("progress", 0)

            job_info.append(job_info_item)

    print(job_info)

    return render_template('search.html', job_info = job_info)
