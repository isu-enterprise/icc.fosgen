import os.path


class icc_fosgenTests:

    def setUp(self):
        pass

    def test_something(self):
        self.assertEqual(1 + 1, 2)

    def tearDown(self):
        pass


class TestsSimples:

    #    def test_str_eq(self):
    #        assert 'ОПК–2' == "ОПК-2"

    def test_extractor_competentions(self):
        from icc.fosgen.constants import extract_comps, COMPETENTIONS
        d = extract_comps(COMPETENTIONS)
        print(d)
        assert len(d) >= 3
        assert d["ОК-7"]
        assert d["ОПК-2"]
        assert d["ОПК-5"]

    def test_extractor_labs(self):
        from icc.fosgen.constants import extract_work_names, LABS
        d = extract_work_names(LABS)
        print(d)
        assert len(d) >= 5
        assert d[1]

    def test_extractor_table9(self):
        from icc.fosgen.constants import extract_table9_data, TABLE9
        from pprint import pprint
        d = extract_table9_data(TABLE9)
        # pprint(d)
        assert d


class TestTableGenerator:

    def setUp(self):
        from icc.fosgen.constants import extract_comps, COMPETENTIONS
        from icc.fosgen.constants import extract_table9_data, TABLE9
        from icc.fosgen.constants import extract_work_names, LABS
        from icc.fosgen.generator import Generator
        self.comps = extract_comps(COMPETENTIONS)
        self.table9 = extract_table9_data(TABLE9)
        self.labs = extract_work_names(LABS)

        self.gen = Generator(comps=self.comps, table9=self.table9)

    def tearDown(self):
        pass

    def save(self, filename):
        self.gen.save(os.path.join("test-results", filename + ".docx"))

    def test_paragraph_gen(self):
        self.gen.add_results(True)
        self.save("paragraph-gen")

    def test_table_9_gen(self):
        self.gen.add_table9()
        self.save("table9-gen")
