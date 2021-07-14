import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from statistics import stdev
from pathlib import Path
import datetime

class Rectangle:
    def __init__(self, x1, y1, w1, h1):
        self.x = x1
        self.y = y1
        self.w = w1
        self.h = h1
        self.is_surface_breaking=True
        self.is_acceptable=True

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+"),"+str(self.w)+"x"+str(self.h)\
               + ", Surface: " + str(self.is_surface_breaking)+", Acceptance: "+str(self.is_acceptable)


def nothing(x):
    print("Nothing:"+str(x))


def is_inside_joint(inner: Rectangle, outer: Rectangle) -> bool:
    if(inner.x >= outer.x and inner.y >= outer.y and
            (inner.x+inner.w) <= (outer.x+outer.w) and (inner.y+inner.h) <= (outer.y+outer.h)):
        return True
    else:
        return False


def error_return():
    return 0, 0, 0, 0, 0, 0, 0


def find_smallest_rec(all_rec):

    smallest = all_rec[0]
    for rec in all_rec:
        if rec.w*rec.h < smallest.w*smallest.h:
            smallest = rec
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

    all_recs.remove(find_smallest_rec(all_recs))
    deviation = stdev(rec_fields)
    while deviation/average_field >= 0.85 and len(all_recs) > 1:
        # print("dev/mean: "+str(deviation/average_field)+" dev: "+str(deviation)+" mean: "+str(average_field))
        all_recs.remove(find_smallest_rec(all_recs))
        for rec in all_recs:
            sum_fields += rec.w*rec.h
            rec_fields.append(rec.w*rec.h)
        average_field = sum_fields / len(all_recs)
        deviation = stdev(rec_fields)
    # print("dev/mean: " + str(deviation / average_field) + " dev: " + str(deviation) + " mean: " + str(average_field))
    # plt.hist(rec_fields, rwidth=5)
    # plt.title("Average field: "+str(average_field)+"\nIndications: "+str(len(rec_fields)))
    # plt.show()
    return all_recs

# def check_histograms(img, rec, roi):
#     k=45
#     #pobieram wymiary obrazu
#     ref_up = cv.imread("images\\ref_up.png")
#     ref_down = cv.imread("images\\ref_down.png")
#     #przycinam obrazy do mierzenia histogramów
#     indication_surface_down = img[roi.y+roi.h:roi.y+roi.h+k, rec.x:rec.x+rec.w]
#     indication_surface_up = img[roi.y-k:roi.y, rec.x:rec.x+rec.w] #górna część obrazu oobcięta SZTYWNO
#     #liczę histogramy
#     hist_indication_surface_down = cv.calcHist([indication_surface_down], [0], None, [256], [0,256])
#     hist_indication_surface_up = cv.calcHist([indication_surface_up], [0], None, [256], [0,256])
#     hist_surface_down = cv.calcHist([ref_down], [0], None, [256], [0,256])
#     hist_surface_up = cv.calcHist([ref_up], [0], None, [256], [0,256])
#     #porównuję histogramy
#     check_up = cv.compareHist(hist_surface_up, hist_indication_surface_up, cv.HISTCMP_CORREL)
#     check_down = cv.compareHist(hist_surface_down, hist_indication_surface_down, cv.HISTCMP_CORREL)
#     #zwracam poprawione prostokąty zależnie od histogramu
#     # if check_down<check_up and check_down<0.92:
#     #     corrected_rect = [(rec.x,rec.y),(rec.x+rec.w,roi.y+roi.h+k)]
#     # elif check_up<check_down and check_up<0.92:
#     #     corrected_rect = [(rec.x,roi.y-k),(rec.x+rec.w,rec.y+rec.h)]
#     # else:
#     #     corrected_rect = [(rec.x,rec.y),(rec.x+rec.w,rec.y+rec.h)]
#     if check_down<check_up and check_down<0.15:
#         corrected_rect = Rectangle(rec.x, rec.y, rec.w, roi.y+roi.h+k-rec.y)
#         corrected_rect.is_surface_breaking=True
#     elif check_up<check_down and check_up<=0.15:
#         corrected_rect = Rectangle(rec.x, roi.y-k, rec.w, rec.y-roi.y+rec.h+k)
#         corrected_rect.is_surface_breaking=True
#         # [(rec.x,roi.y-k),(rec.x+rec.w,rec.y+rec.h)]
#     else:
#         corrected_rect = Rectangle(rec.x,rec.y,rec.w,rec.h)
#     print("Input rec: "+str(rec))
#     print("Check down: " + str(check_down) + "\nCheck up: " + str(check_up))
#     print(corrected_rect)
#
#     return corrected_rect


def check_histograms(img, rec, roi):
    k = 20  # wysokość fali powierzchniowej

    # pobieram wymiary obrazu
    height, width, channels = img.shape
    # przycinam obrazy do mierzenia histogramów
    indication_surface_down = img[roi.y+roi.h:roi.y+roi.h+k, rec.x:rec.x+rec.w]
    indication_surface_up = img[roi.y-k:roi.y, rec.x:rec.x+rec.w]
    surface_down = img[roi.y+roi.h:roi.y+roi.h+k, roi.x:width]
    surface_up = img[roi.y-k:roi.y, roi.x:width]
    # liczę histogramy
    hist_indication_surface_down = cv.calcHist([indication_surface_down], [0], None, [256], [0,256])
    hist_indication_surface_up = cv.calcHist([indication_surface_up], [0], None, [256], [0,256])
    hist_surface_down = cv.calcHist([surface_down], [0], None, [256], [0,256])
    hist_surface_up = cv.calcHist([surface_up], [0], None, [256], [0,256])
    # porównuję histogramy
    check_up = cv.compareHist(hist_surface_up, hist_indication_surface_up, cv.HISTCMP_CORREL)
    check_down = cv.compareHist(hist_surface_down, hist_indication_surface_down, cv.HISTCMP_CORREL)
    # zwracam poprawione prostokąty zależnie od histogramu
    # if check_down<check_up and check_down<0.92:
    #     corrected_rect = [(rec.x,rec.y),(rec.x+rec.w,roi.y+roi.h+k)]
    # elif check_up<check_down and check_up<0.92:
    #     corrected_rect = [(rec.x,roi.y-k),(rec.x+rec.w,rec.y+rec.h)]
    # else:
    #     corrected_rect = [(rec.x,rec.y),(rec.x+rec.w,rec.y+rec.h)]
    if check_down<check_up and check_down < 0.9:
        corrected_rect = Rectangle(rec.x, rec.y, rec.w, roi.y+roi.h+k-rec.y)
        corrected_rect.is_surface_breaking=True
    elif check_up<check_down and check_up <= 0.9:
        corrected_rect = Rectangle(rec.x, roi.y-k, rec.w, rec.y-roi.y+rec.h+k)
        corrected_rect.is_surface_breaking = True
        # [(rec.x,roi.y-k),(rec.x+rec.w,rec.y+rec.h)]
    else:
        corrected_rect = Rectangle(rec.x,rec.y,rec.w,rec.h)
    print("Input rec: "+str(rec))
    print("Check down: " + str(check_down) + "\nCheck up: " + str(check_up))
    print(corrected_rect)

    return corrected_rect


def display_process(images):
    # titles = ['ORIGINAL', 'FILTER', 'CANNY', 'DILATE', 'CONTOURS']
    # for i in range(5):
    #     plt.subplot(3, 2, i+1)
    #     plt.imshow(images[i], 'gray')
    #     plt.title(titles[i])
    #     plt.xticks([])
    #     plt.yticks([])
    # plt.show()
    plt.subplot(1, 2, 1)
    plt.imshow(images[1], 'gray')
    plt.title('FILTER')
    plt.xticks([])
    plt.yticks([])
    plt.subplot(1,2,2)
    plt.imshow(images[2], 'gray')
    plt.title('EDGES')
    plt.xticks([])
    plt.yticks([])
    plt.show()


def find_roi(filename):

    thresh1 = 100
    thresh2 = 255
    dil_kernel_size = 7
    dil_it = 3
    filter_kernel = 5

    roi_img = cv.imread(filename)
    roi_imgray = cv.cvtColor(roi_img, cv.COLOR_BGR2GRAY)
    roi_imgray=cv.GaussianBlur(roi_imgray,(filter_kernel,filter_kernel),0)
    _, roi_imthresh = cv.threshold(roi_imgray, thresh1, thresh2, cv.THRESH_BINARY_INV)
    roi_kernel = np.ones((dil_kernel_size, dil_kernel_size), np.uint8)
    roi_imdil = cv.dilate(roi_imthresh, roi_kernel, iterations=dil_it)

    h, w, c = roi_img.shape
    roi_mat_img = np.transpose(roi_imdil)
    first_column = roi_mat_img[0]

    for i in range(len(first_column)):
        if i == len(first_column)-1:
            y_min = 0
            y_max = len(first_column)-1
            break
        if first_column[i] == 255 and first_column[i + 1] == 0 and i > 10:
            y_min = i
            break

    for j in range(i, len(first_column) - 1):
        if first_column[j] == 0 and first_column[j + 1] == 255 and j - y_min > 50:
            y_max = j
            break

    roi = Rectangle(0, y_min, w, y_max-y_min)
    return roi


def convert_to_mm(roi, thickness, all_recs):
    px_to_mm = int(thickness)/(roi.h+60)
    all_recs_in_mm = []
    for rec in all_recs:
        rec_in_mm = Rectangle(round(rec.x*px_to_mm, 1), round(rec.y*px_to_mm, 1),
                              round(rec.w*px_to_mm, 1), round(rec.h*px_to_mm, 1))
        all_recs_in_mm.append(rec_in_mm)

    x_max = 0; y_max = 0; w_max = 0; h_max = 0

    for rec in all_recs_in_mm:
        if rec.w * rec.h > w_max * h_max:
            x_max = rec.x
            y_max = rec.y
            w_max = rec.w
            h_max = rec.h

    return x_max, y_max, w_max, h_max, all_recs_in_mm


def confirm_indications(all_indications, acceptance_level, thickness):
    joint_acceptance = True
    if acceptance_level == 1:
        l_max = 0.75*float(thickness)
        h3 = 1.5
        h2 = 2
        h1 = 1
    elif acceptance_level == 2:
        l_max = thickness
        h3 = 2
        h2 = 2
        h1 = 1
    elif acceptance_level == 3:
        l_max = min(1.5*thickness, 20)
        h3 = 2
        h2 = 2
        h1 = 1

    for ind in all_indications:
        if ind.w > l_max and ind.h > h1:
            ind.is_acceptable = False
            joint_acceptance = False
        elif ind.w <= l_max:
            if ind.is_surface_breaking and ind.h > h3:
                ind.is_acceptable = False
                joint_acceptance = False
            elif not ind.is_surface_breaking and ind.h > h2:
                ind.is_acceptable = False
                joint_acceptance = False
        elif ind.h < h2 or ind.h < h3:
            if ind.w > l_max:
                ind.is_acceptable = False
                joint_acceptance = False

    for ind in all_indications:
        print(ind)

    date = datetime.date.today()
    time = datetime.datetime.now().time()

    with open(str(date) + "_" + str(time).replace(':', '_')[:-8] + "_results.txt", "w") as f:
        i = 0
        for rec in all_indications:
            f.write("Pattern " + str(i) + ": x0 = " + str(rec.x) + "; y0 = " + str(rec.y) + "; w = "
                    + str(rec.w) + "; h = " + str(rec.h) + "; " + str(rec.is_acceptable) + "\n")
            i += 1

    return joint_acceptance


def inspect(filepath, list_of_parameters, acceptance_level, thickness):
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
        filter_size = 9
        canny_min = 20
        canny_max = 77
        dilation_kernel_size = 3
        dilation_it = 3
        roi_x_min = -1
        roi_x_max = -1
        roi_y_min = -1
        roi_y_max = -1

    try_file = cv.imread(filepath)
    try:
        try_file.size == 0
    except AttributeError:
        return error_return()

    if roi_x_min == -1 and roi_x_max == -1 and roi_y_min == -1 and roi_y_max == -1:
        roi = find_roi(filepath)
    else:
        roi = Rectangle(roi_x_min, roi_y_min, roi_x_max-roi_x_min, roi_y_max-roi_y_min)


    img = cv.imread(filepath)
    height, width, channels = img.shape
    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    filter_img = cv.medianBlur(imgray,filter_size)
    # filter_img = cv.GaussianBlur(imgray,(filter_size,filter_size),0)
    # filter_img = cv.bilateralFilter(imgray, 10, 10, 10)

    edges = cv.Canny(filter_img, canny_min, canny_max)
    cv.imwrite("edges.png", edges)

    try:
        img_to_dilate = edges[roi.y:roi.y+roi.h, roi.x:roi.x+roi.w]
    except IndexError:
        return error_return()

    kernel = np.ones((dilation_kernel_size, dilation_kernel_size), np.uint8)

    img_to_dilate = cv.dilate(img_to_dilate, kernel, iterations=dilation_it)
    edges[roi.y:roi.y+roi.h,roi.x:roi.x+roi.w] = cv.morphologyEx(img_to_dilate, cv.MORPH_CLOSE, kernel)
    dilation = cv.morphologyEx(edges, cv.MORPH_ERODE, kernel)

    contours, hierarchy = cv.findContours(dilation, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    number_of_recs=0
    all_recs = []
    for i in range(len(contours)):
        x, y, w, h = cv.boundingRect(contours[i])
        rec = Rectangle(x, y, w, h)
        if is_inside_joint(rec, roi):
            cv.drawContours(img, contours, i, (0, 0, 255), 1)
            all_recs.append(rec)
            number_of_recs += 1

    if len(all_recs) == 0:
        return error_return()

    cv.imwrite("contours.png",img)
    filtered_recs = discard_irrelevant_results(all_recs)
    corrected_recs = filtered_recs
    if len(corrected_recs) == 0:
        return error_return()

    # corrected_recs = []
    # for rec in filtered_recs:
    #     corrected_recs.append(check_histograms(img, rec, roi))

    x_max = 0; y_max = 0; w_max = 0; h_max = 0
    for rec in corrected_recs:
        cv.rectangle(img, (rec.x, rec.y), (rec.x + rec.w, rec.y + rec.h), (0, 255, 0), 1)
        if rec.w * rec.h > w_max * h_max:
            x_max = rec.x
            y_max = rec.y
            w_max = rec.w
            h_max = rec.h

    images = [imgray, filter_img, edges, dilation, img]
    filepath_inspected = filepath.replace(".png", "_inspected.png")
    cv.imwrite(filepath_inspected, img)

    x_max, y_max, w_max, h_max, all_recs_in_mm = convert_to_mm(roi, thickness, corrected_recs)
    acceptance = confirm_indications(all_recs_in_mm, acceptance_level, thickness)

    with open(Path(filepath).stem+"_results_in_pixels.txt", "w") as f:
        i = 0
        for rec in all_recs:

            f.write("Pattern " + str(i) + ": x0 = " + str(rec.x) + "; y0 = " + str(rec.y) + "; w = " +
                    str(rec.w) + "; h = " + str(rec.h) + "\n")
            i += 1

    return acceptance, x_max, y_max, w_max, h_max, filepath_inspected, images


#throwMe = [9, 20, 77, 3, 3, -1, -1, -1, -1]
#acc, x_max, y_max, w_max, h_max, filepath_inspected, images = inspect("images\\test1.png", throwMe, 3, 12)
#cv.imshow("result", images[0])
#cv.waitKey()
#cv.destroyAllWindows()

# pierwsza strona do podpisu, reszta mailem, prezka w grudniu mailem i przyjść przegadać
#