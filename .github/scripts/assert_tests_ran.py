#!/usr/bin/env python3
"""Fail CI when a green pytest exit code does not mean the suite ran.

A passing run is not evidence of coverage: a collection error, an over-broad
--ignore, or a bad fixture can leave the suite reporting success having executed
almost nothing. The failure mode is invisible precisely because the exit code
is 0.
"""
import sys
import xml.etree.ElementTree as ET

# Floor, not a target. Only trips if coverage regresses; adding tests is free.
MIN_TESTS = 90


def main(path):
    root = ET.parse(path).getroot()
    suites = root.findall("testsuite") or [root]

    total = errors = failures = skipped = 0
    for suite in suites:
        total += int(suite.get("tests", 0))
        errors += int(suite.get("errors", 0))
        failures += int(suite.get("failures", 0))
        skipped += int(suite.get("skipped", 0))

    executed = total - skipped - errors
    print(
        "collected={} executed={} failures={} errors={} skipped={}".format(
            total, executed, failures, errors, skipped
        )
    )

    problems = []
    if errors:
        problems.append("{} collection/setup error(s)".format(errors))
    if executed < MIN_TESTS:
        problems.append(
            "only {} test(s) executed, expected at least {}".format(
                executed, MIN_TESTS
            )
        )

    if problems:
        print("FAIL: " + "; ".join(problems), file=sys.stderr)
        return 1

    print("OK: suite executed {} tests".format(executed))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
