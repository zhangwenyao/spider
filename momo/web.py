#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
from selenium import webdriver
from general import config as systemconfig

config = systemconfig.config


def web(id, outfolder=None, onlyprint=False):
    if not onlyprint:
        if not outfolder:
            outfolder = 'star'
        fld = os.path.join('data', config['args'].web, outfolder)
        if not os.path.exists(fld):
            os.makedirs(fld)

    driver = webdriver.Chrome()
    try:
        star, exact_time = get_star(driver, id)
        if not onlyprint:
            filename = os.path.join(fld, '{}.txt'.format(id))
            save(filename, exact_time, star)
    finally:
        driver.close()
        driver.quit()


def web2(infile, loop=1, outfolder=None, onlyprint=False):
    if not onlyprint:
        if not outfolder:
            outfolder = 'star'
        fld = os.path.join('data', config['args'].web, outfolder)
        if not os.path.exists(fld):
            os.makedirs(fld)

    with open(infile, 'r') as f:
        lines = f.readlines()
    ids = [i.strip() for i in lines]

    driver = webdriver.Chrome()
    try:
        if not loop:
            loop = 1
        loop = int(loop)
        if loop < 1:
            loop = 1
        for _ in range(loop):
            for id in ids:
                star, exact_time = get_star(driver, id)
                if not onlyprint:
                    filename = os.path.join(fld, '{}.txt'.format(id))
                    save(filename, exact_time, star)
    finally:
        driver.close()
        driver.quit()


def get_star(driver, id, time_out=15):
    url = '{}/{}'.format(config['html']['url'], id)
    print('crawl url:', url)
    star = '0'
    t = 0
    try:
        driver.get(url)
        while t < time_out:
            # if url != driver.current_url:
                # break
            try:
                elem = driver.find_element_by_xpath(
                    '//strong[@class="starNum star"]')
                star = elem.text
                if star and star != '0':
                    break
            except:
                pass
            time.sleep(0.1)
            t += 0.1
            t = round(t, 1)
    except:
        pass
    exact_time = (datetime.datetime.utcnow() +
                  datetime.timedelta(hours=8)).strftime("%Y%m%d-%H%M%S")
    print(exact_time, star)
    if url != driver.current_url:
        print('ERROR: user', id, 'does not exist. New url:', driver.current_url)
    if star == '0' and t >= time_out:
        print('time_out')
    else:
        print('time waited:', t)
        star.replace(',', '')
        star.replace(' ', '')
        star.replace('万', '0000')
        star.replace('亿', '00000000')
    return int(star), exact_time


def save(filename, exact_time, star):
    print('save into file:', filename)
    with open(filename, 'a') as f:
        f.write('{}\t{}\n'.format(exact_time, star))
