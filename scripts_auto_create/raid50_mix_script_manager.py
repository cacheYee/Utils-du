#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
author:      panpan.du
date:        2021.01.18
description: 测试用例管理
"""
import os
from scripts_auto_create import constants
from scripts_auto_create.excel_manager import ExcelManager

backplane_dict = {"直连背板": "ALL", "Expander": "ALL", "PCIE·Switch": "ALL"}


class ScriptManager(object):
    """
    author: DuPanPan
    date  : 2021.01.18
    description: 生产Script
    """
    case_dict_list = ExcelManager.get_case_dict_list()
    file_path = "E:\生成用例\\Utils-du\scripts_auto_create\conf_manager\\basicio_raid50.txt"
    sum = 0

    @classmethod
    def create_script(cls) -> None:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 按照用例批量生成脚本
        """
        for case_dict in cls.case_dict_list:
            cls.create_one_script(case_dict)
        print(len(cls.case_dict_list), cls.sum)

    @classmethod
    def create_script_file(cls, script_path, context) -> None:
        current_path = os.path.dirname(os.path.abspath(__file__))

        script_dir = os.path.join(current_path, os.path.dirname(script_path))
        if not os.path.exists(script_dir):
            os.makedirs(script_dir)
        script_path = script_path.replace("\\", "/").split("/")[-1]
        script_path = os.path.join(script_dir, script_path)
        f = open(script_path, 'w', encoding='utf-8')
        f.write(context)
        f.close()

    @classmethod
    def create_one_script(cls, case_dict: dict) -> None:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 按照用例生成一个脚本
        """
        # 生成
        # 读取case_number

        with open(cls.file_path, 'r', encoding='utf-8') as f:
            script_template = f.read()

        with open("E:\生成用例\\Utils-du\scripts_auto_create\conf_manager\pd_dict.txt", 'r', encoding='utf-8') as f1:
            pd_info_dict_template = f1.read()

        direct_str = "bio_constants.VD_WRITE_POLICY: bio_constants.VD_WRITE_CACHE_DIRECT"

        script_path = case_dict.get(constants.case_script)
        case_number = case_dict.get(constants.case_number)
        case_title = case_dict.get(constants.case_title)
        test_category = case_dict.get(constants.case_classification)
        check_point = case_dict.get(constants.case_check_point)
        case_steps = case_dict.get(constants.case_steps)

        case_scene = case_dict.get(constants.case_scene)
        pd_info = case_scene.split("1.")[-1].split("2.")[0]
        vd_info = case_scene.split("2.")[-1].split("3.")[0]

        raid_type = vd_info.split(":")[0]

        if "size=" in vd_info:
            vd_size = "'" + vd_info.split("size=")[-1] + "'"
        else:
            vd_size = "'all'"

        vd_strip = vd_info.split("strip=")[-1].split("，")[0][:-1]
        if vd_strip == "1":
            vd_strip = "1024"

        if "pdperarray=" in vd_info:
            pd_perarray = "bio_constants.VD_PD_PER_ARRAY: " + vd_info.split("pdperarray=")[-1].split("，")[0] + ","
            wcache = vd_info.split("，")[2]
        else:
            pd_perarray = ""
            wcache = vd_info.split("，")[1]

        if "direct" in vd_info:
            direct = direct_str
        else:
            direct = ""

        pd_info_dict_list = ""
        for pd_info_dict in pd_info.split("+"):
            pd_connector = pd_info_dict.split("-")[0]
            backplane = backplane_dict[pd_connector]
            sector_size = "SIZE_" + pd_info_dict.split("-")[1].split("硬盘粒度为")[-1]
            pd_interface = pd_info_dict.split("-")[2]
            pd_medium = pd_info_dict.split("-")[3].split("(")[0]
            pd_count = pd_info_dict.split("(")[-1].split("块")[0]
            pd_info_dict_str = pd_info_dict_template.format(backplane=backplane, sector_size=sector_size,
                                                            pd_interface=pd_interface, pd_medium=pd_medium,
                                                            pd_count=pd_count)
            pd_info_dict_list = pd_info_dict_list + pd_info_dict_str

        passthrough = case_steps.split("设置控制卡MixSceneRaid5x.passthrough开关为")[-1].split("2")[0].upper()

        io_pattern = case_steps.split("IO配置")[-1]
        seekpct = io_pattern.split("数据随机比例为")[-1].split("读写比例为")[0][:-1]
        rdpct = io_pattern.split("读写比例为")[-1].split("，")[0]
        blocks = io_pattern.split("数据块大小设为(")[-1].split(")")[0].replace(",", ":")

        thread = io_pattern.split("线程数为")[-1].split("，")[0]
        depth = io_pattern.split("队列深度为")[-1].split("，")[0]
        if len(thread) > 4:
            thread = 32
        if len(depth) > 4:
            depth = 4
        if "设置IOPS限速交替" in io_pattern:
            rate_io = "bio_constants.IO_RATE_IOPS:'1000',"
        else:
            rate_io = ""

        if "数据量为" in io_pattern:
            io_size = "bio_constants.SIZE:" + "'" + io_pattern.split("数据量为")[-1].split("，")[0] + "'"
        else:
            io_size = ""

        if "测试时间为" in io_pattern:
            io_time = "bio_constants.RUN_TIME:'300',"
        else:
            io_time = ""

        context = script_template.format(case_number=case_number, case_title=case_title, test_category=test_category,
                                         check_point=check_point, case_steps=case_steps, raid_type=raid_type.upper(),
                                         vd_strip=vd_strip,
                                         vd_size=vd_size.strip(), wcache=wcache, pd_perarray=pd_perarray, direct=direct,
                                         pd_info_dict_list=pd_info_dict_list, rate_io=rate_io, blocks=blocks,
                                         rdpct=rdpct, seekpct=seekpct, io_size=io_size, io_time=io_time,
                                         thread=thread, depth=depth,passthrough=passthrough.strip())
        cls.sum += 1

        cls.create_script_file(script_path, context)

    @classmethod
    def create_framework_excel_to_debug(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 产生一条用例的编号
        """
        framework_case_dict_List = list()
        for case_dict in cls.case_dict_list:
            framework_case_dict = dict()
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_ID] = "1"
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_TITLE] = case_dict.get(constants.case_title)
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_VERSION] = "0"
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_TYPE] = case_dict.get(constants.case_type)
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_LEVEL] = "A1"
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_LOCATION] = case_dict.get(constants.case_script)
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_BRANCH_ID] = ""
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_MODULE_ID] = ""
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_MODULE_NAME] = ""
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_STEP] = ""
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_RUN_ID] = "0"
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_NEED_RUN] = "Y"
            framework_case_dict_List.append(framework_case_dict)

        ExcelManager.create_framework_excel(framework_case_dict_List)


ScriptManager.create_script()
ScriptManager.create_framework_excel_to_debug()
