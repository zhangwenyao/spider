#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import datetime
import logging
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
        l = 0
        while loop <= 0 or l < loop:
            if l < loop:
                l += 1
            for id in ids:
                star, exact_time = get_star(driver, id)
                if not onlyprint:
                    filename = os.path.join(fld, '{}.txt'.format(id))
                    save(filename, exact_time, star)
    finally:
        driver.close()
        driver.quit()


def get_star(driver, id, time_out=20):
    url = '{}/{}'.format(config['html']['url'], id)
    logging.info('crawl url: {}'.format(url))
    star = None
    t = 0
    try:
        driver.get(url)
        # flag = True
        while t < time_out:
            # if url != driver.current_url:
                # break
            try:
                elem = driver.find_element_by_xpath(
                    '//strong[@class="starNum star"]')
                star = elem.text
                if star and star != '0':
                    # if int(star) > 0:
                    break
            except:
                # if flag and star and star != '0':
                    # time_out += 60
                    # flag = False
                pass
            time.sleep(0.1)
            t += 0.1
            t = round(t, 1)
    except:
        pass
    exact_time = (datetime.datetime.utcnow() +
                  datetime.timedelta(hours=8)).strftime("%Y%m%d-%H%M%S")
    logging.info('{}\t{}'.format(exact_time,  star))
    try:
        if url != driver.current_url:
            logging.info('ERROR: user {} does not exist. New url: {}'.format(
                id, driver.current_url))
            while url != driver.current_url:
                time.sleep(5)
    except:
        pass
    if not star:
        star = '0'
        logging.info('data error')
        time.sleep(60)
    elif star == '0' and t >= time_out:
        logging.info('time_out: {}'.format(t))
    else:
        logging.info('time waited: {}'.format(t))

    return star, exact_time


def save(filename, exact_time, star):
    with open(filename, 'a') as f:
        f.write('{}\t{}\n'.format(exact_time, star))

    logging.info('save into file: {}'.format(filename))
