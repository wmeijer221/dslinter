"""Class which tests DeterministicAlgorithmChecker."""
import astroid
import pylint.testutils
import dslinter


class TestDeterministicAlgorithmChecker(pylint.testutils.CheckerTestCase):
    """Class which tests DeterministicAlgorithmChecker."""

    CHECKER_CLASS = dslinter.plugin.DeterministicAlgorithmChecker

    def test_with_deterministic_option_set(self):
        """Test whether no message is added if the deterministic algorithm option is used."""
        script = """
        import torch #@
        torch.use_deterministic_algorithms(True) #@
        """
        import_node, call_node = astroid.extract_node(script)
        with self.assertNoMessages():
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)

    def test_without_deterministic_option_set(self):
        """Test whether a message is added if the deterministic algorithm option is not used"""
        script = """
        import torch #@
        torch.randn(10).index_copy(0, torch.tensor([0]), torch.randn(1)) #@
        """
        import_node, call_node = astroid.extract_node(script)
        with self.assertAddsMessages(pylint.testutils.MessageTest(msg_id="deterministic-pytorch", node = call_node)):
            self.checker.visit_import(import_node)
            self.checker.visit_call(call_node)