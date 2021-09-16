from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# g(i,j) = α⋅f(i,j) + β
# α - Control contrast
# β - Control brightness

def lighten_img(pixels):
    # brightening scaler
    beta = 40
    
    dupPixels = pixels.copy()
    threshold = 255 - beta
    dupPixels[dupPixels > threshold] = 255
    dupPixels[dupPixels <= threshold] += beta  
        
    return dupPixels

def contrast_img(pixels):
    # contrast scaler
    alpha = 1.5
    
    dupPixels = pixels.copy()
    dupPixels = np.where(dupPixels * alpha <= 255, dupPixels * alpha, 255)
    dupPixels = dupPixels.astype('uint8')
    
    return dupPixels
    
def rgb2gray(pixels):
    dupPixels = pixels.copy()
    r, g, b = dupPixels[:,:,0], dupPixels[:,:,1], dupPixels[:,:,2]
    gray_scaler = 0.2989 * r + 0.5870 * g + 0.1140 * b
    dupPixels[:,:,0], dupPixels[:,:,1], dupPixels[:,:,2] = gray_scaler, gray_scaler, gray_scaler
    return dupPixels
        
def horizontal_flip(pixels):
    dupPixels = pixels.copy()
    for i in range(dupPixels.shape[0] // 2):
        c = dupPixels[i, :, :].copy()
        dupPixels[i, :, :] = dupPixels[dupPixels.shape[0] - i - 1, :, :]
        dupPixels[dupPixels.shape[0] - i - 1, :, :] = c
    return dupPixels

def vertical_flip(pixels):
    dupPixels = pixels.copy()
    for i in range(dupPixels.shape[1] // 2):
        r = dupPixels[:, i, :].copy()
        dupPixels[:, i, :] = dupPixels[:, dupPixels.shape[1] - i - 1, :]
        dupPixels[:, dupPixels.shape[1] - i - 1, :] = r
    return dupPixels

def blend_2_images():
    lena_img = np.array(Image.open(r"./gray.png"))
    img = np.array(Image.open(r"./flower.png"))
    blendPixels = (lena_img * 0.4 + img * 0.6).astype(np.uint8)
    return blendPixels

def gaussian_blur(pixels):
    gaussian_kernel = (1/ 16.0) * np.array([
        [1.0, 2.0, 1.0],
        [2.0, 4.0, 2.0], 
        [1.0, 2.0, 1.0]
    ])
    
    blur_pixels = []
    for y in range(3):
        temp = pixels.copy()
        temp = np.roll(temp, y - 1, axis = 0) # axis 0 represents rows, -1 shifted up, 1 shifted down
        for x in range(3):
            temp_x = temp.copy()
            temp_x = np.roll(temp_x, x - 1, axis = 1) * gaussian_kernel[y, x] # axis 1 represents columns, -1 shifted left, 1 shifted right
            blur_pixels.append(temp_x)
    
    blur_pixels = np.array(blur_pixels).astype('uint8')
    blur_pixels_sum = np.sum(blur_pixels, axis = 0)        
    return blur_pixels_sum
                  
def main():
    img = Image.open(r"./sample.png")
    
    # convert image to numpy array 
    pixels = np.array(img)
    # print(pixels)
    
    # shape is a tuple of (row (height), column (width), color (3))
    print(pixels.shape)
    

    # lighten image
    lighten_pixels = lighten_img(pixels)
    plt.imshow(lighten_pixels)
    plt.show()
    img = Image.fromarray(lighten_pixels).save("brightness.png")

    # contrast image
    contrast_pixels = contrast_img(pixels)
    plt.imshow(contrast_pixels)
    plt.show()
    img = Image.fromarray(contrast_pixels).save("contrast.png")
    
    # rgb to gray
    gray_pixels = rgb2gray(pixels)
    plt.imshow(gray_pixels)
    plt.show()
    img = Image.fromarray(gray_pixels).save("gray.png")
    
    # horizontally flip image - x axis
    horiz_pixels = horizontal_flip(pixels)
    plt.imshow(horiz_pixels)
    plt.show()
    img = Image.fromarray(horiz_pixels).save("horizontal_rotate.png")
    
    # vertically flip image - y axis
    vert_pixels = vertical_flip(pixels)
    plt.imshow(vert_pixels)
    plt.show()
    img = Image.fromarray(vert_pixels).save("vertical_rotate.png")
    
    # blending 2 images
    blend_pixels = blend_2_images()
    plt.imshow(blend_pixels)
    plt.show()
    img = Image.fromarray(blend_pixels).save("blended.png")
    
    # gaussian blur image
    blur_pixels = np.array(gaussian_blur(pixels)).astype('uint8')
    plt.imshow(blur_pixels)
    plt.show()
    img = Image.fromarray(blur_pixels).save("blur.png")
    
if __name__ == '__main__':
    main()