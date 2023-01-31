import random


def parseAdditionalParamsHelper(lines, start, length):
    additionalParams = {}
    for i in range(start, start + length):
        line = lines[i]
        if len(line) == 0:
            continue
        k, v = line.split("=")[0].strip(), line.split("=")[1].strip()
        additionalParams[k] = v
    return additionalParams


def defaultAdditionalParamsHelper(lines, start):
    """
    解析直到空行
    :param lines:
    :param start:
    :return: 附加参数字典，labelStartIndex
    """
    # 解析additionalParams
    additionalParams = {}
    labelStartIndex = start
    for i in range(start, len(lines)):
        line = lines[i]
        if len(line) == 0:
            labelStartIndex = i
            break
        k, v = line.split("=")[0].strip(), line.split("=")[1].strip()
        additionalParams[k] = v
    # 有可能出现的情况是两行空格，需要跳过
    while len(lines[labelStartIndex]) == 0:
        labelStartIndex += 1
    return additionalParams, labelStartIndex


def parseBasicParamsHelper(lines: list, file_path: str):
    """
    数据处理生成的数据文件会在基础参数里多出Data Proc，需要判别一下
    :param lines:
    :param file_path:
    :return: basicParams解析结果，additionalParams开始位置
    """
    basicParams = {
        'Date': lines[0],
        'TechniqueName': lines[1],  # 测试技术名称
        'File': file_path,
        'DataSource': lines[3].split(":")[1].strip(),
        'InstrumentModel': lines[4].split(":")[1].strip()
    }
    key, value = lines[5].split(":")[0], lines[5].split(":")[1]
    if "Data Proc" in key:
        basicParams[key] = value.strip()
        basicParams['Header'], basicParams['Note'] = lines[6].split(":")[1], lines[7].split(":")[1]
        return basicParams, 9
    basicParams['Header'], basicParams['Note'] = lines[5].split(":")[1], lines[6].split(":")[1]
    return basicParams, 8


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
