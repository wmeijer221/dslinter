"""Class which test ChainIndexingPandasChecker."""
import astroid
import pylint.testutils

import dslinter


class TestTestDatasetRead(pylint.testutils.CheckerTestCase):
    """Class which test ChainIndexingPandasChecker."""

    CHECKER_CLASS = dslinter.plugin.DatasetApiConflict

    def test_dataset_read(self):
        """Message should be added if there is a chain indexing on pandas dataframe."""
        script = """
        import sklearn.svm
        import pandas
        df = pandas.read_csv(r'./data/my_data.csv')
        X = df[['x1', 'x2', 'x4']]
        df_labels = pandas.read_csv(r'./data/my_data_labels.csv')
        y = df_labels[['y']]
        svc = sklearn.svm.SVC(kernel='linear')
        svc.fit(X, y, sample_weights=None)
        """
        body = astroid.parse(script).body

        for node in body[2:6]:
            self.checker.visit_assign(node)

        svc_call_node = body[7].value
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="data-api-conflict", node=svc_call_node)):
            self.checker.visit_call(svc_call_node)
