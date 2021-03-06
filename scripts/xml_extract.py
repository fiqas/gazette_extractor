#!/usr/bin/python3                                                                                                                                   
# -*- coding: utf-8 -*-      

"""
Prints coordinates of paragraphs, words and lines due to given .xml file
.xml file needs to be cleaned by xml_cleaner.py
Helps in checking what is word and what is the picture fragment.
"""
import sys
import xml.etree.ElementTree as ET
import string
from common_text_features_functions import get_punct_amount
from collections import OrderedDict

para_begin_end = []
output_words_lines = []
node_list = []

def get_alpha(line):
    """
    Returns amount of alphanumeric chars.

    Args:
        line (str) : string which needs to be checked
    """
    alpha = 0
    for letter in line:
        if letter.isalpha(): alpha += 1
    return alpha

def check_paragraph(para_xml):
    """
    Checks if paragraphs contains trash, returns true if not and false if yes

    Args:
        para_xml (str) : xml of paragraph
    """
            
    root = ET.fromstring(para_xml)
    text = ""
    chars = ""
    node_list = [ele.tag for ele in root.getiterator()]

    if "WORD" in node_list:
        for word in root.iter("WORD"):
            if word.text != None: text += word.text

    if "CHARACTER" in node_list:
        for word in root.iter("CHARACTER"):
            if word.text != None: text += word.text

    else:
        for word in root.iter("LINE"):
            if word.text != None: text += word.text

    if get_alpha(text) > get_punct_amount(text): return 1
    else : return 0
    
def create_output():
    """
    Prints out the final output
    """
    sys.stdout.write("PARAGRAPH\t" + str(para_begin_end[0][0]) + " " + str(para_begin_end[0][1]) + " " + str(para_begin_end[-1][2]) + " " + str(para_begin_end[-1][3]) + "\n")
    for records in output_words_lines : sys.stdout.write(records + "\n")

def create_words_lines_output(coordinates_words):
    """
    Function which helps in making data for lines and words
    """
    coordinates = []
    for key, value in coordinates_words.items():
        coordinates.append(key)
        para_begin_end.append(key)

    output_words_lines.append("LINE\t" + str(coordinates[0][0]) + " " + str(coordinates[0][1]) + " " + str(coordinates[-1][2]) + " " + str(coordinates[-1][3]))

    for key, value in coordinates_words.items():
        keys = []
        for k in key: keys.append(k)
        for word in value.split(" "):
            output_words_lines.append("WORD\t" + ' '.join(keys) + ' ' + word)

def get_words_xml(line_xml):
    """
    Get words from xml file

    Args:
        line_xml (str) : xml of "LINE"
    """
    root = ET.fromstring(line_xml)
    coordinates_word = OrderedDict()
    node_list =  [ele.tag for ele in root.getiterator()]

    if "WORD" in node_list:
        for word in root.iter("WORD"):
            if not word: 
                coordinates = list(word.attrib.values())[0].split(',')
                x1 = coordinates[0]
                y1 = coordinates[1]
                x2 = coordinates[2]
                y2 = coordinates[3]
                if (word.text != None) :
                    coordinates_word[x1,y1,x2,y2] = word.text.lstrip().rstrip()
    
    if "CHARACTER" in node_list:
        for word in root.iter("CHARACTER"):
            if not word:
                coordinates = list(word.attrib.values())[0].split(',')
                x1 = coordinates[0]
                y1 = coordinates[1]
                x2 = coordinates[2]
                y2 = coordinates[3]
                if (word.text != None) :
                    coordinates_word[x1,y1,x2,y2] = word.text.lstrip().rstrip()

    else:
        for word in root.iter("LINE"):
            if not word:
                coordinates = list(word.attrib.values())[0].split(',')
                x1 = coordinates[0]
                y1 = coordinates[1]
                x2 = coordinates[2]
                y2 = coordinates[3]
                if (word.text != None) :
                    coordinates_word[x1,y1,x2,y2] = word.text.strip()
        
    if coordinates_word : create_words_lines_output(coordinates_word)

def get_lines_xml(para_xml):
    """
    Get lines from xml

    Args:
        para_xml (str) : xml of "PARAGRAPH"
    """
    root = ET.fromstring(para_xml)
    for line in root.iter("LINE"):
        line_xml = ET.tostring(line)
        get_words_xml(line_xml)
        
def get_paragraphs_xml(root):
    """
    Get paragraphs from xml
    """
    para_xml = ""
    for line in root.iter("PARAGRAPH"):
        para_xml = ET.tostring(line)
        if check_paragraph(para_xml):
            get_lines_xml(para_xml)
            create_output()
            para_begin_end[:] = []
            output_words_lines[:] = []

if __name__ == "__main__":

    try:
        tree_xml = ""
        for line in sys.stdin: tree_xml += line
        root = ET.fromstring(tree_xml)
    except:
        exit(0)

    get_paragraphs_xml(root)


