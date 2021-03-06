#!/usr/bin/python3                                                                                                                                   
# -*- coding: utf-8 -*-       
"""
Script which creates a corpus based on nercrologies. Normalization - lowercasing.
"""
import sys
import argparse
import xml.etree.ElementTree as ET
from common_text_features_functions import cut_xml

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract necrologies text from xml file of page to corpus file.")
    parser.add_argument('-fn', help="Filename where coordinates and page number of necrologue are kept. -> gazettetitle.necro")
    args = parser.parse_args()

    filename = args.fn
    gazette_title = filename.replace(".necro", "")
    necrologue = dict()

    with open(filename) as necrologues_data:
        for line in necrologues_data:
            for necrologue_data in line.split(" ")[1:]:
                data = necrologue_data.split("/")
                coordinates = data[1]
                page = data[0]
                necrologue[coordinates] = page

    for coord, page in necrologue.items():
        coordinates = coord.split(",")

        tree = str(gazette_title) + "/page_" + str(page) + ".xml_cleaned"
        root = ET.parse(tree)

        page_with_necro = str(gazette_title) + "/page_" + str(page) + ".txt"
        necro_text = cut_xml(coordinates[0], coordinates[1], coordinates[2], coordinates[3], root)
        necro_text_normalized = " ".join(necro_text).lower()

        sys.stdout.write(necro_text_normalized + "\n")
