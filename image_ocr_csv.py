import pre_process_cut_Image as pc
import extraction as ext
import sys
path = sys.argv[1]
print(path)
pc.convert_img(path)
pc.cut_img(path)
ext.reg_dict(path + '\\static\\cutimg')
