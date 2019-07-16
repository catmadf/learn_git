"""
                                  _oo0oo_
                                 088888880
                                 88" . "88
                                 (| -_- |)
                                  0\ = /0
                               ___/'---'\___
                             .' \\\\|     |// '.
                            / \\\\|||  :  |||// \\
                           /_ ||||| -:- |||||- \\
                          |   | \\\\\\  -  /// |   |
                          | \_|  ''\---/''  |_/ |
                          \  .-\__  '-'  __/-.  /
                        ___'. .'  /--.--\  '. .'___
                     ."" '<  '.___\_<|>_/___.' >'  "".
                    | | : '-  \'.;'\ _ /';.'/ - ' : | |
                    \  \ '_.   \_ __\ /__ _/   .-' /  /
                ====='-.____'.___ \_____/___.-'____.-'=====
                                  '=---='
 
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                        学海无涯    iii    回头是岸
@ author: 烛影鸾书
@ datetime:2019/7/10 14:45
@ software: PyCharm
@ project: SubwayDataAnalysis
@ file：tools.py

以下为简要的文档说明：
该文件下都是一些常用的工具函数，例如：
unpack2npy ：用来解包地铁格式的bin文件并读取成numpy.array格式的数据到内存
load_n_bin : 对于单文件夹下的多bin文件批量导入
mkdir_recursively : 用于递归创建文件夹
flatten : 将不规则的list展开成一维list
generate_ellipse : 生成用于绘制椭圆曲线的序列x, y
"""
doc = "用于git测试"
import re
import os
import struct
import numpy as np
from collections import Iterable


def unpack2npy(file_path, file, transf=True):
    """
    读取地铁格式的bin文件生成二维数组的数据。
    Parameter
    ---------
    file_path: str
        文件所在文件夹路径。
    file: str
        文件名。
    transf: bool, optional
        If true(default), in the returned 2-D array, each row represents a set of data for a sensor.
        If false, in the returned 2-D array, each column represents a set of data for a sensor.
    """
    param = re.findall(r'\d+', re.findall(r'\d+x\d+', file)[0])
    rows = int(param[0])
    cols = int(param[1])
    read_file = file_path + '\\' + file  # 将文件命加入到当前文件路径后面
    if os.path.isfile(read_file):
        f = open(read_file, 'rb')
        fout = f.read()
        value = struct.unpack(str(rows * cols) + 'f', fout)
        if transf:
            record = np.array(value).reshape(rows, cols).T
        else:
            record = np.array(value).reshape(rows, cols)
        return record


def load_n_bin(file_path, transf=True):
    """
        批量读取bin文件。
    Parameter
    ---------
    file_path: str
        文件所在文件夹路径。该路径底下应有多个bin文件
    transf: boll, optional
        If true(default), in the returned 2-D array, each row represents a set of data for a sensor.
        If false, in the returned 2-D array, each column represents a set of data for a sensor.
    """
    data = []
    file_list = os.listdir(file_path)
    file_list.sort(key=lambda x: int(x[2:14]))
    for item in file_list:
        if os.path.splitext(item)[-1] == '.bin':
            data.append(unpack2npy(file_path, item, transf))

    if transf:
        return np.hstack(data)
    else:
        return np.vstack(data)


def mkdir_recursively(path):
    """
    Create the path recursively, same as os.makedirs().

    Return True if success, or return False.

    e.g.
    mkdir_recursively('d:\\a\\b\\c') will create the d:\\a, d:\\a\\b, and d:\\a\\b\\c if these paths does not exist.
    """

    # First transform '\\' to '/'
    local_path = path.replace('\\', '/')

    path_list = local_path.split('/')
    print(path_list)

    if path_list is None:
        return False

    # For windows, we should add the '\\' at the end of disk name. e.g. C: -> C:\\
    disk_name = path_list[0]
    if disk_name[-1] == ':':
        path_list[0] = path_list[0] + '\\'

    dir_ = ''
    for path_item in path_list:
        dir_ = os.path.join(dir_, path_item)
        print("dir:", dir_)
        if os.path.exists(dir_):
            if os.path.isdir(dir_):
                print("mkdir skipped: %s, already exist." % (dir_,))
            else:  # Maybe a regular file, symlink, etc.
                print("Invalid directory already exist:", dir_)
                return False
        else:
            try:
                os.mkdir(dir_)
            except Exception as e:
                print("mkdir error: ", dir_)
                print(e)
                return False
            print("mkdir ok:", dir_)
    return True


def _flatten_yield(obj, ignore_itmes=(str, bytes)):
    for item in obj:
        if isinstance(item, Iterable) and not isinstance(item, ignore_itmes):
            yield from _flatten_yield(item)
        else:
            yield item


def flatten(obj):
    temp = []
    for item in _flatten_yield(obj):
        temp.append(item)
    return temp


def generate_ellipse(x0, y0, a, b, precision=0.001):
    """
    生成用于绘制椭圆曲线的序列x, y
    Parameter
    ---------
    x0: int or float
        椭圆中心的横坐标
    y0: int or float
        椭圆中心的纵坐标
    a, b: int or float
        椭圆的轴半径
    precision : float, should be limited in (0, 1)
        生成点序列的精度。
    """
    theta = np.arange(0, 1 + precision, precision) * 2 * np.pi
    x = x0 + a * np.cos(theta)
    y = y0 + b * np.sin(theta)
    return x, y


def group_consecutives(vals, step=1, f_len=99999):
    """Return list of consecutive lists of numbers from vals (number list)."""
    run = []
    result = [run]
    expect = None
    for v in vals:
        if ((v == expect) or (expect is None)) and len(run) <= f_len:
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    return result
