import v4l2
import fcntl


# list cameras
def list_devices():
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
    res.index = 0
    try:
      fcntl.ioctl(vd, v4l2.VIDIOC_ENUM_FRAMEINTERVALS, res)
    except:
      res = None
    # if res.type == v4l2.V4L2_FRMIVAL_TYPE_DISCRETE:
    #     print("ival: %d/%d" % (res.discrete.numerator, res.discrete.denominator))
    vd.close()
    return res

device = '/dev/video0'

pixfmtn = 0
frmsizen = 0
frmival = 0

pixfmt = get_camera_pixelformats(device, 0)
print("pixfmt: %s" % pixfmt.description)
frmsize = get_camera_framesize(device, pixfmt, 0)
print("frmsize: %d x %d" % (frmsize.discrete.height, frmsize.discrete.width))
frmival = get_camera_frameinterval(device, frmsize, 0)
print("ival: %d/%d" % (frmival.discrete.numerator, frmival.discrete.denominator))
