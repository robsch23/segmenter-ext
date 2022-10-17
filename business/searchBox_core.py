from cv2 import cv2
import numpy as np


def found_all_boxes_with_borders(image, line_min_width=15):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # scala di grigi
    except:
        gray = image
    th1, img_bin = cv2.threshold(gray, 150, 225, cv2.THRESH_BINARY)  # binarizzazione dell'immagine
    kernal_h = np.ones((1, line_min_width), np.uint8)  # creo kernel orizzontale
    kernal_v = np.ones((line_min_width, 1), np.uint8)  # creo kernel verticale
    img_bin_h = cv2.morphologyEx(~img_bin, cv2.MORPH_OPEN,
                                 kernal_h)  # ricerco linee orizzontali ed istanzio nuova immagine
    img_bin_v = cv2.morphologyEx(~img_bin, cv2.MORPH_OPEN,
                                 kernal_v)  # ricerco linne verticali ed istanzio nuova immagine
    img_bin_final = img_bin_h | img_bin_v  # unisco le due immagini
    final_kernel = np.ones((3, 3), np.uint8)  # applico una dilatazione
    img_bin_final = cv2.dilate(img_bin_final, final_kernel, iterations=1)
    tot_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(~img_bin_final, connectivity=8,
                                                                            ltype=cv2.CV_32S)  # un'analisi dei componenti collegati
    # sull'immagine per ottenere i riquadri di
    # delimitazione delle caselle
    return stats


def searchBox_page(page,
                   range_box_height: tuple,
                   range_box_width: tuple,
                   range_box_area: tuple
                   ):
    # open as numpy array
    open_cv_image = np.array(page)

    # Convert RGB to BGR and grayscale
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)[1]

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

    cnts = found_all_boxes_with_borders(gray)

    listaBoxTrovati = []
    for (x, y, w, h, area) in cnts:
        if height_min < h < height_max and width_min < w < width_max and area_max > area > area_min:
            crop = open_cv_image[y:y + h, x:x + w]
            # cv2.imshow('window', crop)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            success, encoded_crop = cv2.imencode('.png', crop)
            if success:
                crop_bytes = encoded_crop.tobytes()
                listaBoxTrovati.append(str(crop_bytes))

    return listaBoxTrovati


if __name__ == '__main__':
    # with open('../resoucers/iban.jpeg', 'rb') as pdf:
    #     pages = convert_from_bytes(pdf.read(), dpi=200, fmt='pdf')
    img = cv2.imread('../resoucers/ANTIRICLAGGIO.pdf_page_2.jpg')

    lista = searchBox_page(img,
                           range_box_height=(0, 0),
                           range_box_width=(0, 0),
                           range_box_area=(6000, 0)
                           )

    # print(lista)
    print(len(lista))

