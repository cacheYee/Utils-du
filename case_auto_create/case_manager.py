#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
author:      panpan.du
date:        2021.01.18
description: 测试用例管理
"""
import random
import conf_manager
from case_auto_create import constants
from excel_manager import ExcelManager
from conf_manager import ConfigManager


class CaseManager(object):
    """
    author: DuPanPan
    date  : 2021.01.18
    description: 生产Case
    """

    case_column_list = [constants.case_number, constants.case_script, constants.case_title,
                        constants.case_product, constants.case_module, constants.case_object,
                        constants.case_type, constants.case_classification, constants.case_check_point,
                        constants.case_card, constants.case_physical_env, constants.case_pre_condition,
                        constants.case_scene, constants.case_steps, constants.case_expect,
                        constants.case_priority, constants.case_is_smoke, constants.case_is_mini,
                        constants.case_is_auto, constants.case_time, constants.case_author, constants.case_notes,
                        constants.case_is_debug, constants.case_result, constants.case_is_upload]

    case_dict_list = list()

    @classmethod
    def create_case_number(cls, classification_index: int, check_point_index: int, scene_index: int) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 产生一条用例的编号
        :return case_classification_title:一条用例的编号
        """
        case_number = constants.CASE_NUMBER_PREFIX + \
                      constants.CASE_NUMBER_CONNECTOR + f"{constants.CASE_MODULE_INDEX:>02d}" + \
                      constants.CASE_NUMBER_CONNECTOR + f"{classification_index:>02d}" + \
                      constants.CASE_NUMBER_CONNECTOR + f"{check_point_index:>03d}" + \
                      constants.CASE_NUMBER_CONNECTOR + f"{scene_index:>03d}"
        return case_number

    @classmethod
    def create_case_script(cls, classification_dir: str, case_check_point_script, case_number: str, case_scene: str,
                           io_pattern, io_blocks_script) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 产生一条用例的编号
        :param classification_dir:分类级文件夹
        :param case_check_point_script: 检查级文件夹
        :param case_number: 用例编号
        :param case_scene: 脚本标志
        :param io_pattern: 脚本后缀
        :return case_script_path:一条用例脚本路径
        """
        case_script_path = constants.CASE_COMMON_DIR + constants.DIR_CONNECTOR + classification_dir + \
                           constants.DIR_CONNECTOR \
                           + case_check_point_script + constants.DIR_CONNECTOR + case_number[11:35] + \
                           constants.CASE_SCRIPTS_PATH_CONNECTOR \
                           + case_scene + constants.CASE_SCRIPTS_PATH_CONNECTOR + \
                           io_pattern + constants.CASE_SCRIPTS_PATH_CONNECTOR + io_blocks_script + \
                           constants.PYTHON_FILE_SUFFIX

        case_script_path = case_script_path.replace("-", "_").replace(" ", "").lower()
        return case_script_path

    @classmethod
    def create_case_title(cls, case_classification_title: str, case_check_point_title: str, case_scene_title: str,
                          io_pattern_title, io_blocks_title) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 产生一条用例的编号
        :param case_check_point_title: 检查点用例标题
        :param case_classification_title: 用例的分类标志
        :param case_scene_title: 用例的标志
        :param io_pattern_title: 用例的IO模型
        :return case_script_path:一条用例的标题
        """
        case_script_path = constants.CASE_TITLE_PREFIX + constants.CASE_TITLE_CONNECTOR + case_classification_title + \
                           constants.CASE_TITLE_CONNECTOR + case_check_point_title + constants.CASE_TITLE_CONNECTOR + \
                           case_scene_title + \
                           constants.CASE_TITLE_CONNECTOR + io_pattern_title + constants.CASE_TITLE_CONNECTOR + \
                           io_blocks_title

        return case_script_path

    @classmethod
    def create_case_product(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 产生一条用例的编号
        :return case_product:一条用例的所属产品
        """
        case_product = constants.CASE_PRODUCT
        return case_product

    @classmethod
    def create_case_module(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的模块
        :return case_product:一条用例模块
        """
        case_module = constants.CASE_MODULE
        return case_module

    @classmethod
    def create_case_object(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的测试对象
        :return case_product:一条用例的测试对象
        """
        case_object = constants.CASE_OBJECT
        return case_object

    @classmethod
    def create_case_type(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的类型
        :return case_product:一条用例类型
        """
        case_type = constants.CASE_TYPE
        return case_type

    @classmethod
    def create_case_classification(cls, case_classification: str) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的分类
        :return case_classification:一条用例的分类
        """
        case_classification = case_classification
        return case_classification

    @classmethod
    def create_case_check_point(cls, case_check_point: str) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的检查点
        :return case_check_point:一条用例检查点
        """
        case_check_point = case_check_point
        return case_check_point

    @classmethod
    def create_case_card(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的卡类别
        :return case_card:一条用例的卡类别
        """
        case_card = constants.CASE_CARD
        return case_card

    @classmethod
    def create_case_physical_env(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的物理环境
        :return case_card:一条用例的物理环境
        """
        case_physical_env = constants.CASE_PHYSICAL_ENV
        return case_physical_env

    @classmethod
    def create_case_pre_condition(cls, case_pre_condition) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的前提条件
        :return case_pre_condition:一条用例的前提条件
        """

        case_pre_condition = case_pre_condition
        return case_pre_condition

    @classmethod
    def create_case_test_scene(cls, case_scene_context, pd_count, disk_info, raid_level, io_pattern,
                               pd_per_array=None) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的测试场景
        :return case_test_scene:一条用例的测试场景
        """
        if pd_per_array is not None:
            pd_per_array = ", pdPerArray=" + str(pd_per_array)
        else:
            pd_per_array = ""

        case_test_scene = case_scene_context.format(pd_count, disk_info, raid_level, pd_per_array, io_pattern)
        case_test_scene = case_test_scene.replace(" ", "").replace("\t", "").strip()
        return case_test_scene

    @classmethod
    def create_case_test_steps(cls, case_steps: str, pd_count: int, disk_info, raid_level, io_pattern,
                               io_pattern_io_check, align, xfersize) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的测试步骤
        :return case_test_steps:一条用例的测试步骤
        """
        if io_pattern_io_check is not None:
            io_pattern_io_check = "，" + io_pattern_io_check
        else:
            io_pattern_io_check = ""

        io_pattern = (align + io_pattern).format(xfersize=xfersize)
        case_test_steps = case_steps.format(pd_count=pd_count, disk_info=disk_info,
                                            raid_level=raid_level,
                                            io_pattern=io_pattern,
                                            io_pattern_io_check=io_pattern_io_check
                                            )
        case_test_steps = case_test_steps.replace(" ", "").replace("\t", "").strip()
        return case_test_steps

    @classmethod
    def create_case_test_except(cls, case_test_except, io_pattern_io_check) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的测试预期
        :return case_test_except:一条用例的测试预期
        """
        if io_pattern_io_check is not None:
            io_pattern_io_check_expect = "，" + io_pattern_io_check + "成功"
        else:
            io_pattern_io_check_expect = ""

        case_test_except = case_test_except.format(io_pattern_io_check_expect=io_pattern_io_check_expect)
        case_test_except = case_test_except.replace(" ", "").replace("\t", "").strip()
        return case_test_except

    @classmethod
    def create_case_test_priority(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的优先级
        :return priority:一条用例的优先级
        """
        priority = constants.CASE_PRIORITY
        return priority

    @classmethod
    def create_case_is_smoke(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例是否为冒烟测试
        :return case_is_smoke:一条用例是否为冒烟测试
        """
        case_is_smoke = constants.CASE_IS_SMOKE
        return case_is_smoke

    @classmethod
    def create_case_is_mini(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例是否属于最小用例集
        :return case_is_mini:一条用例是否属于最小用例集
        """
        case_is_mini = constants.CASE_IS_MINI
        return case_is_mini

    @classmethod
    def create_case_is_auto(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例是否实现自动化
        :return case_is_mini:一条用例是否实现自动化
        """
        auto_type = constants.CASE_IS_AUTO
        return auto_type

    @classmethod
    def create_case_time(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的时间
        :return case_time:一条用例的时间
        """
        case_time = ""
        return case_time

    @classmethod
    def create_case_author(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的时间
        :return case_time:一条用例的时间
        """
        case_author = constants.CASE_AUTHOR = "dupp"
        return case_author

    @classmethod
    def create_case_note(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的备注
        :return case_time:一条用例的备注
        """
        case_note = ""
        return case_note

    @classmethod
    def create_case_debug(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例是否已调试
        :return case_time:一条用例的已调试
        """
        case_debug = constants.CASE_DEBUG
        return case_debug

    @classmethod
    def create_case_result(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的测试结果
        :return case_result:一条用例的测试结果
        """
        case_result = ""
        return case_result

    @classmethod
    def create_case_is_upload(cls) -> str:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的测试结果
        :return case_result:一条用例的测试结果
        """
        case_is_upload = constants.CASE_IS_UPLOAD
        return case_is_upload

    @classmethod
    def create_one_case(cls, case_classification_index, check_point_index, scene_index,
                        case_classification_script_dir, case_check_point_script, case_scene_script,
                        io_pattern_script, io_blocks_script,
                        case_classification_title, check_point_title, case_scene_title, io_pattern_title,
                        io_blocks_title,
                        case_classification_value, case_check_point, case_pre_condition,
                        case_scene_context, pd_per_array,
                        case_steps, pd_count, disk_info, raid_level, io_pattern_io_check, io_pattern, case_except,
                        align, xfersize) -> dict:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的测试结果
        :return case_result:一条用例的测试结果
        """

        case_dict = dict()
        case_number = cls.create_case_number(case_classification_index, check_point_index, scene_index)
        case_dict[constants.case_number] = case_number

        case_dict[constants.case_script] = cls.create_case_script(case_classification_script_dir,
                                                                  case_check_point_script,
                                                                  case_number, case_scene_script,
                                                                  io_pattern_script, io_blocks_script)

        case_dict[constants.case_title] = cls.create_case_title(case_classification_title,
                                                                check_point_title, case_scene_title,
                                                                io_pattern_title, io_blocks_title)

        case_dict[constants.case_product] = cls.create_case_product()
        case_dict[constants.case_module] = cls.create_case_module()
        case_dict[constants.case_object] = cls.create_case_object()
        case_dict[constants.case_type] = cls.create_case_type()
        case_dict[constants.case_classification] = cls.create_case_classification(case_classification_value)
        case_dict[constants.case_check_point] = cls.create_case_check_point(case_check_point)
        case_dict[constants.case_card] = cls.create_case_card()
        case_dict[constants.case_physical_env] = cls.create_case_physical_env()
        case_dict[constants.case_pre_condition] = cls.create_case_pre_condition(case_pre_condition)
        case_dict[constants.case_scene] = cls.create_case_test_scene(case_scene_context, pd_count, disk_info,
                                                                     raid_level, io_pattern_title, pd_per_array)
        case_dict[constants.case_steps] = cls.create_case_test_steps(case_steps, pd_count, disk_info,
                                                                     raid_level, io_pattern, io_pattern_io_check,
                                                                     align, xfersize)
        case_dict[constants.case_expect] = cls.create_case_test_except(case_except, io_pattern_io_check)
        case_dict[constants.case_priority] = cls.create_case_test_priority()
        case_dict[constants.case_is_smoke] = cls.create_case_is_smoke()
        case_dict[constants.case_is_mini] = cls.create_case_is_mini()
        case_dict[constants.case_is_auto] = cls.create_case_is_auto()
        case_dict[constants.case_time] = cls.create_case_time()
        case_dict[constants.case_author] = cls.create_case_author()
        case_dict[constants.case_notes] = cls.create_case_note()
        case_dict[constants.case_is_debug] = cls.create_case_debug()
        case_dict[constants.case_result] = cls.create_case_result()
        case_dict[constants.case_is_upload] = cls.create_case_is_upload()
        return case_dict

    @classmethod
    def create_case_list(cls) -> None:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:产生一条用例的测试结果
        :return case_result:一条用例的测试结果
        """
        ConfigManager.init()
        case_classification_index = 0

        for case in ConfigManager.case_dict_list:
            if case.get(constants.CASE_CLASSIFICATION_INDEX):
                case_classification_index = int(case.get(constants.CASE_CLASSIFICATION_INDEX))
            else:
                case_classification_index += 1
            case_classification_script_dir = case.get(constants.CASE_CLASSIFICATION_SCRIPT_DIR)
            case_classification_title = case.get(constants.CASE_CLASSIFICATION_TAG)
            case_classification_value = case.get(constants.CASE_CLASSIFICATION_VALUE)
            case_check_point_list = case.get(constants.CASE_CHECK_POINT)
            case_check_point_index = 0
            for case_check_point_dict in case_check_point_list:
                if case_check_point_dict.get(constants.CASE_CHECK_POINT_INDEX):
                    case_check_point_index = int(case_check_point_dict.get(constants.CASE_CHECK_POINT_INDEX))
                else:
                    case_check_point_index += 1
                case_check_point_title = case_check_point_dict.get(constants.CASE_CHECK_POINT_TITLE)
                case_check_point = case_check_point_dict.get(constants.CASE_CHECK_POINT_VALUE)
                case_check_point_script = case_check_point_dict.get(constants.CASE_CHECK_POINT_SCRIPT_DIR)
                case_pre_condition = case_check_point_dict.get(constants.CASE_PRE_CONDITION)
                case_steps = case_check_point_dict.get(constants.CASE_STEPS)
                case_except = case_check_point_dict.get(constants.CASE_EXPECT)
                case_scene_dict = case_check_point_dict.get(constants.CASE_SCENE)
                case_scene_context = case_scene_dict.get(constants.CASE_SCENE_CONTEXT)
                raid_scene_tag_list = case_scene_dict.get(constants.CASE_SCENE_RAID_PARM)
                raid_info_list = ConfigManager.get_scene_list(raid_scene_tag_list)
                case_scene_index = 0
                for raid_info_dict in raid_info_list:
                    raid_level = raid_info_dict.get(constants.CASE_SCENE_RAID_LEVEL)
                    pd_count = raid_info_dict.get(constants.CASE_SCENE_PD_COUNT)
                    pd_per_array = raid_info_dict.get(constants.CASE_SCENE_PD_PER_ARRAY)
                    io_pattern_tag_list = case_scene_dict.get(constants.IO_PATTERN)
                    io_pattern_list = ConfigManager.get_io_pattern_list(io_pattern_tag_list)
                    disk_all_info_list = ConfigManager.disk_info_dict.get(constants.ALL_INTERFACE_MEDIUM)
                    for io_pattern in io_pattern_list:
                        io_pattern_parm = io_pattern.get(constants.IO_PATTERN_IO_PRAM)
                        io_pattern_io_check = io_pattern.get(constants.IO_PATTERN_IO_CHECK)
                        disk_info_tag = case_scene_dict.get(constants.CASE_SCENE_INTERFACE_MEDIUM)
                        if disk_info_tag == constants.POLLING_INTERFACE_MEDIUM_CH:
                            case_scene_index += 1
                            disk_info_index = (case_scene_index - 1) % len(disk_all_info_list)
                            disk_info = disk_all_info_list[disk_info_index]
                            case_scene_script = raid_level + constants.CASE_SCRIPTS_PATH_CONNECTOR + \
                                                disk_info.replace(" ", "_").lower()
                            case_scene_title = raid_level + constants.CASE_TITLE_CONNECTOR + \
                                               disk_info.replace(" ", "_").upper()
                            io_pattern_script_title = io_pattern.get(constants.IO_PATTERN_CASE_SCRIPT)
                            io_pattern_title = io_pattern.get(constants.IO_PATTERN_CASE_TITLE)
                            io_blocks_list = ConfigManager.get_io_blocks_list()
                            for io_blocks in io_blocks_list:
                                io_blocks_title = io_blocks.get("case_title")
                                io_blocks_script = io_blocks.get("case_script")
                                xfersize = conf_manager.generate_xfersize(io_blocks.get("case_title"))
                                align_size = 256 * (int(pd_count) - int(pd_per_array))
                                print("***", align)
                                align = io_blocks.get("case_title", "")
                                if align == "条带对齐模式":
                                    align = io_blocks.get("case_text", "").format(alignsize=align_size)
                                elif align == "条带非对齐模式":
                                    align = io_blocks.get("case_text", "").format(alignsize=align_size - \
                                                                                            random.randint(1, 63))
                                else:
                                    align = ""
                                one_case_dict = cls.create_one_case(case_classification_index, case_check_point_index,
                                                                    case_scene_index, case_classification_script_dir,
                                                                    case_check_point_script,
                                                                    case_scene_script, io_pattern_script_title,
                                                                    io_blocks_script,
                                                                    case_classification_title, case_check_point_title,
                                                                    case_scene_title, io_pattern_title, io_blocks_title,
                                                                    case_classification_value, case_check_point,
                                                                    case_pre_condition, case_scene_context,
                                                                    pd_per_array,
                                                                    case_steps, pd_count, disk_info, raid_level,
                                                                    io_pattern_io_check, io_pattern_parm, case_except,
                                                                    align, xfersize)
                                cls.case_dict_list.append(one_case_dict)
                        else:
                            disk_info_list = ConfigManager.get_disk_info_list(disk_info_tag)
                            for disk_info in disk_info_list:
                                case_scene_script = raid_level + constants.CASE_SCRIPTS_PATH_CONNECTOR + \
                                                    disk_info.replace(" ", "_").lower()
                                case_scene_title = raid_level + constants.CASE_TITLE_CONNECTOR + \
                                                   disk_info.replace(" ", "_").upper()
                                io_pattern_script_title = io_pattern.get(constants.IO_PATTERN_CASE_SCRIPT)
                                io_pattern_title = io_pattern.get(constants.IO_PATTERN_CASE_TITLE)
                                io_blocks_list = ConfigManager.get_io_blocks_list()
                                for io_blocks in io_blocks_list:
                                    case_scene_index += 1
                                    io_blocks_title = io_blocks.get("case_title")
                                    io_blocks_script = io_blocks.get("case_script")
                                    if raid_level == "Raid10" and pd_per_array % 2 != 0:
                                        align_size = 256 * pd_count
                                    else:
                                        align_size = 256 * (int(pd_count) - int(int(pd_count) // int(pd_per_array)))

                                    xfersize = conf_manager.generate_xfersize(io_blocks.get("case_title"), align_size)

                                    align = io_blocks.get("case_title", "")
                                    if align == "条带对齐模式":
                                        align = io_blocks.get("case_text", "").format(alignsize=align_size)
                                    elif align == "条带非对齐模式":
                                        align = io_blocks.get("case_text", "").format(alignsize=
                                            align_size - random.randint(1, 63))
                                    else:
                                        align = ""
                                    one_case_dict = cls.create_one_case(case_classification_index,
                                                                        case_check_point_index,
                                                                        case_scene_index,
                                                                        case_classification_script_dir,
                                                                        case_check_point_script,
                                                                        case_scene_script, io_pattern_script_title,
                                                                        io_blocks_script,
                                                                        case_classification_title,
                                                                        case_check_point_title,
                                                                        case_scene_title, io_pattern_title,
                                                                        io_blocks_title,
                                                                        case_classification_value, case_check_point,
                                                                        case_pre_condition, case_scene_context,
                                                                        pd_per_array,
                                                                        case_steps, pd_count, disk_info, raid_level,
                                                                        io_pattern_io_check, io_pattern_parm,
                                                                        case_except,
                                                                        align, xfersize)
                                    cls.case_dict_list.append(one_case_dict)

    @classmethod
    def create_case_file(cls) -> None:
        """
        author: DuPanPan
        date  : 2021.01.18
        description:将测试用例列表写入字典中
        :return： None
        """
        cls.create_case_list()
        ExcelManager.file_create(cls.case_column_list, cls.case_dict_list)


if __name__ == '__main__':
    CaseManager.create_case_file()
