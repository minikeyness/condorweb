from flask import Flask, Blueprint
from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from apps.webservice import schedd, status_enum, universe_enum, hash_enum
import base64, os, re

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


@jobsubmit.route("/manage/complex", methods=["GET", "POST"])
def complexsub():
    if request.method == 'GET':
        return render_template('jobcomplex.html')
    u_name = "whz" # current_user.user_name
    updir = os.path.join("upload", u_name)
    execp = request.form["exec_str"]
    parp = request.form["para_str"]
    files = []
    for etf in request.form:
        if re.match(r"^SWFUpload_\d+_\d+$", etf): # 隐藏域中的文件名称，已经上传的
            files.append(request.form[etf])

    tran_status = schedd.service.beginTransaction(30)
    if tran_status.status.code != status_enum.SUCCESS:
        error = "无法创建服务，提交失败！"
        schedd.service.abortTransaction(tran_status.transaction)
        return render_template('joberrors.html', errors=error)

    clu_id = schedd.service.newCluster(tran_status.transaction)
    job_id = schedd.service.newJob(tran_status.transaction, clu_id.integer)

    for af in files:
        bta41 = open(os.path.join(updir, af), mode="rb") # 作业文件
        bta42 = base64.b64encode(bta41.read())
        len_b = os.path.getsize(af)
        sta1 = schedd.service.declareFile(tran_status.transaction, clu_id.integer, job_id.integer, af, len_b, hash_enum.NOHASH, None)
        sta2 = schedd.service.sendFile(tran_status.transaction, clu_id.integer, job_id.integer, af, 0, bta42)

    requiretment = "Userlog = mpi.log;Output= mpi.out.;Err= mpi.errors;machine_count= 4;" \
        "should_transfer_files= Yes;transfer_input_files= bta4;when_to_transfer_output = ON_EXIT"

    class_ad = schedd.service.createJobTemplate(clu_id.integer, job_id.integer, "condor",
                                  universe_enum.PARALLEL, execp, parp, requiretment)

    schedd.service.submit(tran_status.transaction, clu_id.integer, job_id.integer, class_ad.classAd)
    schedd.service.commitTransaction(tran_status.transaction)

    error = "作业提交成功！"
    return render_template('joberrors.html', errors=error)


# 异步文件上传
@jobsubmit.route("/upload", methods=["POST"])
def fileupload():
    u_name = "whz" # current_user.user_name
    if not os.path.exists("upload"):
        os.mkdir("upload")
    updir = os.path.join("upload", u_name)
    if not os.path.exists(updir):
        os.mkdir(updir)
    uploaded_files = request.files.getlist("files")
    filenames = ""
    for afile in uploaded_files:
        if afile:
            filename = afile.filename
            afile.save(os.path.join(updir, filename))
            filenames = filename
    return jsonify(files=filenames)


# 异步文件删除
@jobsubmit.route("/delfile", methods=["POST"])
def deletefile():
    u_name = "whz" # current_user.user_name
    if not os.path.exists("upload"):
        return jsonify(status="nofile")
    updir = "upload/%s" % u_name
    if not os.path.exists(updir):
        return jsonify(status="nofile")
    filen = request.form["fname"]
    apath = os.path.join(updir, filen)
    if os.path.exists(apath) and os.path.isfile(apath):
        os.remove(apath)
    else:
        return jsonify(status="nofile")
    return jsonify(status="success")
