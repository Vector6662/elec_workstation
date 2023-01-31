from techniques.interface import AbstractTechnique
import string

from uitls import defaultAdditionalParamsHelper, parseCurveHelper, parseBasicParamsHelper, parseAdditionalParamsHelper


class ACV(AbstractTechnique):  # A.C. Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        labels = list(self.dataDict.keys())
        self.curX, self.curY, self.curXCarry, self.curYCarry, self.curXLabel, self.curYLabel \
            = parseCurveHelper(self.dataDict, self.carryDict, labels[0], labels[1], yLabelAlias='AC Current/A')
        self.xKey, self.xUnit, self.yKey, self.yUnit = 'E', 'V', 'i', 'A'

        self.curves.append({'x': self.curX, 'y': self.curY})

    def formatParameterTexts(self):
        basicText = "{}\nTech: {}\nFile: {}".format(self.basicParams['Date'], self.basicParams['TechniqueName'],
                                                    self.basicParams['File'])
        additionalText = ""
        for key in self.additionalParams:
            additionalText += "{} = {}\n".format(key, self.additionalParams[key])
        analysisText = "ep = {}\neh = {}\nhpw = {}".format(self.ep(), self.eh(), self.hpw())
        return basicText, additionalText, analysisText

    def ep(self):
        return '0.208V'

    def eh(self):
        return '0.256V'

    def hpw(self):
        return '0.096V'

    def ap(self):
        return '1.108e-6VA'


class BEL(AbstractTechnique):  # Bulk Electrolysis with Coulometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        self.basicParams, additionalStart = parseBasicParamsHelper(self.lines, self.file_name)
        self.additionalParams = parseAdditionalParamsHelper(self.lines, additionalStart, 6)
        return 15


class CC(AbstractTechnique):  # Chronocoulometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self):
        self.additionalParams = parseAdditionalParamsHelper(self.lines, 8, 15)
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

    def parseCurrentCurves(self):
        labels = list(self.dataDict.keys())
        self.curX, self.curY, self.curXCarry, self.curYCarry, self.curXLabel, self.curYLabel \
            = parseCurveHelper(self.dataDict, self.carryDict, labels[0], labels[1])
        self.xKey, self.xUnit, self.yKey, self.yUnit = 't', 'S', 'Q', 'C'
        end, pre = 0, self.curX[0]
        for i in range(1, len(self.curX)):
            y = self.curY[i]
            if y < pre:
                end = i
                break
            pre = y
        self.curves.append({'x': self.curX, 'y': self.curY})
        self.curves.append({'x': self.curX[0:end], 'y': self.curY[0:end]})
        self.curves.append({'x': self.curX[end:], 'y': self.curY[end:]})


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
            'Sensitivity': self.lines[16].split("=")[1]
        }
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
