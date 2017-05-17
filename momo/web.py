#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
from selenium import webdriver
from general import config as systemconfig

config = systemconfig.config


def web(id, outfolder=None):
    if not outfolder:
        outfolder = 'star'
    fld = os.path.join('data', config['args'].web, outfolder)
    if not os.path.exists(fld):
        os.makedirs(fld)

    driver = webdriver.Chrome()
    try:
        star, exact_time = get_star(driver, id)
        filename = os.path.join(fld, '{}.txt'.format(id))
        save(filename, exact_time, star)
    finally:
        driver.close()
        driver.quit()


def web2(infile, loop=1, outfolder=None):
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
    if int(star) <= 0 and t >= time_out:
        print('time_out')
    else:
        print('time waited:', t)
    print(exact_time, star)
    return int(star), exact_time


def save(filename, exact_time, star):
    print('save into file:', filename)
    with open(filename, 'a') as f:
        f.write('{}\t{}\n'.format(exact_time, star))
