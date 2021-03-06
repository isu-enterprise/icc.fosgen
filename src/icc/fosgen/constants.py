import re
from collections import OrderedDict

COMPETENTIONS = """
способность к самоорганизации и самообразованию (ОК-7);
способностью осваивать методики использования программных средств для решения практических задач (ОПК–2);
способностью решать стандартные задачи профессиональной деятельности на основе информационной и библиографической культуры с применением информационно-коммуникационных технологий и с учетом основных требований информационной безопасности (ОПК–5).
"""

RESULTS = """
знать:
•	методы формализации с использованием логики предикатов первого порядка\ОК-7,ОПК–2;
•	методики обработки рекурсивных структур данных\ОК-7,ОПК–2;
•	методы эвристического целенаправленного перебора\ОК-7,ОПК–2;
уметь:
•	разрабатывать программы в соответствии с логической парадигмой программирования\ОК-7,ОПК-5;
•	обосновывать корректность рекурсивных программ\ОК-7,ОПК–2;
•	разрабатывать алгоритмы автоматизации принятия решения\ОК-7,ОПК-5
владеть:
•	языком программирования Пролог стандарта ISO/IEC 13211-1:1995\ОПК-5
•	методами построения переборных и рекурсивных алгоритмов\ОПК–2,ОПК-5
•	методами разработки оптимизационных программ класса эволюционных алгоритмов\ОПК–2,ОПК-5
•	методами программными средствами разработки экспертных систем\ОПК–2,ОПК-5
"""
TK = (3,   # Количество этапов текущего контроля
      # Текущий контроль Лабы, Семинары, СРС, КП
      (30, 50, 20),        # Лабы
      (None, None, None),  # Семинары
      (30, 50, 20),        # СРС
      (None, None, None)   # КП
      )

LABS = """
1	Построение логической модели предметной области и запись этой модели в виде Пролог-программы
2	Разработка программы, обрабатывающей рекурсивную структуру данных:
3	Реализация метода искусственного интеллекта (на выбор):
4	Изучение методов многомерного статистического анализа данных
5	Разработка экспертной системы
"""

TABLE9 = """1	знать методы формализации с использованием логики предикатов первого порядка	ОК-7
ОПК-2	2,3	1,2						1,2
2	знать методики обработки рекурсивных структур данных	ОК-7
ОПК-2	2-4	1,2	3					1,2	3
3	знать методы эвристического целенаправленного перебора	ОК-7
ОПК-2	2-5		3,4	5					3,4	5
4	уметь разрабатывать программы в соответствии с логической парадигмой программирования	ОК-7
ОПК-5	1-3,6	1,2						1,2
5	уметь обосновывать корректность рекурсивных программ	ОК-7
ОПК-2	2	1,2						1,2
6	уметь разрабатывать алгоритмы автоматизации принятия решения	ОК-7
ОПК-5	1-8	1	3,4	5				1	3,4	5
7	владеть языком программирования Пролог стандарта ISO/IEC 13211-1:1995	ОПК-5	2	1,2						1,2
8	владеть методами построения переборных и рекурсивных алгоритмов	ОПК-2
ОПК-5	2	1,2	3,4	5				1,2	3,4	5
9	владеть методами разработки оптимизационных программ класса эволюционных алгоритмов	ОПК-2
ОПК-5	6-8		4						4
10	владеть методами программными средствами разработки экспертных систем	ОПК-2
ОПК-5	5	1	3	5				1	3	5
"""


def new_dict(d=None):
    if d is None:
        return OrderedDict()
    else:
        return d


def extract_comps(text, d=None):
    """
    Extracts competention codes from list like above
    mentioned variable COMPETENTIONS.
    `d` - dictionary (or None) to store code->text mapping
    """
    d = new_dict(d)
    rexp = re.compile("^(.+)(\((.+)\))")
    corerexp = re.compile("(\w+).+(\d+)")
    for l in text.split("\n"):
        l = l.strip()
        if not l:
            continue
        m = rexp.match(l)
        if m is None:
            raise ValueError(l)
        descr = m.group(1).strip()
        code = m.group(3).strip()
        m2 = corerexp.match(code)
        if m2 is None:
            raise ValueError("wrong code ({})".format(code))
        a, b = m2.group(1, 2)
        code = a + "-" + b
        d[code] = descr
    return d


def extract_work_names(text, d=None):
    """Extracts names of e.g. Laboratory works.
    Format:
    <Number> <space> <Name> <end-of-line>
    """

    d = new_dict(d)
    rexp = re.compile("^\s*(\d*)\s*(.*)$")
    for l in text.split("\n"):
        l = l.strip()
        if not l:
            continue
        m = rexp.match(l)
        if m is None:
            raise ValueError(l)
        code = m.group(1).strip()
        descr = m.group(2).strip()
        d[int(code)] = descr
    return d


def extract_table9_data(table, d=None):
    """
    3	знать методы эвристического целенаправленного перебора	ОК-7
    ОПК-2	2-5		3,4	5					3,4	5
    """
    def csplit(cols, l):
        answer = (cols + [""] * l)[:l]
        cols = (cols + [""] * l)[l:]
        return answer, cols

    d = new_dict(d)
    N = -1
    ROWRE = re.compile("^(\d+)\t(.*)$")
    s = ""
    for row in table.split("\n"):
        row = row.rstrip("\n") + " "
        m1 = ROWRE.match(row)
        if m1 is None:
            # This is a row continuation
            s += row
            continue
        # Processing s
        s = s.strip()
        if not s:
            s += " " + row
            continue
        cols = s.split("\t")
        n = int(cols[0])
        if not n >= N:
            raise ValueError(
                "Sequence of the first row is not increment monotonously")
        _,    cols = csplit(cols, 4)
        labs, cols = csplit(cols, 3)
        sem,  cols = csplit(cols, 3)
        srs,  cols = csplit(cols, 3)
        kp,   cols = csplit(cols, 3)

        d[n] = (_, labs, sem, srs, kp)

        N = n
        s = row

    return d
