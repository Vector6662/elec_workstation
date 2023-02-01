import random
import re


def formatBasicParamsHelper(basic_params: dict, start_index=7):
    """

    :param basic_params:
    :param start_index: 基本参数的第二部分开始位置
    :return:
    """
    basicText = "{}\nTech: {}\nFile: {}\n\n" \
        .format(basic_params['Date'], basic_params['TechniqueName'], basic_params['File'].split("/")[-1])
    keys = list(basic_params.keys())
    for i in range(start_index, len(keys)):
        key = keys[i]
        basicText += '{} = {}\n'.format(key, basic_params[key])
    return basicText


def parseBasicParamsHelper(lines: list, file_path: str):
    """
    :param lines:
    :param file_path:
    :return: basicParams解析结果，additionalParams开始位置
    """
    basicParams = {
        'Date': lines[0],
        'TechniqueName': lines[1],  # 测试技术名称
        'File': file_path,
    }
    # 解析基础参数
    start = 3
    for _ in range(2):
        for i in range(start, len(lines)):
            line = lines[i]
            if len(line) == 0:
                start = i + 1
                break
            if ":" not in line and "=" not in line:  # IMP测试会出现这种情况
                basicParams[line] = ''
                continue
            split = re.split(r'[:=]', line)
            k, v = split[0].strip(), split[1].strip()
            basicParams[k] = v
    return basicParams, start


def formatLabel(text, carry):
    """
    格式化label，会加上进位
    :param text: 输入例子：Potential/V、Total(i/A)
    :param carry:
    :return:
    """
    if carry == 0:
        return text
    str1, str2 = text.split("/")
    return "{}/1e{}{}".format(str1, carry, str2)


def parseCurveHelper(dataDict: dict, carryDict: dict, xLabel: str, yLabel: str, xLabelAlias=None, yLabelAlias=None):
    """
    辅助方法，解析数据图像的必要参数
    :param dataDict:
    :param carryDict: 每一个label下数据进位，如{-3,-1,0}
    :param xLabel: 当前图像x轴显示的数据在dataDict中的key
    :param yLabel: 同理
    :param xLabelAlias: 别名，按照chi660设备，文件中的label名称不一定是最终显示在坐标轴legend上的那个
    :param yLabelAlias: 同理
    :return:
    """
    curX, curY = dataDict[xLabel], dataDict[yLabel]
    curXCarry, curYCarry = carryDict[xLabel], carryDict[yLabel]
    curXLabel, curYLabel = formatLabel(xLabel if xLabelAlias is None else xLabelAlias, curXCarry), \
                           formatLabel(yLabel if yLabelAlias is None else yLabelAlias, curYCarry)
    return curX, curY, curXCarry, curYCarry, curXLabel, curYLabel


def randomColor():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
