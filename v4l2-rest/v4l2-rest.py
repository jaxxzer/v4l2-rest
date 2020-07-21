import v4l2
import fcntl
import json
# from ctypes_json import CDataJSONEncoder

from bottle import route, run

# list cameras
def list_devices():
  return None

def get_camera_settings(device):
  return None


# get camera pixelformats
def get_camera_pixelformats(device, index):
  vd = open(device)
  res = v4l2.v4l2_fmtdesc()
  res.type = v4l2.V4L2_BUF_TYPE_VIDEO_CAPTURE
  res.index = index
  try:
    fcntl.ioctl(vd, v4l2.VIDIOC_ENUM_FMT, res)
  except:
    res = None
  vd.close()
  return res

# get camera framesizes
def get_camera_framesize(device, fmtdesc, index):
    vd = open(device)
    res = v4l2.v4l2_frmsizeenum()
    res.pixel_format = fmtdesc.pixelformat
    res.index = index
    try:
      fcntl.ioctl(vd, v4l2.VIDIOC_ENUM_FRAMESIZES, res)
    except:
      res = None
    # if res.type == v4l2.V4L2_FRMSIZE_TYPE_DISCRETE:
    #     print(res.discrete.height)
    vd.close()
    return res

# get camera framerates
def get_camera_frameinterval(device, frmsizeenum, index):
    vd = open(device)
    res = v4l2.v4l2_frmivalenum()
    res.pixel_format = frmsizeenum.pixel_format
    res.height = frmsizeenum.discrete.height
    res.width = frmsizeenum.discrete.width
    res.index = index
    try:
      fcntl.ioctl(vd, v4l2.VIDIOC_ENUM_FRAMEINTERVALS, res)
    except:
      res = None
    # if res.type == v4l2.V4L2_FRMIVAL_TYPE_DISCRETE:
    #     print("ival: %d/%d" % (res.discrete.numerator, res.discrete.denominator))
    vd.close()
    return res

# device = '/dev/video2'


# ```
# 0: {
#     pixformat:
#     description:
#     framesizes:
#     [
#         0: {
#             type:
#             height:
#             width:
#             frameintervals: [
#                 0: {
#                     type:
#                     numerator:
#                     denomintator:
#                 }

#             ]
#         }
#     ]
# }
# ```
@route("/camera/settings/<device>")
def get_camera_formats(device):
  device = "/dev/video" + device
  formats = {}
  pixfmtn = 0
  pixfmt = get_camera_pixelformats(device, pixfmtn)
  while pixfmt is not None:
      print("pixfmt: %s" % str(pixfmt.description))
      #print(json.dumps(pixfmt, cls=CDataJSONEncoder))
      formats[pixfmtn] = {}
      formats[pixfmtn]["description"] = pixfmt.description.decode('utf-8')
      frmsizes = {}
      frmsizen = 0
      frmsize = get_camera_framesize(device, pixfmt, frmsizen)
      while frmsize is not None:
          frmsizes[frmsizen] = {}
          if frmsize.type == v4l2.V4L2_FRMSIZE_TYPE_DISCRETE:
            print("frmsize: %d x %d" % (frmsize.discrete.height, frmsize.discrete.width))
            frmsizes[frmsizen]["height"] = frmsize.discrete.height
            frmsizes[frmsizen]["width"] = frmsize.discrete.width
          elif frmsize.type == v4l2.V4L2_FRMSIZE_TYPE_STEPWISE:
            print("frmsize: %d x %d -> %d x %d" % (frmsize.stepwise.min_width, frmsize.stepwise.min_height, frmsize.stepwise.max_width, frmsize.stepwise.max_height))
            frmsizes[frmsizen]["height"] = frmsize.stepwise.max_height
            frmsizes[frmsizen]["width"] = frmsize.stepwise.max_width
          #print(json.dumps(frmsize, cls=CDataJSONEncoder))

          frmivals = {}
          frmivaln = 0
          frmival = get_camera_frameinterval(device, frmsize, frmivaln)
          while frmival is not None:
            if frmival.type == v4l2.V4L2_FRMIVAL_TYPE_DISCRETE:
              print("ival: %d/%d" % (frmival.discrete.numerator, frmival.discrete.denominator))
            elif frmsize.type == v4l2.V4L2_FRMIVAL_TYPE_STEPWISE:
              print("ival: %d/%d -> %d/%d" % (frmival.stepwise.min.numerator, frmival.stepwise.min.denominator, frmival.stepwise.max.numerator, frmival.stepwise.max.denominator))
              #print(json.dumps(frmival, cls=CDataJSONEncoder))
            frmivals[frmivaln] = {}
            frmivals[frmivaln]["numerator"] = frmival.discrete.numerator
            frmivals[frmivaln]["denominator"] = frmival.discrete.denominator
            frmivaln = frmivaln + 1
            frmival = get_camera_frameinterval(device, frmsize, frmivaln)
          frmsizes[frmsizen]["intervals"] = frmivals
          frmsizen = frmsizen + 1
          frmsize = get_camera_framesize(device, pixfmt, frmsizen)
      formats[pixfmtn]["framesizes"] = frmsizes
      pixfmtn = pixfmtn + 1
      pixfmt = get_camera_pixelformats(device, pixfmtn)

  return json.dumps(formats, indent=4)

#print(formats)
#print(json.dumps(formats, indent=2))

run(host="localhost", port=8888)
