#!/usr/bin/env python3
"""
Copy redacted analysis to new project
Flywheel is suppose to be smart about copies -- files are not actually duplicated

https://flywheel.io/insights/research-data-management-resources/smart-copy-helps-flywheel-sites-share-and-manage-data-more-efficiently

--- the best way to censor PHI (de-ID) and move is likley wiht the 
  deid-export grear (?)
  it supports pixel censoring too.

https://docs.flywheel.io/admin/deid/#when-moving-between-projects-gear
>  Run the gear each time you upload data. This method creates 2 datasets in Flywheel, the original dataset with PHI and a second dataset that has been de-identified. Typically, the two datasets are in different projects.

https://gitlab.com/flywheel-io/flywheel-apps/fw-gear-deid-export

https://flywheel-io.gitlab.io/public/migration-toolkit/pages/pixels.html

https://gitlab.com/flywheel-io/scientific-solutions/gears/deid-export#:~:text=the%20resolver%20path%20of%20the%20destination%20project%20

"""
import logging
import os
import re
import sys

import flywheel  # pip install flywheel-sdk
# run 'pip install -r requirements.txt'
from fw_gear_deid_export.container_export import find_or_create_container

logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "DEBUG").upper(),
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")

fw = flywheel.Client()
# PHI = fw.projects.find_one("label==LTACH Swallow")
PHI = fw.get("67c0a7cf735c304fb0bb71f4") # direct access (when missing permission)
cen_proj = fw.projects.find_one("label=LTACH Swallow deID")

# for debugging, quickly get an acq:
#  acq = fw.get("67c07327f8480b82c2d61747").acquisitions()[0]
#  ses = acq.session

# all sessions that have PHI that will have been censored
phi_sess = fw.sessions.find(f"project.label={PHI.label}")

for ses in phi_sess:
    dest_subj = find_or_create_container(fw, ses.subject, dest_parent=cen_proj)
    dest_sess = find_or_create_container(fw, ses, dest_parent=dest_subj)
    for acq in ses.acquisitions():

        dest_acq = find_or_create_container(fw, acq, dest_parent=dest_sess)
        for fname in acq.get_files():
            if not re.search('redacted', fname.name):
                continue
            print(fname)
            dest_file = find_or_create_container(fw, fname, dest_parent=dest_acq)
            # does this check if already exists?
            print(dest_file)
            # just testing. exit all loops after first interation
            raise Exception("dont want to run on everyone yet")
            # we can update like
            #  dest_acq.update({'label': 'Unknown_WFMod'})
            # but this wont work for files
            #   dest_acq.update({'files': [fname]})
            # Detail: [{'type': 'extra_forbidden', 'loc': ['body', 'files'], 'msg': 'Extra inputs are not permitted', ...
            dest_file = fname # WARNING: not a copy!
            dest_file.parents.session = dest_sess.id
            dest_file.parents.subject = dest_sess.subject.id
            dest_file.parents.project  = cen_proj.id
            dest_file.copy_of = fname.id

            #
            from fw_gear_deid_export.uploader import Uploader
            up = Uploader(fw)
            up.upload(dest_acq, dest_file.name, dest_file.path)


