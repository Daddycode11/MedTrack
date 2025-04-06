import unittest
from django.test.runner import DiscoverRunner
from tabulate import tabulate  # Install tabulate using `pip install tabulate`
from colorama import Fore, Style

class CustomTestRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        result = unittest.TextTestRunner(verbosity=2, resultclass=ColoredTextTestResult).run(suite)
        return result


class ColoredTextTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        self.stream.write(f"{Fore.GREEN}OK{Style.RESET_ALL}\n")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.stream.write(f"{Fore.RED}FAIL{Style.RESET_ALL}\n")

    def addError(self, test, err):
        super().addError(test, err)
        self.stream.write(f"{Fore.YELLOW}ERROR{Style.RESET_ALL}\n")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.stream.write(f"{Fore.CYAN}SKIPPED{Style.RESET_ALL}\n")

    def log_results(self, result):
        table_data = []

        #

        # Process successful tests
        successful_tests = set(result.testsRun) - {failure[0] for failure in result.failures} - {error[0] for error in result.errors}
        for test in successful_tests:
            table_data.append([f"{test.__class__.__module__}.{test.__class__.__name__}.{test._testMethodName}", "PASS"])

        # Process failed tests
        for test, _ in result.failures:
            table_data.append([f"{test.__class__.__module__}.{test.__class__.__name__}.{test._testMethodName}", "FAIL"])

        # Process errored tests
        for test, _ in result.errors:
            table_data.append([f"{test.__class__.__module__}.{test.__class__.__name__}.{test._testMethodName}", "ERROR"])

        # Print the table
        print("\nTest Results Summary:")
        print(tabulate(table_data, headers=["TEST_NAME", "STATUS"], tablefmt="grid"))