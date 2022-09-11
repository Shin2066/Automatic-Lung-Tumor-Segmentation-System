import glob
from pydicom import dcmread
from pydicom.pixel_data_handlers.util import apply_modality_lut
import matplotlib.pyplot as plt
from pathlib import Path

# dicom檔案轉bmp影像
def dicom_to_image(in_dir, out_dir, HU=False):
    file_list = glob.glob(in_dir + "/*.dcm")    # 讀資料夾內的檔案

    for index, path in enumerate(file_list):
        ds = dcmread(path)  # 讀dicom
        # print(ds) # 印出dicom內的所有屬性
        #file_name = ds.Modality + "_" + ds.SOPInstanceUID   # 保存影像用的檔名，可以自己改
        file_name =Path(path).stem
        
        if HU==True:
            hu_image = apply_modality_lut(ds.pixel_array, ds)

            vmin = ds.WindowCenter - ds.WindowWidth/2
            vmax = ds.WindowCenter + ds.WindowWidth/2

            plt.imsave((out_dir + "/" + file_name + ".bmp"), hu_image, cmap='gray', vmin=vmin, vmax=vmax)

        # 如果不轉換HU值
        else:
            plt.imsave((out_dir + "/" + file_name + ".bmp"), ds.pixel_array, cmap='gray')

        print(index+1, end="\r")

if __name__ == "__main__":
    dicom_to_image(in_dir=r"D:\UI\CAT-UNet\dcm_data",
                    out_dir=r"D:\UI\CAT-UNet\x_rays_data\val\images", HU=False)
