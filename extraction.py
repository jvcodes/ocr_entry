from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
from fuzzywuzzy import fuzz
import pandas as pd
import io
import json
import cv2
import numpy as np
import requests

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

def tc_regex(data, method, reg):
    try:
        if method == 'findall':
            data = re.findall(reg, data , re.IGNORECASE)
        return data
    except Exception as e:
        print(e)
        return ''
        
def text_extract(path):
    files = [path + '/' + file for file in os.listdir(path) if '.jpg' in file]
    ocr_text ={}
    for file in files:
        data = ocr_core(file)
        ocr_text[file] = data
    return ocr_text

def reg_dict(path):
    ocr_text = text_extract(path)
    results = []
    for key,value in ocr_text.items():
        result = {}
        try:
            content = value.split('\n')
            content_noline = value.replace('\n', ' ')#.replace('  ', ' ')
            result['file'] = key
            result['year'] = ''
            result['name'] = ''
            result['birth_date'] = ''
            result['mother'] = ''
            result['father'] = ''
            ################  birth_date  ####################
            birth_date = re.findall('e\s{,3}declar.{1,15}\s{,3}que.*\).*\(.{1,3}h.{0,10}\)', content_noline)
            if not birth_date:
    #             print(key)
                birth_date = ['']
            reg = '.*(\(\d{1,2}\)).*(\(\d{1,2}\)).*(\(\d{4}\)).*'
            birth_date = tc_regex(birth_date[0], 'findall', reg)
            if birth_date:
                birth_date = str(birth_date[0]).replace('(','').replace(')','').replace('\'','').replace(',','/')
                result['birth_date'] = birth_date
            ################  birth_date END ####################    
    #         print(content_noline)
            parents_name = re.findall('send.{0,3}av.{0,5}patern.{0,4}\s*([A-Z\s]+e[A-Z\s]+)', content_noline , re.IGNORECASE)
            if parents_name:
                if 'e' in parents_name[0]:
                    parents_name = parents_name[0].split('e')
                    result['mother'] = parents_name[0]
                    result['father'] = parents_name[1]

            for key, val in enumerate(content):
    #             print(val)
                if 'Livro' in val:
                    for txt in content[key+1:]:
                        result['year'] += txt + ' '
                        if 'neste' in txt or 'municipio' in txt:
                            break
                ratio = fuzz.partial_ratio('filha dele declarante',val.strip())
    #             print(ratio)
                if re.findall('(.*filha\s+dele\s+declarante.*)', val) or ratio > 80:
    #                 print(content[key-1].strip(), 'ss', key, val,ratio)
                    if content[key-1].strip():
                        result['name'] = content[key-1]
                    else:
                        result['name'] = content[key-2]
                ratio = 0

            year_re = re.search('(.*)neste.*', result['year']).groups()
            if year_re:
                result['year'] = year_re[0]    
            # print(result)
            results.append(result)
        except Exception as e:
            print(e)

        data = pd.DataFrame(results)
        data.to_csv('extracted.csv')        