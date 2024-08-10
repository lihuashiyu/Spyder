# -*- coding: utf-8 -*-

"""
====================================================================================================
    ProjectName   ：  Spider
    FileName      ：  Telegram
    CreateTime    ：  2024/8/9 17:03:58
    Author        ：  Administrator
    Email         ：
    PythonCompiler：  3.9.9
    IDE           ：  PyCharm 2020.3.4
    Version       ：  1.0
    Description   ：  文件描述
====================================================================================================
"""

import os
import sys
import base64
import requests
import json
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from multiprocessing import Pool


# 常量类和配置类
class Config:
    SUCCESS_CODE = 200

    HEADERS = \
        {
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Content-Type": "application/json;charset=uf8",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }
    
    PROXY_DICT = \
        {
            "http": "http://127.0.0.1:57890",
            "https": "http://127.0.0.1:57890"
        }
    
    NOTE_PREFIX_TUPLE = ("vless://", "vmess://", "ss://", "trojan://", "tuic://")
    
    IP_REGION_API_LIST = \
        [
            "https://ipwhois.app/json/{ip}",
            "https://ipapi.co/{ip}/json/",
            "http://www.geoplugin.net/json.gp?ip={ip}",
            "https://api.ipbase.com/v1/json/{ip}"
        ]
    
    TELEGRAM_URL_LIST = \
        [
            "https://t.me/s/v2line",
            "https://t.me/s/forwardv2ray",
            "https://t.me/s/inikotesla",
            "https://t.me/s/PrivateVPNs",
            "https://t.me/s/VlessConfig",
            "https://t.me/s/V2pedia",
            "https://t.me/s/v2rayNG_Matsuri",
            "https://t.me/s/PrivateVPNs",
            "https://t.me/s/proxystore11",
            "https://t.me/s/DirectVPN",
            "https://t.me/s/VmessProtocol",
            "https://t.me/s/OutlineVpnOfficial",
            "https://t.me/s/networknim",
            "https://t.me/s/beiten",
            "https://t.me/s/MsV2ray",
            "https://t.me/s/foxrayiran",
            "https://t.me/s/DailyV2RY",
            "https://t.me/s/yaney_01",
            "https://t.me/s/FreakConfig",
            "https://t.me/s/EliV2ray",
            "https://t.me/s/ServerNett",
            "https://t.me/s/proxystore11",
            "https://t.me/s/v2rayng_fa2",
            "https://t.me/s/v2rayng_org",
            "https://t.me/s/V2rayNGvpni",
            "https://t.me/s/custom_14",
            "https://t.me/s/v2rayNG_VPNN",
            "https://t.me/s/v2ray_outlineir",
            "https://t.me/s/v2_vmess",
            "https://t.me/s/FreeVlessVpn",
            "https://t.me/s/vmess_vless_v2rayng",
            "https://t.me/s/PrivateVPNs",
            "https://t.me/s/freeland8",
            "https://t.me/s/vmessiran",
            "https://t.me/s/Outline_Vpn",
            "https://t.me/s/vmessq",
            "https://t.me/s/WeePeeN",
            "https://t.me/s/V2rayNG3",
            "https://t.me/s/ShadowsocksM",
            "https://t.me/s/shadowsocksshop",
            "https://t.me/s/v2rayan",
            "https://t.me/s/ShadowSocks_s",
            "https://t.me/s/VmessProtocol",
            "https://t.me/s/napsternetv_config",
            "https://t.me/s/Easy_Free_VPN",
            "https://t.me/s/V2Ray_FreedomIran",
            "https://t.me/s/V2RAY_VMESS_free",
            "https://t.me/s/v2ray_for_free",
            "https://t.me/s/V2rayN_Free",
            "https://t.me/s/free4allVPN",
            "https://t.me/s/vpn_ocean",
            "https://t.me/s/configV2rayForFree",
            "https://t.me/s/FreeV2rays",
            "https://t.me/s/DigiV2ray",
            "https://t.me/s/v2rayNG_VPN",
            "https://t.me/s/freev2rayssr",
            "https://t.me/s/v2rayn_server",
            "https://t.me/s/Shadowlinkserverr",
            "https://t.me/s/iranvpnet",
            "https://t.me/s/vmess_iran",
            "https://t.me/s/mahsaamoon1",
            "https://t.me/s/V2RAY_NEW",
            "https://t.me/s/v2RayChannel",
            "https://t.me/s/configV2rayNG",
            "https://t.me/s/config_v2ray",
            "https://t.me/s/vpn_proxy_custom",
            "https://t.me/s/vpnmasi",
            "https://t.me/s/v2ray_custom",
            "https://t.me/s/VPNCUSTOMIZE",
            "https://t.me/s/HTTPCustomLand",
            "https://t.me/s/vpn_proxy_custom",
            "https://t.me/s/ViPVpn_v2ray",
            "https://t.me/s/FreeNet1500",
            "https://t.me/s/v2ray_ar",
            "https://t.me/s/beta_v2ray",
            "https://t.me/s/vip_vpn_2022",
            "https://t.me/s/FOX_VPN66",
            "https://t.me/s/VorTexIRN",
            "https://t.me/s/YtTe3la",
            "https://t.me/s/V2RayOxygen",
            "https://t.me/s/Network_442",
            "https://t.me/s/VPN_443",
            "https://t.me/s/v2rayng_v",
            "https://t.me/s/ultrasurf_12",
            "https://t.me/s/iSeqaro",
            "https://t.me/s/frev2rayng",
            "https://t.me/s/frev2ray",
            "https://t.me/s/FreakConfig",
            "https://t.me/s/Awlix_ir",
            "https://t.me/s/v2rayngvpn",
            "https://t.me/s/God_CONFIG",
            "https://t.me/s/Configforvpn01",
        ]
    
    SPLIT_ONE_SEP_LIST = ["DailyV2ry"]
    
    SAVE_MODE = "w"
    FILE_ENCODING = "utf-8"
    SAVE_DIRECTORY = "data"
    POOL_SIZE = 8
    

# 从 Telegram 获取 V2Ray 节点信息
class GetNodeResourceInfo:
    # 初始化连接会话信息
    def __init__(self, headers: Dict[str, str] = Config.HEADERS, proxies: Dict[str, str] = Config.PROXY_DICT):
        self.session = requests.Session()
        self.session.headers = headers
        # self.session.proxies = proxies
    
    # 根据 url 获取节点和 ip 对应的国家
    def get_node_by_url(self, telegram_url: str) -> Dict[str, str]:
        node_info_list = self.get_v2ray_link(telegram_url=telegram_url)
        node_country_dict = {}
        
        for node_info in node_info_list:
            ip_address = self.get_ip(node_info)
            country = self.get_country_by_ip(ip=ip_address)
            
            if country:
                node_country_dict[node_info] = country
        
        return node_country_dict
    
    # 获取 v2ray 的节点信息
    def get_v2ray_link(self: str, telegram_url: str) -> List[str]:
        response = self.session.get(url=telegram_url)
        
        node_info_list = []
        if response.status_code == Config.SUCCESS_CODE:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            divs = soup.find_all('div', class_='tgme_widget_message_text')
            divs2 = soup.find_all('div', class_='tgme_widget_message_text js-message_text before_footer')
            spans = soup.find_all('span', class_='tgme_widget_message_text')
            codes = soup.find_all('code')
            span = soup.find_all('span')
            main = soup.find_all('div')
            node_list = divs + spans + codes + divs2 + span + main
            
            for tag in node_list:
                content = tag.get_text()
                if content.startswith(Config.NOTE_PREFIX_TUPLE):
                    contents = self.split_one(string=content)
                    node_info_list = node_info_list + contents
        else:
            print(f"    Failed to fetch URL (Status Code: {response.status_code})")
        
        response.close()
        return node_info_list
    
    # 获取 url 中的 ip 地址
    def get_ip(self, string: str) -> str:
        address = string.split('//')[1]
        
        if "@" in address:
            address = address.split("@")[1]
        
        if "#" in address:
            address = address.split("#")[0]
        
        if "?" in address:
            address = address.split("?")[0]
        
        if "=" in address or address.startswith("ey"):
            str_split = address.split("=")
            cache_base64 = str_split[0] + "=" * (len(str_split) - 1)
            
            try:
                string = base64.b64decode(cache_base64).decode(Config.FILE_ENCODING)
                try:
                    data_json = json.loads(string)
                    if "add" in data_json.keys():
                        address = data_json["add"]
                    else:
                        address = data_json["host"]
                except Exception as ae:
                    address = self.get_ip(string=string)
            except Exception as e:
                print(f"    Parse base64 from string {cache_base64} is failure: {e} ...... ")
                
        return address
    
    # 根据 ip 获取对应的国家
    def get_country_by_ip(self, ip: str) -> str:
        county = ""
        
        for ip_region_api in Config.IP_REGION_API_LIST:
            ip_region = ip_region_api.replace("{ip}", ip)
            
            try:
                response = self.session.get(url=ip_region)
                
                if response.status_code == Config.SUCCESS_CODE:
                    data_dict = response.json()
                    if "country" in data_dict:
                        county = data_dict["country"]
                        return county
            except Exception as e:
                print(f"    Error retrieving region from {ip_region}: {e} ......")
        return county
    
    # 切割字符串
    def split_one(self, string: str) -> List[str]:
        split_list = []
        for sep in Config.SPLIT_ONE_SEP_LIST:
            if sep in string:
                caches = string.strip(sep).split(sep)
                split_list = caches
                break
        
        if len(split_list) == 0:
            split_list = [string]
        
        return split_list
    
    # 关闭会话
    def session_close(self):
        if self.session is not None:
            self.session.close()
        print("Request Session is closed ......")
        

# 保存资源到本地
class SaveResource:
    # 初始化保存信息
    def __init__(self, mode: str = Config.SAVE_MODE, encoding: str = Config.FILE_ENCODING, save_directory: str = Config.SAVE_DIRECTORY) -> None:
        self.mode = mode
        self.encoding = encoding
        self.save_directory = save_directory
        
    # 获取文件或目录的父文件夹
    def get_parent_directory(self, path: str = None) -> str:
        absolute_path = self.get_absolute_path(path=path)
        absolute_directory = os.path.dirname(absolute_path)
        return absolute_directory
    
    # 创建文件夹
    def create_directory(self, path: str) -> None:
        absolute_directory = self.get_parent_directory(path=path)
        os.makedirs(name=absolute_directory, mode=0o644, exist_ok=True)
    
    # 将 list 写入文件
    def list_write(self, data_list: List[str], file_name: str = f"v2ray-node.txt", mode: str = None, encoding: str = None) -> None:
        if "/" not in file_name:
            file_name = f"{self.save_directory}/{file_name}"
        
        if mode is None:
            mode = self.mode
        
        if encoding is None:
            encoding = self.encoding
            
        self.create_directory(path=file_name)
        absolute_path = self.get_absolute_path(file_name)
        
        data_string = "\n".join(data_list)
        with open(absolute_path, mode=mode, encoding=encoding) as save_file:
            save_file.write(data_string)
            print(f"    File {absolute_path} is done successfully ......    ")
    
    # 将 dict 的 value 希写入文件
    def dict_write_by_key(self, data_dict: Dict[str, Any], directory: str = None) -> None:
        if directory is None:
            directory = self.save_directory
        save_directory = self.get_absolute_path(directory)
        
        for key, value_list in data_dict.items():
            self.list_write(data_list=value_list, file_name=f"{save_directory}/{key}.txt")
            
    # 将 dict 的 key 和 value 互换
    @staticmethod
    def key_value_transformer(data_dict: Dict[str, str]) -> Dict[str, List[str]]:
        transformer_dict = {}
        a = []
    
        for key, value in data_dict.items():
            if value in transformer_dict.keys():
                transformer_dict[value].append(key)
            else:
                transformer_dict[value] = [key]
        return transformer_dict
    
    # 获取文件或文件夹的绝对路径
    @staticmethod
    def get_absolute_path(path: str = None) -> str:
        if path is None:
            path = sys.path[0]
    
        absolute_path = os.path.realpath(path)
        return absolute_path


class RunProcess:
    def __init__(self, url_list: List[str] = Config.TELEGRAM_URL_LIST, pool_size: int = Config.POOL_SIZE):
        self.url_list = url_list
        self.pool_size = pool_size
        self.node_resource = GetNodeResourceInfo()
        self.save_resource = SaveResource()
        
    # 单进程运行
    def single_run(self) -> None:
        node_list = []
        for url in self.url_list:
            nodes = self.node_resource.get_v2ray_link(telegram_url=url)
            node_list = node_list + nodes
            
        self.save_data(node_list=node_list)
        
    #  多进程运行使用
    def multi_run(self) -> None:
        self.save_resource.mode = "a"
        pool = Pool(processes=self.pool_size)
        
        for url in self.url_list:
            nodes = self.node_resource.get_v2ray_link(telegram_url=url)
            pool.apply_async(func=self.save_data, args=(nodes,))
            
        pool.close()
        pool.join()
        
    # 保存数据
    def save_data(self, node_list: List[str]) -> None:
        self.save_resource.list_write(data_list=node_list)
        
        node_dict = {}
        for node in node_list:
            ip_address = self.node_resource.get_ip(string=node)
            country = self.node_resource.get_country_by_ip(ip=ip_address)
            if country:
                if country in node_dict.keys():
                    node_dict[country].append(node)
                else:
                    node_dict[country] = [node]
                    
        self.save_resource.dict_write_by_key(data_dict=node_dict)
        
    # 关闭建立的会话
    def close(self):
        self.node_resource.session_close()


if __name__ == "__main__":
    from time import time
    start = time()
    
    run = RunProcess()
    run.multi_run()
    run.close()
    
    end = time()
    print(f"time = {round(end - start, 3)}")
    