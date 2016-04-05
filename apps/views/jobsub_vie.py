from flask import Flask, Blueprint
from flask import render_template, flash, redirect, session, url_for, request, g
from apps.webservice import schedd, status_enum, universe_enum, hash_enum
import base64, os

jobsubmit = Blueprint('jobsubmit', __name__)


@jobsubmit.route("/manage/usermsg", methods=["GET"])
def usermessage():
    return render_template('jobmanage.html')


@jobsubmit.route("/manage/simple", methods=["GET", "POST"])
def simplesub():
    if request.method == 'GET':
        return render_template('jobsubmit.html')
    cmd = request.form["cmd_str"]
    par = request.form["para_str"]
    tran_status = schedd.service.beginTransaction(30)

    if tran_status.status.code != status_enum.SUCCESS:
        error = "无法创建服务，提交失败！"
        schedd.service.abortTransaction(tran_status.transaction)
        return render_template('jobsubmit.html', errors=error)

    clu_id = schedd.service.newCluster(tran_status.transaction)
    job_id = schedd.service.newJob(tran_status.transaction, clu_id.integer)
    class_ad = schedd.service.createJobTemplate(clu_id.integer, job_id.integer, "whz",
                                                universe_enum.VANILLA, cmd, par, "")

    if clu_id.status.code != status_enum.SUCCESS or job_id.status.code != status_enum.SUCCESS or\
            class_ad.status.code != status_enum.SUCCESS:
        error = "创建作业失败，提交失败！"
        schedd.service.abortTransaction(tran_status.transaction)
        return render_template('jobsubmit.html', errors=error)
    stat1 = schedd.service.submit(tran_status.transaction, clu_id.integer, job_id.integer, class_ad.classAd)
    stat2 = schedd.service.commitTransaction(tran_status.transaction)
    if stat1.status.code != status_enum.SUCCESS or stat2.code != status_enum.SUCCESS:
        error = "提交失败！"
        schedd.service.abortTransaction(tran_status.transaction)
        return render_template('jobsubmit.html', errors=error)
    else:
        succes = "提交成功！"
        return render_template('jobsubmit.html', succ=succes)


@jobsubmit.route("/manage/complex")
def complexsub():
    if request.method == 'GET':
        return render_template('jobcomplex.html')

    # tran_status = schedd.service.beginTransaction(30)
    # if tran_status.status.code != status_enum.SUCCESS:
    #     error = "无法创建服务，提交失败！"
    #     schedd.service.abortTransaction(tran_status.transaction)
    #     return render_template('jobcomplex.html', errors=error)
    #
    # clu_id = schedd.service.newCluster(tran_status.transaction)
    # job_id = schedd.service.newJob(tran_status.transaction, clu_id.integer)
    #
    # bta41 = open("bta4", mode="rb") # 作业文件
    # bta42 = base64.b64encode(bta41.read())
    # len_b = os.path.getsize("bta4")
    # sta1 = schedd.service.declareFile(tran_status.transaction, clu_id.integer, job_id.integer, "bta4", len_b, hash_enum.NOHASH, None)
    # sta2 = schedd.service.sendFile(tran_status.transaction, clu_id.integer, job_id.integer, "bta4", 0, bta42)
    # schedd.service.commitTransaction(tran_status.transaction)
    #
    # tran_status = schedd.service.beginTransaction(30)
    # mpi1 = open("mpiscript", mode="rb") # 作业文件
    # mpi2 = base64.b64encode(mpi1.read())
    # schedd.service.declareFile(tran_status.transaction, clu_id.integer, job_id.integer, "mpiscript", os.path.getsize("mpiscript"), hash_enum.NOHASH, "")
    # schedd.service.sendFile(tran_status.transaction, clu_id.integer, job_id.integer, "mpiscript", 0, mpi2)
    # schedd.service.commitTransaction(tran_status.transaction)
    #
    # tran_status = schedd.service.beginTransaction(30)
    # requiretment = "Userlog = mpi.log;Output= mpi.out.;Err= mpi.errors;machine_count= 4;" \
    #     "should_transfer_files= Yes;transfer_input_files= bta4;when_to_transfer_output = ON_EXIT"
    #
    # class_ad = schedd.service.createJobTemplate(clu_id.integer, job_id.integer, "condor",
    #                               universe_enum.PARALLEL, "mpiscript", "./bta4", requiretment)
    #
    # schedd.service.submit(tran_status.transaction, clu_id.integer, job_id.integer, class_ad.classAd)
    # schedd.service.commitTransaction(tran_status.transaction)
