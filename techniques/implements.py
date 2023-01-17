from techniques.interface import AbstractTechnique
import string


def sensitivityHelper(text: string):
    """
    辅助函数。解析格式如:1e-2, 1e+234, 1e-11 格式的灵敏度
    如果是普通浮点数形式（如0.001），则会先转换为科学计数法
    :param text: 灵敏度字符串字符串
    :return: 符号，+或-；灵敏度绝对值
    """
    if "e" not in text:
        text = "1e-{}".format(len(text.split(".")[1]))
    text = text.strip()
    symbolIndex = text.find("e") + 1
    symbol = text[symbolIndex]
    sensitivity = int(text[symbolIndex + 1:])
    return symbol, sensitivity


def parseHelper(lines, start, end):
    """
    解析一般情况下的参数，给出区间即可解析。注意end是开区间，不包含
    :return: additionalParams, sensitivity, symbol
    """
    # 解析additionalParams
    additionalParams = {}
    sensitivity, symbol = None, None
    for i in range(start, end):
        line = lines[i]
        k, v = line.split("=")[0].strip(), line.split("=")[1].strip()
        if "Sensitivity" in k:
            symbol, sensitivity = sensitivityHelper(v)
        additionalParams[k] = v
    return additionalParams, sensitivity, symbol


class ACV(AbstractTechnique):  # A.C. Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        self.additionalParams, self.sensitivity, self.symbol = parseHelper(self.lines, 8, 16)
        # self.additionalParams = {
        #     'Init E(V)': float(self.lines[8].split("=")[1]),
        #     'Final E(V)': float(self.lines[9].split("=")[1]),
        #     'Incr E(V)': float(self.lines[10].split("=")[1]),
        #     'Amplitude(V)': float(self.lines[11].split("=")[1]),
        #     'Frequency(Hz)': float(self.lines[12].split("=")[1]),
        #     'Sample Period(S)': float(self.lines[13].split("=")[1]),
        #     'Quiet Time(S)': float(self.lines[14].split("=")[1]),
        #     'Sensitivity(A/V)': self.lines[15].split("=")[1],
        # }
        # self.symbol, self.sensitivity = sensitivityHelper(self.lines[15].split("=")[1])
        self.analyseParams = {
            'Ep': self.ep(), 'Eh': self.eh(), 'Hpw': self.hpw(), 'Ap': self.ap()
        }
        return 17

    def ep(self):
        return 0

    def eh(self):
        return 0

    def hpw(self):
        return 0

    def ap(self):
        return 0


class BEL(AbstractTechnique):  # Bulk Electrolysis with Coulometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        self.additionalParams, _, _ = parseHelper(self.lines, 8, 11)
        self.symbol = '-'
        self.sensitivity = 5  # 用total Q作为灵敏度
        self.analyseParams, _, _ = parseHelper(self.lines, 12, 14)
        return 15


class CC(AbstractTechnique):  # Chronocoulometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        self.additionalParams, _, _ = parseHelper(self.lines, 8, 15)
        self.sensitivity, self.symbol = 6, '-'
        self.analyseParams = {
            'F_Slp': self.lines[17].split("=")[1],
            'F_Int': self.lines[18].split("=")[1],
            'F_Cor': self.lines[19].split("=")[1],
            'R_Slp': self.lines[22].split("=")[1],
            'R_Int': self.lines[23].split("=")[1],
            'R_Cor': self.lines[24].split("=")[1],
        }
        return 26

    def formatParameterTexts(self):
        # CC测试技术的分析参数的格式较为特殊，因此重写
        basicText = "{}\nTech: {}\nFile: {}".format(self.basicParams['date'], self.basicParams['techniqueName'],
                                                    self.basicParams['file'])
        additionalText = ""
        for key in self.additionalParams:
            additionalText += "{} = {}\n".format(key, self.additionalParams[key])
        textFormat = "Slp = {}\nInt = {}\nCor = {}\n\n"
        analysisText = "Forward:\n"
        analysisText += textFormat.format(self.analyseParams['F_Slp'], self.analyseParams['F_Int'],
                                          self.analyseParams['F_Cor'])
        analysisText += "Reverse:\n"
        analysisText += textFormat.format(self.analyseParams['R_Slp'], self.analyseParams['R_Int'],
                                          self.analyseParams['R_Cor'])
        return basicText, additionalText, analysisText


class CP(AbstractTechnique):  # Chronopotentiometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class CV(AbstractTechnique):  # Cyclic Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        # 解析实验参数
        self.additionalParams = {
            'Init E': float(self.lines[8].split("=")[1]),
            'High E': float(self.lines[9].split("=")[1]),
            'Low E': float(self.lines[10].split("=")[1]),
            'Init PN': self.lines[11],
            'Scan Rate': float(self.lines[12].split("=")[1]),
            'Segment': float(self.lines[13].split("=")[1]),  # segment数量
            'Sample Interval': float(self.lines[14].split("=")[1]),
            'Quiet Time': float(self.lines[15].split("=")[1]),
            'Sensitivity': self.lines[16].split("=")[1]  # Sensitivity数据本身
        }
        self.symbol, self.sensitivity = sensitivityHelper(self.lines[16].split("=")[1])
        return 21


class DDPA(AbstractTechnique):  # Double Differential Pulse Amperometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class DNPV(AbstractTechnique):  # Differential Normal Pulse Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class DPA(AbstractTechnique):  # Differential Pulse Amperometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class DPV(AbstractTechnique):  # Differential Pulse Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class IMP(AbstractTechnique):  # A.C. Impedance
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class IMPE(AbstractTechnique):  # Impedance - Potential
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class IMPT(AbstractTechnique):  # Impedance - Time
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class IT(AbstractTechnique):  # Amperometric i-t Curve
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class LSV(AbstractTechnique):  # Linear Sweep Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class NPV(AbstractTechnique):  # Normal Pulse Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class OCPT(AbstractTechnique):  # Open Circuit Potential - Time
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class SCV(AbstractTechnique):  # Staircase Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class SHACV(AbstractTechnique):  # 2nd Harmonic A.C. Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class SSF(AbstractTechnique):  # Sweep-Step Functions
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class SWV(AbstractTechnique):  # Square Wave Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


class TAFEL(AbstractTechnique):  # Tafel Plot
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        pass


def initTech():
    return {
        'A.C. Voltammetry': ACV,
        'Bulk Electrolysis with Coulometry': BEL,
        'Chronocoulometry': CC,
        'Chronopotentiometry': CP,
        'Cyclic Voltammetry': CV,
        'Double Differential Pulse Amperometry': DDPA,
        'Differential Normal Pulse Voltammetry': DNPV,
        'Differential Pulse Amperometry': DPA,
        'Differential Pulse Voltammetry': DPV,
        'A.C. Impedance': IMP,
        'Impedance - Potential': IMPE,
        'Impedance - Time': IMPT,
        'Amperometric i-t Curve': IT,
        'Linear Sweep Voltammetry': LSV,
        'Normal Pulse Voltammetry': NPV,
        'Open Circuit Potential - Time': OCPT,
        'Staircase Voltammetry': SCV,
        '2nd Harmonic A.C. Voltammetry': SHACV,
        'Sweep-Step Functions': SSF,
        'Square Wave Voltammetry': SWV,
        'Tafel Plot': TAFEL
    }


techniqueDict = initTech()
