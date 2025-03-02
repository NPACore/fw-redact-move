exit 1 # dont actually run me
# fw-beta gear install -n deid-export -v latest
fw cp "fw://unknown/LTACH Swallow/LTACH001/SWALLOWING FUNCTION STUDY WITH VIDEO AND OR MODIFIED SWALLOW/Unknown_1/files/redacted_1.2.276.0.7230010.3.1.3.0.515.1740665514.879490.dcm" ./phi.dcm
dcm2pnm phi.dcm | magick convert pnm:- phi.jpg
# use gimp to make rect selection -> 'to path' -> export path:
#   creates ./box_path_center and ./box_path
#   0,0 to 180,166
