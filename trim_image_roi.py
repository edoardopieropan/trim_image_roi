import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from PIL import Image

image_path = "path/to/image.nii"
roi_path = "path/to/image_roi.nii"

def crop_image(img):
    assert(img.sum()!=0.0)

    left_border, right_border = 10000,0
    top_border,bottom_border = 10000,0

    for i in range(img.shape[2]): #for slice
        image_slice = img[:,:,i]
        image_slice = Image.fromarray(image_slice)
        for x in range(image_slice.size[0]): #for width
            for y in range(image_slice.size[1]): #for height
                col = image_slice.getpixel((x, y))
                if col != 0.0: #if color equal white
                    if x < left_border:
                        left_border=x
                    if x > right_border:
                        right_border=x
                    if y < top_border:
                        top_border = y
                    if y > bottom_border:
                        bottom_border = y

    final_image = np.zeros((bottom_border-top_border,right_border-left_border,img.shape[2]))

    for i in range(img.shape[2]):
        image_slice = img[:,:,i]
        image_slice = Image.fromarray(image_slice)
        image_crop = image_slice.crop((left_border, top_border, right_border, bottom_border)) 
        final_image[:,:,i]=image_crop
    return np.asarray(final_image)

img = nib.load(image_path)
img_data = img.get_fdata()
roi = nib.load(roi_path)
roi_data = roi.get_fdata()
img_data_roi = np.where(roi_data==1, img_data, 0)
img_cropped = crop_image(img_data_roi)

#visualize slices
fig = plt.figure()
plt.ion()
plt.show()
for j in range(img_cropped.shape[2]):
    if img_cropped[:,:,j].sum() != 0.0:
        plt.imshow(img_cropped[:,:,j],cmap = 'Greys')
        plt.title("slice "+str(j))
        plt.draw()

        plt.show()
        plt.pause(0.01)