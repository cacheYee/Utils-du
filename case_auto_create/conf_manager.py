# -*- encoding=utf8 -*-
import os
import ast
import constants
import random
import copy
import xml.etree.ElementTree as ET

mio_list = [constants.RAND_READ_MIO_CH, constants.RAND_READ_MIO, constants.SEQUENTIAL_READ_MIO_CH,
            constants.SEQUENTIAL_READ_MIO, constants.RAND_WRITE_MIO_CH, constants.RAND_WRITE_MIO,
            constants.SEQUENTIAL_WRITE_MIO_CH, constants.SEQUENTIAL_WRITE_MIO, constants.RAND_READ_WRITE_MIO_CH,
            constants.RAND_READ_WRITE_MIO, constants.SEQUENTIAL_READ_WRITE_MIO_CH]
sio_list = [constants.RAND_READ_SIO_CH,constants.RAND_READ_SIO,constants.RAND_WRITE_SIO_CH, constants.RAND_WRITE_SIO]
lio_list = [constants.SEQUENTIAL_WRITE_LIO_CH, constants.SEQUENTIAL_WRITE_LIO]


def generate_xfersize(io_pattern_tag: str) -> str:
    """
    author:DuPanPan
    date:2020.04.28
    description: 标准化值
    :return value_format:标准化的值
    """
    io_tool_tag = random.randint(0, 9)
    xfersize = "(1K, 256K, 512K, 1M)"
    # 适用于fio数据块
    if io_tool_tag > 2:
        if io_pattern_tag in sio_list:
            a = sorted(random.sample(range(1, 16), 1))
            b = sorted(random.sample(range(17, 127), 1))
            c = sorted(random.sample(range(128, 255), 1))
            d = sorted(random.sample(range(256, 512), 1))
            a = a + b + c + d
            a = [str(x) + "K" for x in a]
            xfersize = "(" + ",".join(a) + ")"

        if io_pattern_tag in lio_list:
            a = sorted(random.sample(range(512, 1023), 1))

            b = sorted(random.sample(range(1, 4), 1))
            c = sorted(random.sample(range(5, 16), 1))
            d = sorted(random.sample(range(17, 32), 1))
            b = b + c + d
            a = [str(x) + "K" for x in a]
            b = [str(x) + "M" for x in b]
            a = a + b
            xfersize = "(" + ",".join(a) + ")"

        if io_pattern_tag in mio_list:
            a = sorted(random.sample(range(1, 255), 1))
            b = sorted(random.sample(range(256, 511), 1))
            c = sorted(random.sample(range(512, 2047, 256), 1))
            a = a + b + c
            d = sorted(random.sample(range(2, 32), 1))
            a = [str(x) + "K" for x in a]
            d = [str(x) + "M" for x in d]
            a = a + d
            xfersize = "(" + ",".join(a) + ")"

    else:
        if io_pattern_tag in sio_list:
            a = random.randint(1, 16)
            b = sorted(random.sample(range(2 * a, 127, a), 1))
            c = sorted(random.sample(list(range(2 * b[0], 255, a)), 1))
            d = sorted(random.sample(range(2 * c[0], 512, a), 1))
            a = [a]
            a = a + b + c + d
            a = [str(x) + "K" for x in a]
            xfersize = "(" + ",".join(a) + ")"

        if io_pattern_tag in lio_list:
            # a = sorted(random.sample(range(1, 1), 1))
            a = [1]
            b = sorted(random.sample(range(2, 12), 1))
            c = sorted(random.sample(range(13, 24), 1))
            d = sorted(random.sample(range(25, 32), 1))
            a = a + b + c + d
            a = [str(x) + "M" for x in a]
            xfersize = "(" + ",".join(a) + ")"

        if io_pattern_tag in mio_list:
            a = sorted(random.sample(range(1, 255), 1))
            step = a[0]
            b = sorted(random.sample(range(a[0], 511, step), 1))
            c = sorted(random.sample(range(2 * b[0], 2047, step), 1))
            d = sorted(random.sample(range(2 * c[0], 4096, step), 1))
            a = a + b + c + d
            a = [str(x) + "K" for x in a]
            xfersize = "(" + ",".join(a) + ")"

    return xfersize


def format_value(value: str) -> object:
    """
    author:DuPanPan
    date:2020.04.28
    description: 标准化值
    :return value_format:标准化的值
    """
    value = str(value)
    if value == "" or value == constants.NONE_STR:
        value_format = None
    elif value in constants.TRUE_STR_LIST:
        value_format = True
    elif value in constants.FALSE_STR_LIST:
        value_format = False
    else:
        value = value.replace(" ", "")
        try:
            value_format = ast.literal_eval(value.strip())
        except BaseException:
            value_format = value.strip()

    return value_format


class ConfigManager(object):
    """
    author: DuPanPan
    date  : 2021.01.18
    description: 管理xml配置文件
    """

    io_pattern_tag_dict = {
        constants.RAND_READ_MIO_CH: constants.RAND_READ_MIO,
        constants.SEQUENTIAL_READ_MIO_CH: constants.SEQUENTIAL_READ_MIO,
        constants.RAND_WRITE_MIO_CH: constants.RAND_WRITE_MIO,
        constants.SEQUENTIAL_WRITE_MIO_CH: constants.SEQUENTIAL_WRITE_MIO,
        constants.RAND_READ_WRITE_MIO_CH: constants.RAND_READ_WRITE_MIO,
        constants.SEQUENTIAL_READ_WRITE_MIO_CH: constants.SEQUENTIAL_READ_WRITE,
        constants.RAND_WRITE_SIO_CH: constants.RAND_WRITE_SIO,
        constants.SEQUENTIAL_WRITE_LIO_CH: constants.SEQUENTIAL_WRITE_LIO
    }
    disk_info_tag_dict = {
        constants.ALL_INTERFACE_MEDIUM_CH: constants.ALL_INTERFACE_MEDIUM,
        constants.ANY_INTERFACE_MEDIUM_CH: constants.ANY_INTERFACE_MEDIUM}

    """文件路径"""
    disk_conf_path = "test_conf/disk_conf.xml"
    io_pattern_path = "test_conf/io_pattren_conf.xml"
    raid_scene_path = "test_conf/raid_sence_conf.xml"
    case_conf_path = constants.CASE_CONF_PATH

    disk_info_dict = None
    raid_scene_dict = None
    io_pattern_list = None
    case_dict_list = None

    @classmethod
    def init(cls) -> None:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 创建Excel文件
        :return: 无返回值
        """
        cls.disk_info_dict = dict()
        cls.raid_scene_dict = dict()
        cls.io_pattern_list = dict()
        cls.case_dict_list = list()
        # ..\case_auto_create
        current_path = os.path.dirname(os.path.abspath(__file__))
        root_path = current_path
        cls.disk_conf_path = os.path.join(root_path, cls.disk_conf_path)
        cls.io_pattern_path = os.path.join(root_path, cls.io_pattern_path)
        cls.raid_scene_path = os.path.join(root_path, cls.raid_scene_path)

        cls.parse_disk_conf()
        cls.parse_raid_scene()
        cls.parse_io_pattern_conf()
        cls.parse_case_conf()

    @classmethod
    def parse_disk_conf(cls) -> None:
        """
        author: DuPanPan
        date  : 2021.01.19
        description: 解析硬盘信息文件
        :return: 无返回值
        """

        root = ET.parse(cls.disk_conf_path).getroot()
        all_interface_medium = root.find(constants.ALL_INTERFACE_MEDIUM)
        list_nodes = list(all_interface_medium)
        interface_medium_list = list()
        for node in list_nodes:
            interface_medium_list.append(format_value(node.text))
        cls.disk_info_dict[constants.ALL_INTERFACE_MEDIUM] = interface_medium_list
        any_interface_medium = root.find(constants.ANY_INTERFACE_MEDIUM)
        list_nodes = list(any_interface_medium)
        any_interface_medium_list = list()
        for node in list_nodes:
            any_interface_medium_list.append(format_value(node.text))
        cls.disk_info_dict[constants.ANY_INTERFACE_MEDIUM] = any_interface_medium_list

        print("Parse disk info xml success")

    @classmethod
    def parse_raid_scene(cls) -> None:
        """
        author: DuPanPan
        date  : 2021.01.18
        description: 解析Raid场景
        :return: 无返回值
        """
        root = ET.parse(cls.raid_scene_path).getroot()

        # JBOD
        jbod_list = list()
        jbod = root.find(constants.JBOD)
        jbod_dict = dict()
        jbod_attr_list = list(jbod)
        for jbod_attr in jbod_attr_list:
            print(type(jbod_attr))
            jbod_dict[jbod_attr.tag] = format_value(jbod_attr.text)
        jbod_list.append(jbod_dict)
        cls.raid_scene_dict[constants.JBOD] = jbod_list

        raid_level_node_list = list(root)
        for raid_level_node in raid_level_node_list:
            raid_node_list = list(raid_level_node)
            raid_list = list()
            for raid in raid_node_list:
                raid_attr_node_list = list(raid)
                raid_attr_dict = dict()
                for raid_attr in raid_attr_node_list:
                    raid_attr_dict[raid_attr.tag] = format_value(raid_attr.text)
                raid_list.append(raid_attr_dict)
            cls.raid_scene_dict[raid_level_node.tag] = raid_list
        print("Parse io pattern xml success")

    @classmethod
    def parse_io_pattern_conf(cls) -> None:
        """
        author: DuPanPan
        date  : 2021.01.19
        description: 解析IO模型
        :return: 无返回值
        """
        root = ET.parse(cls.io_pattern_path).getroot()
        io_pattern_nodes_list = list(root)
        for io_pattern_node in io_pattern_nodes_list:
            io_pattern_attr_node_list = list(io_pattern_node)
            io_pattern_attr_dict = dict()
            for io_pattern_attr in io_pattern_attr_node_list:
                io_pattern_attr_dict[io_pattern_attr.tag] = format_value(io_pattern_attr.text)
            cls.io_pattern_list[io_pattern_node.tag] = io_pattern_attr_dict
        print("Parse io pattern xml success")

    @classmethod
    def parse_case_conf(cls):
        """
        author: DuPanPan
        date  : 2021.01.19
        description: 解析IO模型
        :return: 无返回值
        """
        root = ET.parse(cls.case_conf_path).getroot()
        case_classification_node_list = root.findall(constants.CASE_CLASSIFICATION)
        for case_classification_node in case_classification_node_list:
            case_dict = format_value(case_classification_node.attrib)
            check_point_node_list = case_classification_node.findall(constants.CASE_CHECK_POINT)
            check_point_list = list()
            for check_point_node in check_point_node_list:
                check_point_dict = format_value(check_point_node.attrib)

                case_scene_node = check_point_node.find(constants.CASE_SCENE)
                case_scene_attr_list = list(case_scene_node)
                case_scene_dict = dict()
                for case_scene_attr in case_scene_attr_list:
                    case_scene_dict[case_scene_attr.tag] = format_value(case_scene_attr.text)
                    # print(case_scene_dict[case_scene_attr.tag])
                check_point_dict[constants.CASE_SCENE] = case_scene_dict

                case_pre_condition_node = check_point_node.find(constants.CASE_PRE_CONDITION)
                check_point_dict[case_pre_condition_node.tag] = format_value(case_pre_condition_node.text)

                case_steps_node = check_point_node.find(constants.CASE_STEPS)
                check_point_dict[case_steps_node.tag] = format_value(case_steps_node.text)

                case_except_node = check_point_node.find(constants.CASE_EXPECT)
                check_point_dict[case_except_node.tag] = format_value(case_except_node.text)

                check_point_list.append(check_point_dict)

            case_dict[constants.CASE_CHECK_POINT] = check_point_list

            cls.case_dict_list.append(case_dict)
        print("Parse case conf xml success")

    @classmethod
    def get_scene_list(cls, scene_tag_list) -> list:
        """
        author: DuPanPan
        date  : 2021.01.19
        description: 根据场景标签列表获取需要的场景列表
        :param scene_tag_list: 查询Raid的标签["Raid0-1","Raid5-2"]
        :return: 无返回值
        """
        scene_info_list = list()
        for scene_tag in scene_tag_list:
            raid_level = scene_tag.split(constants.RAID_SCENE_CONNECTOR)[0]
            raid_index = scene_tag.split(constants.RAID_SCENE_CONNECTOR)[-1]
            raid_scene_list = list()
            if raid_index == constants.RAID_ALL:
                raid_scene_list = cls.raid_scene_dict.get(raid_level)
            else:
                try:
                    raid_index = int(raid_index)
                except:
                    raid_index = 1
                raid_scene_list.append(cls.raid_scene_dict.get(raid_level)[raid_index - 1])
            if raid_scene_list is None or not raid_scene_list:
                print(scene_tag, ":不存在这样的Raid，检查一下字段")
            else:
                scene_info_list = scene_info_list + raid_scene_list
        return scene_info_list

    @classmethod
    def get_io_pattern_list(cls, io_pattern_tag_list) -> list:
        """
        author: DuPanPan
        date  : 2021.01.19
        description: 根据标签列表获取需要的io模型列表
        :return: 无返回值
        """
        io_pattern_info_list = list()
        for io_pattern_tag_ch in io_pattern_tag_list:
            io_pattern_tag = cls.io_pattern_tag_dict.get(io_pattern_tag_ch)
            xfersize = generate_xfersize(io_pattern_tag_ch)
            io_pattern_dict = copy.deepcopy(cls.io_pattern_list.get(io_pattern_tag))
            io_pattern_dict[constants.IO_PATTERN_IO_PRAM] = io_pattern_dict[constants.IO_PATTERN_IO_PRAM].format(
                xfersize=xfersize)
            if io_pattern_dict is None:
                print(io_pattern_tag_ch, ":不存在这样的IO模型，检查一下字段")
            io_pattern_info_list.append(io_pattern_dict)
        return io_pattern_info_list

    @classmethod
    def get_disk_info_list(cls, disk_info_tag_ch) -> list:
        """
        author: DuPanPan
        date  : 2021.01.19
        description: 根据标签列表获取需要的硬盘信息列表
        :return: 无返回值
        """
        disk_info_tag = cls.disk_info_tag_dict.get(disk_info_tag_ch)
        disk_info_list = cls.disk_info_dict.get(disk_info_tag)
        if disk_info_list is None:
            disk_info_list = format_value(disk_info_tag_ch)

        return disk_info_list


ConfigManager.init()
# print(ConfigManager.disk_info_dict)
# print(ConfigManager.raid_scene_dict)
# print(ConfigManager.io_pattern_list)
# print(len(ConfigManager.case_dict_list))
# print(ConfigManager.get_scene_list(["Raid0-all", "Raid1", "Raid5-2"]))
# print(ConfigManager.get_io_pattern_list([constants.RAND_READ_MIO_CH]))
