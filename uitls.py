import random


def parseParamHelper(lines, start, end):
    """
    解析一般情况下的参数，给出区间即可解析。注意end是开区间，不包含
    :return: additionalParams
    """
    # 解析additionalParams
    additionalParams = {}
    for i in range(start, end):
        line = lines[i]
        k, v = line.split("=")[0].strip(), line.split("=")[1].strip()
        additionalParams[k] = v
    return additionalParams


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
