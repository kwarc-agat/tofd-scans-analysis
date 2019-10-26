import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from statistics import stdev

class Rectangle:
    def __init__(self, x1, y1, w1, h1):
        self.x = x1
        self.y = y1
        self.w = w1
        self.h = h1
        self.is_surface_breaking=False
        self.is_acceptable=True
    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+"),"+str(self.w)+"x"+str(self.h)\
               +", Surface: "+str(self.is_surface_breaking)+", Acceptance: "+str(self.is_acceptable)


def nothing(x):
    print("Nothing:"+str(x))


def is_inside_joint(inner: Rectangle, outer: Rectangle) -> bool:
    if(inner.x >= outer.x and inner.y >= outer.y and
            (inner.x+inner.w) <= (outer.x+outer.w) and (inner.y+inner.h) <= (outer.y+outer.h)):
        return True
    else:
        return False


def copy_list_without_elem(elem, list):
   copy_list=[]
   for e in list:
      if e!=elem:
         copy_list.append(e)
   return copy_list


def do_overlap(rec1:Rectangle, rec2:Rectangle):

    if rec1.x>(rec2.x+rec2.w) or rec2.x>(rec1.x+rec1.w):
        print("left side")
        return False
    if rec1.y<(rec2.y+rec2.h) or rec2.y<(rec1.y+rec1.h):
        print("above")
        return False
    print("IT OVERLAPPED")
    return True


def do_overlap_whole_list(list):
    if list!=[]:
        for i in range(len(list)):
            for j in range(i, len(list)):
                if do_overlap(list[i], list[j])==True:
                    return True
        return False
    return True

def check_recs_ove_recs(all_recs):
    corrected_recs = []
    while do_overlap_whole_list(corrected_recs):
        corrected_recs = []
        for rec in all_recs:
            copy_list = all_recs
            for r in copy_list:
                if do_overlap(rec, r):
                    x1 = min(rec.x, r.x)
                    y1 = min(rec.y, r.y)
                    x2 = max(rec.x + rec.w, r.x + r.w)
                    y2 = max(rec.y + rec.h, r.y + r.h)
                    new_rec = Rectangle(x1, y1, x2 - x1, y2 - y1)
                    corrected_recs.append(new_rec)
        corrected_recs.append(rec)
        all_recs = corrected_recs
    return corrected_recs

def find_smallest_rec(all_rec):

    smallest=all_rec[0]
    for rec in all_rec:
        if rec.w*rec.h<smallest.w*smallest.h:
            smallest=rec
    return smallest

def discard_irrelevant_results(all_recs):
    rec_fields = []
    rec_relevant = []
    sum_fields = 0
    for rec in all_recs:
        sum_fields += rec.w*rec.h
    average_field = sum_fields/len(all_recs)
    # for rec in all_recs:
    #     if rec.w * rec.h > average_field:
    #         rec_fields.append(rec.w*rec.h)
    #         rec_relevant.append(Rectangle(rec.x,rec.y,rec.w,rec.h))
    for rec in all_recs:
        rec_fields.append(rec.w * rec.h)
    deviation=stdev(rec_fields)
    while deviation/average_field>=1 and len(all_recs)>1:
        all_recs.remove(find_smallest_rec(all_recs))
    # plt.hist(rec_fields, rwidth=5)
    # plt.title("Average field: "+str(average_field)+"\nIndications: "+str(len(rec_fields)))
    # plt.show()
    return all_recs


# def check_histograms(img, x_max, y_max, w_max, h_max, roi_x_min, roi_x_max, roi_y_min, roi_y_max):
#
#     height, width, channels = img.shape
#     indication_surface_down = img[roi_y_max:height, x_max:x_max+w_max]
#     indication_surface_up = img[80:roi_y_min, x_max:x_max+w_max] #górna część obrazu oobcięta SZTYWNO
#     surface_down = img[roi_y_max:height, roi_x_min:roi_x_max] # próbka obrazu wzięta na SZTYWNO
#     surface_up = img[80:roi_y_min, roi_x_min:roi_x_max] # górna część obrazu oobcięta SZTYWNO
#
#     # cv.imshow("INDICATION DOWN", indication_surface_down)
#     # cv.imshow("INDICATION UP", indication_surface_up)
#     # cv.imshow("DOWN", surface_down)
#     # cv.imshow("UP", surface_up)
#
#     hist_indication_surface_down = cv.calcHist([indication_surface_down], [0], None, [256], [0,256])
#     hist_indication_surface_up = cv.calcHist([indication_surface_up], [0], None, [256], [0,256])
#     hist_surface_down = cv.calcHist([surface_down], [0], None, [256], [0,256])
#     hist_surface_up = cv.calcHist([surface_up], [0], None, [256], [0,256])
#     hists = [hist_indication_surface_up, hist_indication_surface_down, hist_surface_up, hist_surface_down]
#
#     check_up = cv.compareHist(hist_surface_up, hist_indication_surface_up, cv.HISTCMP_CORREL)
#     check_down = cv.compareHist(hist_surface_down, hist_indication_surface_down, cv.HISTCMP_CORREL)
#
#     # hist=cv.calcHist([img], [0], None, [256], [0,256])
#     # plt.plot(hist_indication_surface_down)
#     # plt.show()
#
#     # titles = ['UP', 'DOWN', 'IND_UP: '+str(check_up), 'IND_DOWN'+str(check_down)]
#     # for i in range(4):
#     #     plt.subplot(2, 2, i + 1)
#     #     plt.plot(hists[i], 'gray')
#     #     plt.title(titles[i])
#     #     plt.xticks([])
#     #     plt.yticks([])
#     # plt.show()
#     # cv.imshow("INIT", img)
#     # cv.waitKey()
#
#     if check_down<check_up and check_down<0.75:
#         corrected_rect = [(x_max,y_max),(x_max+w_max,roi_y_max)]
#     elif check_up<check_down and check_up<0.75:
#         corrected_rect = [(x_max,roi_y_min),(x_max+w_max,y_max+h_max)]
#     else:
#         corrected_rect = [(x_max,y_max),(x_max+w_max,y_max+h_max)]
#
#     return corrected_rect

def check_histograms(img, rec, roi):
    k=20
    #pobieram wymiary obrazu
    height, width, channels = img.shape
    #przycinam obrazy do mierzenia histogramów
    indication_surface_down = img[roi.y+roi.h:roi.y+roi.h+k, rec.x:rec.x+rec.w]
    indication_surface_up = img[roi.y-k:roi.y, rec.x:rec.x+rec.w] #górna część obrazu oobcięta SZTYWNO
    surface_down = img[roi.y+roi.h:roi.y+roi.h+k, roi.x:width] # próbka obrazu wzięta na SZTYWNO
    surface_up = img[roi.y-k:roi.y, roi.x:width] # górna część obrazu oobcięta SZTYWNO
    #liczę histogramy
    hist_indication_surface_down = cv.calcHist([indication_surface_down], [0], None, [256], [0,256])
    hist_indication_surface_up = cv.calcHist([indication_surface_up], [0], None, [256], [0,256])
    hist_surface_down = cv.calcHist([surface_down], [0], None, [256], [0,256])
    hist_surface_up = cv.calcHist([surface_up], [0], None, [256], [0,256])
    #porównuję histogramy
    check_up = cv.compareHist(hist_surface_up, hist_indication_surface_up, cv.HISTCMP_CORREL)
    check_down = cv.compareHist(hist_surface_down, hist_indication_surface_down, cv.HISTCMP_CORREL)
    #zwracam poprawione prostokąty zależnie od histogramu
    # if check_down<check_up and check_down<0.92:
    #     corrected_rect = [(rec.x,rec.y),(rec.x+rec.w,roi.y+roi.h+k)]
    # elif check_up<check_down and check_up<0.92:
    #     corrected_rect = [(rec.x,roi.y-k),(rec.x+rec.w,rec.y+rec.h)]
    # else:
    #     corrected_rect = [(rec.x,rec.y),(rec.x+rec.w,rec.y+rec.h)]
    if check_down<check_up and check_down<0.93:
        corrected_rect = Rectangle(rec.x, rec.y, rec.w, roi.y+roi.h+k-rec.y)
        corrected_rect.is_surface_breaking=True
    elif check_up<check_down and check_up<0.93:
        corrected_rect = Rectangle(rec.x, roi.y-k, rec.w, rec.y-roi.y+rec.h+k)
        corrected_rect.is_surface_breaking=True
        # [(rec.x,roi.y-k),(rec.x+rec.w,rec.y+rec.h)]
    else:
        corrected_rect = Rectangle(rec.x,rec.y,rec.w,rec.h)
    print("Input rec: ")
    print("[("+str(rec.x)+","+str(rec.y)+"),("+str(rec.x+rec.w)+","+str(rec.y+rec.h)+")]")
    print("Check down: " + str(check_down) + "\nCheck up: " + str(check_up))
    print(corrected_rect)

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


def find_roi(filename):

    thresh1 = 100
    thresh2 = 255
    dil_kernel_size = 7
    dil_it = 3
    filter_kernel=5

    roi_img = cv.imread(filename)
    roi_imgray = cv.cvtColor(roi_img, cv.COLOR_BGR2GRAY)
    roi_imgray=cv.GaussianBlur(roi_imgray,(filter_kernel,filter_kernel),0)
    _, roi_imthresh = cv.threshold(roi_imgray, thresh1, thresh2, cv.THRESH_BINARY_INV)
    roi_kernel = np.ones((dil_kernel_size, dil_kernel_size), np.uint8)
    roi_imdil = cv.dilate(roi_imthresh, roi_kernel, iterations=dil_it)
    # roi_imdil=cv.morphologyEx(roi_imdil,cv.MORPH_CLOSE,roi_kernel)

    h, w, c = roi_img.shape
    roi_mat_img = np.transpose(roi_imdil)
    first_column = roi_mat_img[0]

    for i in range(len(first_column)):
        if first_column[i] == 255 and first_column[i + 1] == 0 and i > 10:  # jakie piękne rzeczy na sztywno jprdl
            y_min = i
            break

    for j in range(i, len(first_column) - 1):
        if first_column[j] == 0 and first_column[j + 1] == 255 and j - y_min > 50:
            y_max = j                                   # jakie piękne rzeczy na sztywno jprdl
            break

    roi = Rectangle(0,y_min,w,y_max-y_min)

    # cv.rectangle(roi_img, (0,y_min), (w,y_max), (0,255,0), 2)
    # cv.imshow("my roi", roi_img)
    # cv.imshow("morph", roi_imdil)
    # # with open("roi_s_v2.txt", "a") as f:
    #     f.write("\n" + filename + ": x0 = 0; y0 = " + str(y_min) + "; x_max = " + str(w) + "; y_max = " +
    #             str(y_max) + "; h (12mm) -> " + str(y_max - y_min))

    return roi


def convert_to_mm(roi, thickness, all_recs):
    px_to_mm=thickness/roi.h
    all_recs_in_mm=[]
    for rec in all_recs:
        rec_in_mm = Rectangle(round(rec.x*px_to_mm,1),round(rec.y*px_to_mm,1),
                              round(rec.w*px_to_mm,1),round(rec.h*px_to_mm, 1))
        all_recs_in_mm.append(rec_in_mm)

    x_max = 0;y_max = 0;w_max = 0;h_max = 0

    for rec in all_recs_in_mm:
        if rec.w * rec.h > w_max * h_max:
            x_max = rec.x
            y_max = rec.y
            w_max = rec.w
            h_max = rec.h

    with open("results_in_mm.txt", "w" ) as f:
        i=0
        for rec in all_recs_in_mm:
            f.write("Pattern "+str(i)+": x0 = "+str(rec.x)+"; y0 = "+str(rec.y)+"; w = "
                    +str(rec.w)+"; h = "+str(rec.h)+"\n")
            i += 1
        f.write("Max: x0 = "+str(x_max)+"; y0 = "+str(y_max)+"; w = "+str(w_max)+"; h = "+str(h_max)+"\n")

    return x_max, y_max, w_max, h_max, all_recs_in_mm


def confirm_indications(all_indications, acceptance_level, thickness):

    if acceptance_level==1:
        l_max=0.75*thickness
        h3=1.5
        h2=2
        h1=1
    elif acceptance_level==2:
        l_max=thickness
        h3=2
        h2=2
        h1=1
    elif acceptance_level==3:
        l_max=min(1.5*thickness, 20)
        h3=2
        h2=2
        h1=1

    for ind in all_indications:
        if ind.w > l_max and ind.h > h1: ind.is_acceptable=False
        elif ind.w <= l_max:
            if ind.is_surface_breaking and ind.h > h3: ind.is_acceptable=False
            elif ind.is_surface_breaking==False and ind.h > h2: ind.is_acceptable=False
        elif ind.h < h2 or ind.h < h3:
            if ind.w > l_max: ind.is_acceptable=False

    for ind in all_indications:
        print(ind)

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

    # roi = Rectangle(roi_x_min, roi_y_min, roi_x_max-roi_x_min, roi_y_max-roi_y_min)
    roi=find_roi(filepath)
    img = cv.imread(filepath)
    img_copy = img.copy()
    height, width, channels = img.shape
    print("Height: "+str(height)+" Width: "+str(width))
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    filter_img = cv.medianBlur(imgray,filter_size)
    # filter_img = cv.GaussianBlur(imgray,(filter_size,filter_size),0)
    # filter_img = cv.bilateralFilter(imgray,10,75,75)

    edges = cv.Canny(filter_img, canny_min,canny_max)

    # img_to_dilate = edges[roi.y:roi.y+roi.h,roi.x:roi.x+roi.w]
    kernel = np.ones((dilation_kernel_size,dilation_kernel_size), np.uint8)

    edges[roi.y:roi.y+roi.h,roi.x:roi.x+roi.w] = cv.dilate(edges[roi.y:roi.y+roi.h,roi.x:roi.x+roi.w], kernel, iterations=dilation_it)
    edges[roi.y:roi.y+roi.h,roi.x:roi.x+roi.w] = cv.morphologyEx(edges[roi.y:roi.y+roi.h,roi.x:roi.x+roi.w], cv.MORPH_CLOSE, kernel)
    dilation = cv.morphologyEx(edges, cv.MORPH_ERODE, kernel)


    contours, hierarchy = cv.findContours(dilation, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = sorted(contours, reverse=1, key=cv.contourArea)
    print(len(contours))
    number_of_recs=0
    all_recs=[]
    for i in range(len(contours)):
        x,y,w,h = cv.boundingRect(contours[i])
        rec = Rectangle(x, y, w, h)
        if is_inside_joint(rec, roi):
            cv.drawContours(img, contours, i, (0, 0, 255), 1)
            all_recs.append(rec)
            number_of_recs+=1

    filtered_recs=discard_irrelevant_results(all_recs)
    # corrected_recs=all_recs
    # print(all_recs)
    # corrected_recs=check_recs_ove_recs(all_recs)
    # corrected_recs=list(dict.fromkeys((corrected_recs)))    #usuwa duplikaty
    # print("now corrected")
    # print(corrected_recs)

    corrected_recs = filtered_recs
    # for rec in filtered_recs:
    #     corrected_recs.append(check_histograms(img, rec, roi))

    x_max = 0; y_max = 0; w_max = 0; h_max = 0  # NAJWIĘKSZY PROSTOKĄT WEWNĄTRZ
    # for rec in corrected_recs:
    #     cv.rectangle(img, rec[0], rec[1], (0, 255, 0), 2)
    #     w=rec[1][0]-rec[0][0]
    #     h=rec[1][1]-rec[0][1]
    #     if w*h > w_max*h_max:
    #         x_max=rec[0][0]
    #         y_max=rec[0][1]
    #         w_max=w
    #         h_max=h
    for rec in corrected_recs:
        cv.rectangle(img, (rec.x, rec.y), (rec.x + rec.w, rec.y + rec.h), (0, 255, 0), 2)
        if rec.w * rec.h > w_max * h_max:
            x_max = rec.x
            y_max = rec.y
            w_max = rec.w
            h_max = rec.h

    images = [imgray, filter_img, edges, dilation, img]
    filepath_inspected = filepath.replace(".png", "_inspected.png")
    cv.imwrite(filepath_inspected, img)

    x_max, y_max, w_max, h_max, all_recs_in_mm = convert_to_mm(roi, 12, corrected_recs)
    confirm_indications(all_recs_in_mm,1,12)


    with open("results_in_pixels.txt", "w" ) as f:
        i=0
        for rec in all_recs:
            f.write("Pattern "+str(i)+": x0 = "+str(rec.x)+"; y0 = "+str(rec.y)+"; w = "+str(rec.w)+"; h = "+str(rec.h)+"\n")
            i += 1
        f.write("Max: x0 = "+str(x_max)+"; y0 = "+str(y_max)+"; w = "+str(w_max)+"; h = "+str(h_max)+"\n")

    return x_max, y_max, w_max, h_max, filepath_inspected, images

# throwMe=[7,20,130,3,2,0,1079,110,190]
# x_max, y_max, w_max, h_max, filepath_inspected, images = inspect("images\\test3.png", throwMe)
# cv.imshow("result", images[4])
# cv.waitKey()
# cv.destroyAllWindows()
