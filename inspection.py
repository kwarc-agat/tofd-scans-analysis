import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

class Rectangle:
    def __init__(self, x1, y1, w1, h1):
        self.x = x1
        self.y = y1
        self.w = w1
        self.h = h1

def nothing(x):
    print(x)
def is_inside_joint(x, y, x_min, x_max, y_min, y_max):
    if(y<y_max and y>y_min and x<x_max and x>x_min):
        return True
    else:
        return False

def is_inside_joint(inner: Rectangle, outer: Rectangle) -> bool:
    if(inner.x >= outer.x and inner.y >= outer.y and
            (inner.x+inner.w) <= (outer.x+outer.w) and (inner.y+inner.h) <= (outer.y+outer.h)):
        return True
    else:
        return False


def check_histograms(img, x_max, y_max, w_max, h_max, roi_x_min, roi_x_max, roi_y_min, roi_y_max):
    height, width, channels = img.shape
    indication_surface_down = img[roi_y_max:height, x_max:x_max+w_max]
    indication_surface_up = img[80:roi_y_min, x_max:x_max+w_max] #górna część obrazu oobcięta SZTYWNO
    surface_down = img[roi_y_max:height, roi_x_min:roi_x_max] # próbka obrazu wzięta na SZTYWNO
    surface_up = img[80:roi_y_min, roi_x_min:roi_x_max] # górna część obrazu oobcięta SZTYWNO

    # cv.imshow("INDICATION DOWN", indication_surface_down)
    # cv.imshow("INDICATION UP", indication_surface_up)
    # cv.imshow("DOWN", surface_down)
    # cv.imshow("UP", surface_up)

    hist_indication_surface_down = cv.calcHist([indication_surface_down], [0], None, [256], [0,256])
    hist_indication_surface_up = cv.calcHist([indication_surface_up], [0], None, [256], [0,256])
    hist_surface_down = cv.calcHist([surface_down], [0], None, [256], [0,256])
    hist_surface_up = cv.calcHist([surface_up], [0], None, [256], [0,256])
    hists = [hist_indication_surface_up, hist_indication_surface_down, hist_surface_up, hist_surface_down]

    check_up = cv.compareHist(hist_surface_up, hist_indication_surface_up, cv.HISTCMP_CORREL)
    check_down = cv.compareHist(hist_surface_down, hist_indication_surface_down, cv.HISTCMP_CORREL)

    # hist=cv.calcHist([img], [0], None, [256], [0,256])
    # plt.plot(hist_indication_surface_down)
    # plt.show()

    # titles = ['UP', 'DOWN', 'IND_UP: '+str(check_up), 'IND_DOWN'+str(check_down)]
    # for i in range(4):
    #     plt.subplot(2, 2, i + 1)
    #     plt.plot(hists[i], 'gray')
    #     plt.title(titles[i])
    #     plt.xticks([])
    #     plt.yticks([])
    # plt.show()
    cv.imshow("INIT", img)
    cv.waitKey()
    if check_down<check_up and check_down<0.75:
        corrected_rect = [(x_max,y_max),(x_max+w_max,roi_y_max)]
    elif check_up<check_down and check_up<0.75:
        corrected_rect = [(x_max,roi_y_min),(x_max+w_max,y_max+h_max)]
    else:
        corrected_rect = [(x_max,y_max),(x_max+w_max,y_max+h_max)]

    return corrected_rect


def display_process(images):
    titles = ['ORIGINAL','FILTER', 'CANNY', 'DILATE', 'CONTOURS', 'SOBEL-COMBINED', 'CANNY']
    for i in range(5):
        plt.subplot(3, 2, i+1)
        plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([])
        plt.yticks([])
    plt.show()
def inspect(filepath, list_of_parameters):
    try:
        filter_size=list_of_parameters[0]
        canny_min=list_of_parameters[1]
        canny_max=list_of_parameters[2]
        dilation_kernel_size=list_of_parameters[3]
        dilation_it=list_of_parameters[4]
        roi_x_min=list_of_parameters[5]
        roi_x_max=list_of_parameters[6]
        roi_y_min=list_of_parameters[7]
        roi_y_max=list_of_parameters[8]
    except IndexError:
        filter_size = 7
        canny_min = 30
        canny_max = 255
        dilation_kernel_size = 3
        dilation_it = 4
        roi_x_min = 0
        roi_x_max = 500
        roi_y_min = 200
        roi_y_max = 335

    img = cv.imread(filepath)
    img_copy = img.copy()
    height, width, channels = img.shape
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    filter_img = cv.medianBlur(imgray,filter_size)
    # filter_img = cv.GaussianBlur(imgray,(5,5),0)
    # filter_img = cv.bilateralFilter(imgray,10,75,75)

    edges = cv.Canny(filter_img, canny_min,canny_max)

    kernel = np.ones((dilation_kernel_size,dilation_kernel_size), np.uint8)
    dilation = cv.dilate(edges, kernel, iterations=dilation_it)
    # dilation = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

    contours, hierarchy = cv.findContours(dilation, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = sorted(contours, reverse=1, key=cv.contourArea)

    number_of_recs=0
    all_recs=[]
    for i in range(len(contours)):
        x,y,w,h = cv.boundingRect(contours[i])
        if is_inside_joint(x, y, roi_x_min, roi_x_max, roi_y_min, roi_y_max):                              # KONTURY LEŻĄCE WEWNĄTRZ, ALE WNĘTRZE SZTYWNO ZDEFINIOWANE
            cv.drawContours(img, contours, i, (0, 0, 255), 1)                   #GORZEJ - SPRAWDZAM TYLKO CZY LEWY GÓRNY RÓG LEŻY WEWNĄTRZ XDXDXDXDXD
            cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)
            rec = Rectangle(x,y,w,h)
            all_recs.append(rec)
            number_of_recs+=1

    x_max = 0; y_max = 0; w_max = 0; h_max = 0  # NAJWIĘKSZY PROSTOKĄT WEWNĄTRZ
    for rec in all_recs:
        if rec.w*rec.h > w_max*h_max:
            x_max=rec.x
            y_max=rec.y
            w_max=rec.w
            h_max=rec.h

    images = [imgray, filter_img, edges, dilation, img]
    filepath_inspected = filepath.replace(".png", "_inspected.png")
    cv.imwrite(filepath_inspected, img)
    return x_max, y_max, w_max, h_max, filepath_inspected, images

# throwMe=[]
# x_max, y_max, w_max, h_max, filepath_inspected, images = inspect("images\\tofd_weld.png", throwMe)
