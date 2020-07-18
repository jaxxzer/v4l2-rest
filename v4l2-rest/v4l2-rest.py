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
    res.index = index
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
while (pixfmt := get_camera_pixelformats(device, pixfmtn)) is not None:
    print("pixfmt: %s" % str(pixfmt.description))
    frmsizen = 0
    while (frmsize := get_camera_framesize(device, pixfmt, frmsizen)) is not None:
        print("frmsize: %d x %d" % (frmsize.discrete.height, frmsize.discrete.width))
        frmivaln = 0
        while (frmival := get_camera_frameinterval(device, frmsize, frmivaln)) is not None:
            print("ival: %d/%d" % (frmival.discrete.numerator, frmival.discrete.denominator))
            frmivaln = frmivaln + 1
        frmsizen = frmsizen + 1
    pixfmtn = pixfmtn + 1
