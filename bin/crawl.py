# -*- coding: utf-8 -*-

import os
import sys
ROOT = os.getcwd()
sys.path.append(ROOT)

import re
import time
import json
import requests
from bs4 import BeautifulSoup

import config.setting as setting
import db.redisdb as redis


class Crawl():
    
    def __init__(self):
        self.redis = redis.RedisConnect()
        self.headers = setting.PROXY_HEADERS
        self.sleep = setting.SLEEP

    def crawl(self):
        self.__66ip()
        self.__89ip()
        self.__kuaidaili()
        self.__xiladaili()
        self.__xicidaili()

    def __setter(self, ips, website):
        try:
            for item in ips:
                self.redis.hash_set_original(item, website)
        except:
            pass

    def __template_for_daili_func(self):
        def parser(response):
            proxy = []
            ips = ['ip.ip.ip.ip:port', '...']
            for ip in ips:
                proxy.append({'http': f'http://{str(ip)}', 'https': f'http://{str(ip)}'})
                proxy.append({'http': f'https://{str(ip)}', 'https': f'https://{str(ip)}'})
            return proxy
        website = 'website'
        urls = ['website-proxy-page-urls']
        proxys = []
        for url in urls:
            try:
                response = requests.get(url, headers=self.headers)
                time.sleep(self.sleep)
                proxy = parser(response.text)
                proxys += proxy
            except Exception as error:
                setting.logging.error(f'[ERROR] [{website}] - CAUSE: {error}')
        self.__setter(proxys, website)
        setting.logging.info(f'[SUCCESS] [{website}]')

    def __66ip(self):
        def parser(response):
            proxy = []
            soup = BeautifulSoup(response, 'html.parser')
            ips = re.findall(r'\d+.\d+.\d+.\d+:\d+', soup.text)
            for ip in ips:
                proxy.append({'http': f'http://{str(ip)}', 'https': f'http://{str(ip)}'})
                proxy.append({'http': f'https://{str(ip)}', 'https': f'https://{str(ip)}'})
            return proxy
        website = 'http://www.66ip.cn/'
        url = 'http://www.66ip.cn/mo.php?sxb=&tqsl=9999'
        proxys = []
        try:
            response = requests.get(url, headers=self.headers)
            time.sleep(self.sleep)
            proxy = parser(response.text)
            proxys += proxy
        except Exception as error:
            setting.logging.error(f'[ERROR] [{website}] - CAUSE: {error}')
        self.__setter(proxys, website)
        setting.logging.info(f'[SUCCESS] [{website}]')

    def __89ip(self):
        def parser(response):
            proxy = []
            soup = BeautifulSoup(response, 'html.parser')
            ips = re.findall(r'\d+.\d+.\d+.\d+:\d+', str(soup.find('div', attrs={'class': 'fly-panel'})))
            for ip in ips:
                proxy.append({'http': f'http://{str(ip)}', 'https': f'http://{str(ip)}'})
                proxy.append({'http': f'https://{str(ip)}', 'https': f'https://{str(ip)}'})
            return proxy
        website = 'http://www.89ip.cn/'
        url = 'http://www.89ip.cn/tqdl.html?num=9999'
        proxys = []
        try:
            response = requests.get(url, headers=self.headers)
            time.sleep(self.sleep)
            proxy = parser(response.text)
            proxys += proxy
        except Exception as error:
            setting.logging.error(f'[ERROR] [{website}] - CAUSE: {error}')
        self.__setter(proxys, website)
        setting.logging.info(f'[SUCCESS] [{website}]')

    def __kuaidaili(self):
        def parser(response):
            proxy = []
            soup = BeautifulSoup(response, 'html.parser')
            ips = [ip.text for ip in soup.find_all('td', attrs={'data-title': 'IP'})]
            ports = [port.text for port in soup.find_all('td', attrs={'data-title': 'PORT'})]
            for i in zip(ips, ports):
                proxy.append({'http': f'http://{str(i[0])}:{str(i[1])}', 'https': f'http://{str(i[0])}:{str(i[1])}'})
                proxy.append({'http': f'https://{str(i[0])}:{str(i[1])}', 'https': f'https://{str(i[0])}:{str(i[1])}'})
            return proxy
        website = 'https://www.kuaidaili.com/'
        urls = ['https://www.kuaidaili.com/free/inha/%d/' % i for i in range(1, 101)] + \
               ['https://www.kuaidaili.com/free/inha/%d/' % i for i in range(1, 101)]
        proxys = []
        for url in urls:
            try:
                response = requests.get(url, headers=self.headers)
                time.sleep(self.sleep)
                proxy = parser(response.text)
                proxys += proxy
            except Exception as error:
                setting.logging.error(f'[ERROR] [{website}] - CAUSE: {error}')
        self.__setter(proxys, website)
        setting.logging.info(f'[SUCCESS] [{website}]')

    def __xiladaili(self):
        def parser(response):
            proxy = []
            soup = BeautifulSoup(response, 'html.parser')
            ip_ports = [ip.find_all('td')[0].text for ip in soup.find('table', attrs={'class': 'fl-table'}).find('tbody').find_all('tr')]
            for ip_port in ip_ports:
                proxy.append({'http': f'http://{str(ip_port)}', 'https': f'http://{str(ip_port)}'})
                proxy.append({'http': f'https://{str(ip_port)}', 'https': f'https://{str(ip_port)}'})
            return proxy
        website = 'http://www.xiladaili.com/'
        urls = ['http://www.xiladaili.com/putong/%d/' % i for i in range(1, 101)] + \
               ['http://www.xiladaili.com/gaoni/%d/' % i for i in range(1, 101)] + \
               ['http://www.xiladaili.com/http/%d/' % i for i in range(1, 101)] + \
               ['http://www.xiladaili.com/https/%d/' % i for i in range(1, 101)]
        proxys = []
        for url in urls:
            try:
                response = requests.get(url, headers=self.headers)
                time.sleep(self.sleep)
                proxy = parser(response.text)
                proxys += proxy
            except Exception as error:
                setting.logging.error(f'[ERROR] [{website}] - CAUSE: {error}')
        self.__setter(proxys, website)
        setting.logging.info(f'[SUCCESS] [{website}]')

    def __xicidaili(self):
        def parser(response):
            proxy = []
            soup = BeautifulSoup(response, 'html.parser')
            ip_list = soup.find('table', attrs={'id': 'ip_list'}).find_all('tr')[1:]
            ips = [ip.find_all('td')[1].text for ip in ip_list]
            ports = [port.find_all('td')[2].text for port in ip_list]
            for i in zip(ips, ports):
                proxy.append({'http': f'http://{str(i[0])}:{str(i[1])}', 'https': f'http://{str(i[0])}:{str(i[1])}'})
                proxy.append({'http': f'https://{str(i[0])}:{str(i[1])}', 'https': f'https://{str(i[0])}:{str(i[1])}'})
            return proxy
        website = 'https://www.xicidaili.com/'
        urls = ['https://www.xicidaili.com/wt/%d/' % i for i in range(1, 11)] + \
               ['https://www.xicidaili.com/wn/%d/' % i for i in range(1, 11)] + \
               ['https://www.xicidaili.com/nt/%d/' % i for i in range(1, 11)] + \
               ['https://www.xicidaili.com/nn/%d/' % i for i in range(1, 11)]
        proxys = []
        for url in urls:
            try:
                response = requests.get(url, headers=self.headers)
                time.sleep(self.sleep)
                proxy = parser(response.text)
                proxys += proxy
            except Exception as error:
                setting.logging.error(f'[ERROR] [{website}] - CAUSE: {error}')
        self.__setter(proxys, website)
        setting.logging.info(f'[SUCCESS] [{website}]')


c = Crawl()
while True:
    c.crawl()
    time.sleep(setting.TIME_CRAWL)
