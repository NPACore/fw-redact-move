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
import flywheel  # pip install flywheel-sdk
import os
import re


logging.basicConfig(
        level=os.environ.get("LOGLEVEL", "DEBUG").upper(),
        format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")

fw = flywheel.Client()
# PHI = fw.projects.find_one("label==LTACH Swallow")
PHI = fw.get("67c0a7cf735c304fb0bb71f4") # direct access (when missing permission)
cen = fw.projects.find_one("label=LTACH Swallow deID")

acq = fw.get("67c07327f8480b82c2d61747").acquisitions()[0]

phi_sess = fw.sessions.find(f"project.label={PHI.label}")
for ses in phi_sess:
    for acq in ses.acquisitions():
        for fname in acq.get_files():
            if not re.search('redacted', fname.name):
                continue
            # TODO: check if fname in cen project?
            print(fname)
            # TODO: add to new container
            #       must crate new project/subj/sess/acq first?
            # https://gitlab.com/flywheel-io/scientific-solutions/gears/deid-export/-/blob/main/fw_gear_deid_export/container_export.py#L404
