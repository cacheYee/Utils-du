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


class ScriptManager(object):
    """
    author: DuPanPan
    date  : 2021.01.18
    description: 生产Script
    """
    case_dict_list = ExcelManager.get_case_dict_list()
    file_path = constants.INPUT_FILE.replace("\\", "/")
    sum = 0

    @classmethod
    def select_method(cls, check_point):
        offline_method = None
        if "passthrough:" in check_point:
            offline_method = "OFFLINE_MULTI_ONCE_ALL_DG"
        elif "setoffline1块盘" in check_point:
            offline_method = "OFFLINE_ONE_PD"
        elif "setoffline至VDOffline" in check_point:
            offline_method = "OFFLINE_MULTI_PD"
        return offline_method


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

        script_path = case_dict.get(constants.case_script)
        case_number = case_dict.get(constants.case_number)
        case_title = case_dict.get(constants.case_title)
        test_category = case_dict.get(constants.case_classification)
        check_point = case_dict.get(constants.case_check_point)
        case_steps = case_dict.get(constants.case_steps)

        case_scene = case_dict.get(constants.case_scene)
        pd_info = case_scene.split("2.")[-1].split("3.")[0]
        pd_count_str = pd_info.split("块")[0]
        if "x" in pd_count_str:
            pd_count = int(pd_count_str.split("x")[-1])
        else:
            pd_count = int(pd_count_str)
        pd_interface = pd_info.split("块")[-1][0:-4].upper()
        pd_medium = pd_info.split("块")[-1][-4:-1].upper()
        raid_type = case_scene.split("3.")[-1].split("个")[-1].split(":")[0].upper()

        io_pattern = case_steps.split("IO配置")[-1]
        seekpct = io_pattern.split("数据随机比例为")[-1].split("读写比例为")[0][:-1]
        rdpct = io_pattern.split("读写比例为")[-1].split("数据块大小")[0][:-1]
        blocks = io_pattern.split("数据块大小设为(")[-1].split(")测试并发")[0].replace(",", ":")

        offline_method = cls.select_method(check_point)

        context = script_template.format(case_number=case_number, case_title=case_title, test_category=test_category,
                                         check_point=check_point, case_steps=case_steps, raid_type=raid_type,
                                         pd_interface=pd_interface,pd_medium=pd_medium,
                                         pd_count=pd_count, blocks=blocks, rdpct=rdpct, seekpct=seekpct,
                                         offline_method=offline_method)
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
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_LEVEL] = case_dict.get("A1")
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_LOCATION] = case_dict.get(constants.case_script)
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_BRANCH_ID] = ""
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_MODULE_ID] = ""
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_MODULE_NAME] = ""
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_STEP] = ""
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_RUN_ID] = "0"
            framework_case_dict[constants.FRAMEWORK_EXCEL_CASE_NEED_RUN] = "Y"
            framework_case_dict_List.append(framework_case_dict)

        ExcelManager.create_framework_excel(framework_case_dict_List)




# ScriptManager.create_script()
ScriptManager.create_framework_excel_to_debug()
