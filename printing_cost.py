import argparse
import csv
import os
from multiprocessing import Process, Queue

import cost_config as cfg
from PIL import Image

cmyk_scale = 255  # PIL scale cmyk from 0 to 255


def main(image_path, output, num_threads):
    image_list = os.listdir(image_path)

    task_queue = Queue()
    for img in image_list:
        task_queue.put((image_path, img))
    result_queue = Queue()

    workers = []
    for i in range(num_threads):
        #        worker = Thread(target=color_calculation_in_thread, args=(i, q))
        worker = Process(target=color_calculation_in_thread, args=(i, task_queue, result_queue))
        #        worker.setDaemon(False)
        worker.start()
        workers.append(worker)

    # wait until all workers are finished
    for worker in workers:
        worker.join()
    # color_list = color_calculation(image_path, image_list)

    price_list = price_calculation(result_queue)
    with open(output, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "c", "m", "y", "b", "price_k", "price_m", "price_y", "price_k", "price_total"])
        writer.writerows(price_list)


def color_calculation_in_thread(i, task_queue, result_queue):
    while not task_queue.empty():
        image_path, img = task_queue.get()
        res = color_calculation(image_path, img)
        result_queue.put(res)


def color_calculation(image_path, image):
    img_path = os.path.join(image_path, image)
    img = Image.open(img_path, "r")

    if img.mode != "CMYK":
        img = img.convert("CMYK")

    pixels = img.load()
    width, height = img.size

    white = 0
    cyan = 0
    magenta = 0
    yellow = 0
    black = 0

    #        print(img.mode)

    for x in range(width):
        for y in range(height):
            if pixels[x, y] != (255, 255, 255):
                # r, g, b = pixels[x, y]
                # (p_c, p_m, p_y, p_k) = rgb_to_cmyk(r, g, b)
                (p_c, p_m, p_y, p_k) = pixels[x, y]
                (p_c, p_m, p_y, p_k) = recalculateK(p_c, p_m, p_y, p_k)
                cyan += p_c
                magenta += p_m
                yellow += p_y
                black += p_k

    return (img_path, cyan, magenta, yellow, black, white)


def recalculateK(c, m, y, k):
    if k != 0:
        return c, m, y, k
    # extract out k [0,255]
    min_cmy = min(c, m, y)
    c = (c - min_cmy)
    m = (m - min_cmy)
    y = (y - min_cmy)
    k = min_cmy

    return c, m, y, k


def price_calculation(color_list):
    height = cfg.PAGE_PIXEL_HEIGHT
    width = cfg.PAGE_PIXEL_WIDTH
    coverage = cfg.COST_COVERAGE

    price_list = []
    while not color_list.empty():
        el = color_list.get()
        #    for el in color_list:
        cyan = el[1] / ((height * width) * coverage * cmyk_scale)
        magenta = el[2] / ((height * width) * coverage * cmyk_scale)
        yellow = el[3] / ((height * width) * coverage * cmyk_scale)
        black = el[4] / ((height * width) * coverage * cmyk_scale)
        cyan_cost = cyan * cfg.COST_CYAN
        magenta_cost = magenta * cfg.COST_MAGENTA
        yellow_cost = yellow * cfg.COST_YELLOW
        black_cost = black * cfg.COST_BLACK

        total_cost = cyan_cost + magenta_cost + yellow_cost + black_cost + cfg.COST_ADDITIONAL
        price_list.append(
            (el[0], cyan, magenta, yellow, black, cyan_cost, magenta_cost, yellow_cost, black_cost, total_cost))
    return price_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculating printing costs for given images")
    parser.add_argument("--path", type=str, required=True, help="path to dir including images")
    parser.add_argument("--output", type=str, default="pricelist.csv", help="name of outputfile, default pricelist.csv")
    parser.add_argument("--threads", type=int, default=2, help="number of threads for parellel execution")

    args = parser.parse_args()

    main(args.path, args.output, args.threads)
