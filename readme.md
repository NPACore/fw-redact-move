# redacting burnt in PHI (Censor)

 * [`find_and_move.py`](find_and_move.py) - copy redacted dicoms form `fw://unknown/LTACH Swallow` to `fw://mrrc/LTACH Swallow deID`. Redacted files created by the presidio-image-redactor gear.  Tries [deid-export](https://gitlab.com/flywheel-io/scientific-solutions/gears/deid-export)'s `find_or_create_container` to mirror subj,ses,and acq containers. File copy (link by ref?) unsolved. (dead code for upload)
 * [`deid.yaml`] - [deid-export](https://gitlab.com/flywheel-io/scientific-solutions/gears/deid-export) YAML file (missing `when` block?) for dicom pixel censoring using fixed box
  - syntax from deid -> [migration-toolkit:pixels](https://flywheel-io.gitlab.io/public/migration-toolkit/pages/pixels.html) -> [pydicom:deid:filters](https://pydicom.github.io/deid/user-docs/recipe-filters/)


## Notes
 * HPC nodes failing, missing mount? adjusted but still failing [0]
 * deid-export 1.7 busted [1]
 * deid-export 1.5 errors [2]
 * moving with [`find_and_move.py`](find_and_move.py): dont know how to copy without download/upload output of `presidio-image-redactorv0.1.1-rc.0`


[1]:
```
File "/venv/lib/python3.12/site-packages/flywheel_gear_toolkit/context/context.py", line 223, in init_logging
  if job_id := self.config_json.get("job", {}).get("id", {}):

               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
```

[2]:
```
 [2025-03-02 - DEBUG - fw_gear_deid_export.file_exporter:402] Downloading 1.2.276.0.7230010.3.1.3.0.515.1740675504.880114.dcm
[2025-03-02 - DEBUG - fw_gear_deid_export.file_exporter:406] Applying de-identfication template to /tmp/tmpnrli5j4h/1.2.276.0.7230010.3.1.3.0.515.1740675504.880114.dcm
[2025-03-02 - ERROR - fw_gear_deid_export.file_exporter:207] an exception was raised when de-identifying 1.2.276.0.7230010.3.1.3.0.515.1740675504.880114.dcm:
[2025-03-02 - ERROR - fw_gear_deid_export.file_exporter:418] can only concatenate str (not "NoneType") to str
Traceback (most recent call last):
  File "/flywheel/v0/fw_gear_deid_export/file_exporter.py", line 409, in deidentify
    deid_path = deidentify_file(
  File "/flywheel/v0/fw_gear_deid_export/deid_file.py", line 174, in deidentify_file
    deid_profile.process_file(src_fs=src_fs, src_file=basename, dst_fs=dst_fs)
  File "/usr/local/lib/python3.8/site-packages/flywheel_migration/deidentify/deid_profile.py", line 141, in process_file
    dst_path = profile.process_files(
  File "/usr/local/lib/python3.8/contextlib.py", line 75, in inner
    return func(*args, **kwds)
  File "/usr/local/lib/python3.8/site-packages/flywheel_migration/deidentify/dicom_file_profile.py", line 1060, in process_files
    super(DicomFileProfile, self).process_files(*args, **kwargs)
  File "/usr/local/lib/python3.8/site-packages/flywheel_migration/deidentify/file_profile.py", line 359, in process_files
    state = self.create_file_state()
  File "/usr/local/lib/python3.8/site-packages/flywheel_migration/deidentify/dicom_file_profile.py", line 511, in create_file_state
    path = self.parse_pixel_actions()
  File "/usr/local/lib/python3.8/site-packages/flywheel_migration/deidentify/dicom_file_profile.py", line 589, in parse_pixel_actions
    res += when
TypeError: can only concatenate str (not "NoneType") to str
 ```

[0]:
```
# Flywheel Job Log for 67c4b5d9ca8d69fdecbb7170
# Executor: node07, CPU: 16 cores, Memory: 135GB, Disk: 414TB, Swap: 13GB
# Gear starting...
# FATAL:   While checking container encryption: could not open image /raidzeus/flywheel/hpc/singularity/cache/cache/net/b0b2680224e50667aa827b8e8012a212fa69fc4027626422e200e4cbb4ee8519: image format not recognized
# 

ssh node07 file  /raidzeus/flywheel/hpc/singularity/cache/cache/net/b0b2680224e50667aa827b8e8012a212fa69fc4027626422e200e4cbb4ee8519
/raidzeus/flywheel/hpc/singularity/cache/cache/net/b0b2680224e50667aa827b8e8012a212fa69fc4027626422e200e4cbb4ee8519: gzip compressed data, from Unix, original size 1160365568

ssh node07 -- APPTAINER_CACHEDIR=/raidzeus/flywheel/hpc/singularity/cache singularity cache list -v |grep b0b26
b0b2680224e50667aa827b   2025-03-02 14:12:13    391.72 MiB       net

srun --nodes=1 --ntasks-per-node=1 --time=01:00:00 --pty file  /raidzeus/flywheel/hpc/singularity/cache/cache/net/b0b2680224e50667aa827b8e8012a212fa69fc4027626422e200e4cbb4ee8519
/raidzeus/flywheel/hpc/singularity/cache/cache/net/b0b2680224e50667aa827b8e8012a212fa69fc4027626422e200e4cbb4ee8519: gzip compressed data, from Unix, original size 1160365568


find /raidzeus/flywheel/hpc/singularity/cache/cache/ -type f -exec stat -c "%y %n" {} \+ |sort |tail -n2
2025-03-02 14:07:18.248980583 -0500 /raidzeus/flywheel/hpc/singularity/cache/cache/oci-tmp/e4d7bab5c12451b5b724b1a9182eb6c600a52543de98694e1c7af24934da7a24
2025-03-02 14:12:13.471288557 -0500 /raidzeus/flywheel/hpc/singularity/cache/cache/net/b0b2680224e50667aa827b8e8012a212fa69fc4027626422e200e4cbb4ee8519

singularity inspect  /raidzeus/flywheel/hpc/singularity/cache/cache/oci-tmp/e4d7bab5c12451b5b724b1a9182eb6c600a52543de98694e1c7af24934da7a24

io.buildah.version: 1.38.0
org.label-schema.build-arch: amd64
org.label-schema.build-date: Sunday_2_March_2025_14:6:58_EST
org.label-schema.schema-version: 1.0
org.label-schema.usage.apptainer.version: 1.3.3-1.el8
org.label-schema.usage.singularity.deffile.bootstrap: docker
org.label-schema.usage.singularity.deffile.from: us-docker.pkg.dev/flywheel-exchange/gear-exchange/flywheel-deid-export:1.7.0

singularity inspect  /raidzeus/flywheel/hpc/singularity/cache/cache/net/b0b2680224e50667aa827b8e8012a212fa69fc4027626422e200e4cbb4ee8519

FATAL:   Failed to open image /raidzeus/flywheel/hpc/singularity/cache/cache/net/b0b2680224e50667aa827b8e8012a212fa69fc4027626422e200e4cbb4ee8519: image format not recognized

```
