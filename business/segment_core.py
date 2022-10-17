from cv2 import cv2
import numpy as np
from pdf2image import convert_from_bytes


def segmentation_page(page,
                      dilation_kernel_size: tuple,
                      dilate_iteration: int,
                      range_box_height: tuple,
                      range_box_width: tuple,
                      range_box_area: tuple
                      ):
    # open as numpy array
    open_cv_image = np.array(page)

    # Convert RGB to BGR and grayscale
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

    # get max_height and max_width
    max_height_of_page = open_cv_image.shape[0]
    max_width_of_page = open_cv_image.shape[1]

    height_min, height_max = range_box_height[0], range_box_height[1]
    if not height_max or height_max <= 0:
        height_max = max_height_of_page

    width_min, width_max = range_box_width[0], range_box_width[1]
    if not width_max or width_max <= 0:
        width_max = max_width_of_page

    area_min, area_max = range_box_area[0], range_box_area[1]
    if area_max <= 0 or not area_max:
        area_max = max_width_of_page * max_height_of_page

    # clean the image using otsu method with the inversed binarized image
    blur = cv2.GaussianBlur(gray, (5, 5), sigmaX=5, sigmaY=5)  # remove anomal pixel
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]  # Otsu threshold
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, dilation_kernel_size)
    dilate = cv2.dilate(thresh, kernel, iterations=dilate_iteration)

    cnts = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    lista_box_segmentati = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        area_box = w * h
        if height_min < h < height_max and width_min < w < width_max and area_max > area_box > area_min:
            crop = open_cv_image[y:y + h, x:x + w]
            # cv2.imshow('window', crop)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            success, encoded_crop = cv2.imencode('.png', crop)
            if success:
                crop_bytes = encoded_crop.tobytes()
                lista_box_segmentati.append(str(crop_bytes))

    return lista_box_segmentati


if __name__ == '__main__':
    with open('../resoucers/AllegatoSIAMM-0000000000-0.pdf', 'rb') as pdf:
        pages = convert_from_bytes(pdf.read(), dpi=200, fmt='pdf')

    lista = segmentation_page(pages[6],
                              dilation_kernel_size=(7, 5),
                              dilate_iteration=5,
                              range_box_height=(100, 0),
                              range_box_width=(100, 0),
                              range_box_area=(0, 0)
                              )

    # print(lista)
    print(len(lista))
