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
    def select_template(cls, check_point):
        if check_point.split("-")[1] in ["缓IO时间内"]:
            script_base = "reliability.hot_plug.diff_dg.hold_io.script_bases.hold_io"
            if check_point.split("-")[3] in ["原槽位插拔DG下所有盘"]:
                plug_method = "cls.plug_in_out_method = bio_constants.PLUG_METHOD_DG_ALL"
            elif check_point.split("-")[3] in ["原盘原槽位插回"]:
                plug_method = "cls.plug_in_out_method = bio_constants.PLUG_METHOD_OLD_PD_OLD_SLOT"
            elif check_point.split("-")[3] in ["原盘原槽位反复热拔插"]:
                plug_method = "cls.plug_in_out_method = bio_constants.PLUG_METHOD_REPEAT5"
            elif check_point.split("-")[3] in ["原盘换槽位插回"]:
                plug_method = "cls.plug_in_out_method = bio_constants.PLUG_METHOD_CHANGE_SLOT"

        else:
            plug_method = ""
            if check_point.split("-")[3] in ["新盘原槽位插回"]:
                script_base = "reliability.hot_plug.diff_dg.non_hold_io.script_bases.new_pd_old_slot"
            elif check_point.split("-")[3] in ["原盘原槽位插回"]:
                script_base = "reliability.hot_plug.diff_dg.non_hold_io.script_bases.old_pd_old_slot"
            elif check_point.split("-")[3] in ["原槽位插拔DG下所有盘"]:
                script_base = "reliability.hot_plug.diff_dg.non_hold_io.script_bases.all_dg_pd_old_slot"
            elif check_point.split("-")[3] in ["原盘换槽位插回"]:
                script_base = "reliability.hot_plug.diff_dg.non_hold_io.script_bases.old_pd_change_slot"

        if check_point.split("-")[4] in ["不带io"]:
            io_flag = "cls.plug_with_io = False"
        else:
            io_flag = ""

        return script_base, plug_method, io_flag

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

        script_base, plug_method, io_flag = cls.select_template(check_point)

        context = script_template.format(case_number=case_number, case_title=case_title, test_category=test_category,
                                         check_point=check_point, case_steps=case_steps, script_base=script_base,
                                         raid_type1=raid_type, raid_type2=raid_type, pd_count1=pd_count,
                                         pd_count2=pd_count, blocks=blocks, rdpct=rdpct, seekpct=seekpct,
                                         io_flag=io_flag, plug_method=plug_method)
        cls.sum += 1

        cls.create_script_file(script_path, context)

    @classmethod
    def get_scripts_path(cls, classification_index: int, check_point_index: int, scene_index: int) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 产生一条用例的编号
        :return case_classification_title:一条用例的编号
        """


ScriptManager.create_script()
