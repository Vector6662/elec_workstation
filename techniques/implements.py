from techniques.interface import AbstractTechnique

from uitls import parseCurveHelper, parseBasicParamsHelper, formatBasicParamsHelper


class ACV(AbstractTechnique):  # A.C. Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='E', x_unit='V', y_key='i', y_unit='A', y_label_alias='AC Current/A')

    def formatParameterTexts(self):
        basicText = formatBasicParamsHelper(self.basicParams)
        # 特殊解析附加参数
        additionalText = "ep = {}\neh = {}\nhpw = {}".format(self.ep(), self.eh(), self.hpw())
        return basicText, additionalText

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

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='t', x_unit='s', y_key='Q', y_unit='C')


class CC(AbstractTechnique):  # Chronocoulometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self) -> int:
        self.basicParams, start = parseBasicParamsHelper(self.lines, self.file_name)
        # 解析附加参数
        self.additionalParams = {
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
        basicText = formatBasicParamsHelper(self.basicParams)

        textFormat = "Slp = {}\nInt = {}\nCor = {}\n\n"
        additionalText = "Forward:\n"
        additionalText += textFormat.format(self.additionalParams['F_Slp'], self.additionalParams['F_Int'],
                                            self.additionalParams['F_Cor'])
        additionalText += "Reverse:\n"
        additionalText += textFormat.format(self.additionalParams['R_Slp'], self.additionalParams['R_Int'],
                                            self.additionalParams['R_Cor'])
        return basicText, additionalText

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='t', x_unit='s', y_key='Q', y_unit='C')
        end, pre = 0, self.curX[0]
        for i in range(1, len(self.curX)):
            y = self.curY[i]
            if y < pre:
                end = i
                break
            pre = y
        # 其他片段
        self.curves.append({'x': self.curX[0:end], 'y': self.curY[0:end]})
        self.curves.append({'x': self.curX[end:], 'y': self.curY[end:]})


class CA(AbstractTechnique):
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseParams(self) -> int:
        self.basicParams, start = parseBasicParamsHelper(self.lines, self.file_name)
        self.additionalParams = {
            'F_Slp': self.lines[19].split("=")[1],
            'F_Int': self.lines[20].split("=")[1],
            'F_Cor': self.lines[21].split("=")[1],
            'R_Slp': self.lines[24].split("=")[1],
            'R_Int': self.lines[25].split("=")[1],
            'R_Cor': self.lines[26].split("=")[1],
        }
        return 28

    def formatParameterTexts(self):
        return CC.formatParameterTexts(self)

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='t', x_unit='s', y_key='i', y_unit='A')
        end, val = 0, self.curY[0]
        for i in range(1, len(self.curX)):
            if val > self.curY[i]:
                end, val = i, self.curY[i]
        # 其他片段
        self.curves.append({'x': self.curX[0:end], 'y': self.curY[0:end]})
        self.curves.append({'x': self.curX[end:], 'y': self.curY[end:]})


class CP(AbstractTechnique):  # Chronopotentiometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='t', x_unit='s', y_key='E', y_unit='V')


class CV(AbstractTechnique):  # Cyclic Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='E', x_unit='V', y_key='i', y_unit='A')
        index, val = 0, self.curX[0]
        for i in range(1, len(self.curX)):
            x = self.curX[i]
            if x < val:
                index, val = i, x
        self.curves.append({'x': self.curX[0:index], 'y': self.curY[0:index]})
        self.curves.append({'x': self.curX[index:], 'y': self.curY[index:]})


class DDPA(AbstractTechnique):  # Double Differential Pulse Amperometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='t', x_unit='s', y_key='i', y_unit='A')


class DNPV(AbstractTechnique):  # Differential Normal Pulse Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='E', x_unit='V', y_key='i', y_unit='A')


class DPA(AbstractTechnique):  # Differential Pulse Amperometry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='t', x_unit='s', y_key='i', y_unit='A')


class DPV(AbstractTechnique):  # Differential Pulse Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='E', x_unit='V', y_key='i', y_unit='A')


class IMP(AbstractTechnique):  # A.C. Impedance
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(cur_x_label="Z'/ohm", cur_y_label='Z\"/ohm',
                                x_key='E', x_unit='V', y_key='i', y_unit='A')


class IMPE(AbstractTechnique):  # Impedance - Potential
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(cur_x_label="Potential/V", cur_y_label='Z/ohm', x_key='E', x_unit='V', y_key='y',
                                y_unit='e')


class IMPT(AbstractTechnique):  # Impedance - Time
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)


class IT(AbstractTechnique):  # Amperometric i-t Curve
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)


class LSV(AbstractTechnique):  # Linear Sweep Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)

    def parseCurrentCurves(self):
        self.defaultCurveParser(x_key='E', x_unit='V', y_key='i', y_unit='A')


class NPV(AbstractTechnique):  # Normal Pulse Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)


class OCPT(AbstractTechnique):  # Open Circuit Potential - Time
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)


class SCV(AbstractTechnique):  # Staircase Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)


class SHACV(AbstractTechnique):  # 2nd Harmonic A.C. Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)


class SSF(AbstractTechnique):  # Sweep-Step Functions
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)


class SWV(AbstractTechnique):  # Square Wave Voltammetry
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)


class TAFEL(AbstractTechnique):  # Tafel Plot
    def __init__(self, parent, lines, file_name, file_type):
        super().__init__(parent, lines, file_name, file_type)


def initTech():
    return {
        'A.C. Voltammetry': ACV,
        'Bulk Electrolysis with Coulometry': BEL,
        'Chronoamperometry': CA,
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
