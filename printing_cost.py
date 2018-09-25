import argparse
import csv
import os

import cost_config as cfg
from PIL import Image


# from color_convert import rgb_to_cmyk, cmyk_scale


def main(image_path, output):
    image_list = os.listdir(image_path)
    color_list = color_calculation(image_path, image_list)
    price_list = price_calculation(color_list)
    with open(output, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["c", "m", "y", "b", "price_c", "price_m", "price_y", "price_b", "price_total"])
        writer.writerows(price_list)


def price_calculation(color_list):
    height = cfg.PAGE_PIXEL_HEIGHT
    width = cfg.PAGE_PIXEL_WIDTH
    coverage = cfg.COST_COVERAGE

    price_list = []
    for el in color_list:
        cyan = el[0] / ((height * width) * coverage * cmyk_scale)
        magenta = el[1] / ((height * width) * coverage * cmyk_scale)
        yellow = el[2] / ((height * width) * coverage * cmyk_scale)
        black = el[3] / ((height * width) * coverage * cmyk_scale)
        cyan_cost = cyan * cfg.COST_CYAN
        magenta_cost = magenta * cfg.COST_MAGENTA
        yellow_cost = yellow * cfg.COST_YELLOW
        black_cost = black * cfg.COST_BLACK

        total_cost = cyan_cost + magenta_cost + yellow_cost + black_cost + cfg.COST_ADDITIONAL
        price_list.append((cyan, magenta, yellow, black, cyan_cost, magenta_cost, yellow_cost, black_cost, total_cost))
    return price_list


def color_calculation(image_path, image_list):
    img_color_list = []
    for image in image_list:
        img = Image.open(os.path.join(image_path, image), "r")

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
                    cyan += p_c
                    magenta += p_m
                    yellow += p_y
                    black += p_k

        img_color_list.append((cyan, magenta, yellow, black, white))
    return img_color_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculating printing costs for given images")
    parser.add_argument("--path", type=str, required=True, help="path to dir including images")
    parser.add_argument("--output", type=str, default="pricelist.csv", help="name of outputfile, default pricelist.csv")
    args = parser.parse_args()

    main(args.path, args.output)
