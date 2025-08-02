#!/usr/bin/env python3
"""
Comprehensive Automated Testing Suite for Danger Rose
======================================================

This script runs all automated tests to detect visual and audio bugs.
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))


class AutomatedTestRunner:
    """Runs all automated tests and generates a comprehensive report."""

    def __init__(self):
        self.results_dir = Path("automated_test_results")
        self.results_dir.mkdir(exist_ok=True)

        self.session_dir = self.results_dir / datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_dir.mkdir(exist_ok=True)

        self.test_results = {}

    def run_all_tests(self, quick_mode: bool = False) -> dict[str, Any]:
        """Run all automated tests."""
        print("🤖 DANGER ROSE AUTOMATED TEST SUITE")
        print("=" * 60)
        print(f"Session: {self.session_dir.name}")
        print(f"Mode: {'Quick' if quick_mode else 'Full'}")
        print("=" * 60)

        start_time = time.time()

        # Define test suite
        tests = [
            {
                "name": "Audio Validation",
                "module": "audio_validator",
                "class": "AudioValidator",
                "method": "run_validation",
                "critical": True,
            },
            {
                "name": "Visual Regression",
                "module": "visual_regression_tester",
                "class": "VisualRegressionTester",
                "method": "run_visual_tests",
                "critical": True,
            },
            {
                "name": "Game Integration",
                "module": "automated_game_tester",
                "class": "AutomatedGameTester",
                "method": "run_automated_test",
                "args": {"duration_seconds": 30 if quick_mode else 120},
                "critical": False,
            },
        ]

        # Run each test
        for test in tests:
            print(f"\n🧪 Running: {test['name']}...")
            try:
                result = self._run_test(test)
                self.test_results[test["name"]] = result

                # Print immediate feedback
                if result.get("status") == "passed":
                    print(f"✅ {test['name']} - PASSED")
                else:
                    print(f"❌ {test['name']} - FAILED")
                    if test.get("critical"):
                        print(
                            "⚠️  Critical test failed - subsequent tests may be affected"
                        )

            except Exception as e:
                print(f"💥 {test['name']} - CRASHED: {str(e)}")
                self.test_results[test["name"]] = {
                    "status": "crashed",
                    "error": str(e),
                    "critical": test.get("critical", False),
                }

        # Generate comprehensive report
        total_time = time.time() - start_time
        report = self._generate_comprehensive_report(total_time)

        # Save report
        report_path = self.session_dir / "comprehensive_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        # Generate HTML report
        self._generate_html_report(report)

        # Print summary
        self._print_final_summary(report)

        return report

    def _run_test(self, test_config: dict) -> dict[str, Any]:
        """Run a single test."""
        try:
            # Import test module
            module = __import__(test_config["module"])
            test_class = getattr(module, test_config["class"])

            # Create test instance
            output_dir = self.session_dir / test_config["name"].lower().replace(
                " ", "_"
            )

            if test_config["class"] == "AutomatedGameTester":
                tester = test_class(output_dir=str(output_dir))
            elif test_config["class"] == "VisualRegressionTester":
                reference_dir = self.results_dir / "visual_references"
                reference_dir.mkdir(exist_ok=True)
                tester = test_class(reference_dir=str(reference_dir))
            else:
                tester = test_class()

            # Run test method
            method = getattr(tester, test_config["method"])
            args = test_config.get("args", {})

            if args:
                result = method(**args)
            else:
                result = method()

            # Determine pass/fail
            status = self._determine_test_status(test_config["name"], result)

            return {
                "status": status,
                "details": result,
                "critical": test_config.get("critical", False),
            }

        except Exception as e:
            import traceback

            return {
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "critical": test_config.get("critical", False),
            }

    def _determine_test_status(self, test_name: str, result: dict) -> str:
        """Determine if test passed or failed based on results."""
        if test_name == "Audio Validation":
            if result.get("critical_issues", 0) > 0:
                return "failed"
            if result.get("total_issues", 0) > 5:
                return "warning"
            return "passed"

        if test_name == "Visual Regression":
            if result.get("visual_regressions", 0) > 0:
                return "failed"
            return "passed"

        if test_name == "Game Integration":
            if result.get("crashes", 0) > 0:
                return "failed"
            if (
                result.get("visual_bugs", 0) > 5
                or result.get("performance_issues", 0) > 10
            ):
                return "warning"
            return "passed"

        return "unknown"

    def _generate_comprehensive_report(self, total_time: float) -> dict[str, Any]:
        """Generate comprehensive test report."""
        # Count results
        passed = sum(
            1 for r in self.test_results.values() if r.get("status") == "passed"
        )
        failed = sum(
            1 for r in self.test_results.values() if r.get("status") == "failed"
        )
        warnings = sum(
            1 for r in self.test_results.values() if r.get("status") == "warning"
        )
        crashed = sum(
            1 for r in self.test_results.values() if r.get("status") == "crashed"
        )

        # Aggregate issues
        total_issues = 0
        critical_issues = 0

        for test_name, result in self.test_results.items():
            if result.get("status") != "crashed":
                details = result.get("details", {})

                if test_name == "Audio Validation":
                    total_issues += details.get("total_issues", 0)
                    critical_issues += details.get("critical_issues", 0)
                elif test_name == "Visual Regression":
                    total_issues += details.get("visual_regressions", 0)
                    if details.get("visual_regressions", 0) > 0:
                        critical_issues += 1
                elif test_name == "Game Integration":
                    total_issues += details.get("visual_bugs", 0)
                    total_issues += details.get("audio_bugs", 0)
                    total_issues += details.get("performance_issues", 0)
                    critical_issues += details.get("crashes", 0)

        report = {
            "session": self.session_dir.name,
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": total_time,
            "summary": {
                "total_tests": len(self.test_results),
                "passed": passed,
                "failed": failed,
                "warnings": warnings,
                "crashed": crashed,
                "total_issues": total_issues,
                "critical_issues": critical_issues,
            },
            "test_results": self.test_results,
            "recommendations": self._generate_recommendations(),
        }

        return report

    def _generate_recommendations(self) -> list[str]:
        """Generate recommendations based on test results."""
        recommendations = []

        # Check audio issues
        audio_result = self.test_results.get("Audio Validation", {})
        if audio_result.get("status") == "failed":
            details = audio_result.get("details", {})
            if (
                details.get("test_results", {})
                .get("file_validation", {})
                .get("missing")
            ):
                recommendations.append(
                    "🔊 Add missing audio files to prevent runtime errors"
                )
            if details.get("critical_issues", 0) > 0:
                recommendations.append(
                    "🔊 Fix critical audio issues (corrupted files, playback failures)"
                )

        # Check visual issues
        visual_result = self.test_results.get("Visual Regression", {})
        if visual_result.get("status") == "failed":
            recommendations.append(
                "🎨 Review visual regressions and update reference images if changes are intentional"
            )

        # Check game integration issues
        game_result = self.test_results.get("Game Integration", {})
        if game_result.get("status") in ["failed", "warning"]:
            details = game_result.get("details", {})
            if details.get("crashes", 0) > 0:
                recommendations.append(
                    "🐛 Fix game crashes immediately - check crash reports for details"
                )
            if details.get("visual_bugs", 0) > 5:
                recommendations.append(
                    "🎮 Investigate visual bugs (missing sprites, black screens)"
                )
            if details.get("performance_issues", 0) > 10:
                recommendations.append("⚡ Optimize performance to maintain 60 FPS")

        if not recommendations:
            recommendations.append("✨ All tests passed! The game is in good shape.")

        return recommendations

    def _generate_html_report(self, report: dict[str, Any]) -> None:
        """Generate an HTML report for easy viewing."""
        html_path = self.session_dir / "report.html"

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Danger Rose Test Report - {report["session"]}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: #333; color: white; padding: 20px; border-radius: 8px; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .warning {{ color: #ffc107; }}
        .crashed {{ color: #6c757d; }}
        .test-result {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; }}
        .recommendations {{ background: #e9ecef; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎮 Danger Rose Automated Test Report</h1>
        <p>Session: {report["session"]} | Duration: {report["duration_seconds"]:.1f}s</p>
    </div>

    <div class="summary">
        <div class="stat-card">
            <h3>Tests Run</h3>
            <h2>{report["summary"]["total_tests"]}</h2>
        </div>
        <div class="stat-card">
            <h3 class="passed">Passed</h3>
            <h2 class="passed">{report["summary"]["passed"]}</h2>
        </div>
        <div class="stat-card">
            <h3 class="failed">Failed</h3>
            <h2 class="failed">{report["summary"]["failed"]}</h2>
        </div>
        <div class="stat-card">
            <h3 class="warning">Warnings</h3>
            <h2 class="warning">{report["summary"]["warnings"]}</h2>
        </div>
        <div class="stat-card">
            <h3>Total Issues</h3>
            <h2>{report["summary"]["total_issues"]}</h2>
        </div>
    </div>

    <div class="recommendations">
        <h3>📋 Recommendations</h3>
        <ul>
        {"".join(f"<li>{rec}</li>" for rec in report["recommendations"])}
        </ul>
    </div>

    <h2>Test Results</h2>
    {self._generate_test_results_html(report["test_results"])}

</body>
</html>
        """

        with open(html_path, "w") as f:
            f.write(html_content)

    def _generate_test_results_html(self, test_results: dict) -> str:
        """Generate HTML for test results."""
        html = ""

        for test_name, result in test_results.items():
            status = result.get("status", "unknown")
            status_class = status

            html += f"""
            <div class="test-result">
                <h3>{test_name} - <span class="{status_class}">{status.upper()}</span></h3>
            """

            if status == "crashed":
                html += f"<p>Error: {result.get('error', 'Unknown error')}</p>"
            else:
                details = result.get("details", {})

                if test_name == "Audio Validation":
                    file_val = details.get("test_results", {}).get(
                        "file_validation", {}
                    )
                    html += f"""
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        <tr><td>Files Expected</td><td>{file_val.get("total_expected", 0)}</td></tr>
                        <tr><td>Files Found</td><td>{file_val.get("found", 0)}</td></tr>
                        <tr><td>Missing Files</td><td>{len(file_val.get("missing", []))}</td></tr>
                        <tr><td>Total Issues</td><td>{details.get("total_issues", 0)}</td></tr>
                        <tr><td>Critical Issues</td><td>{details.get("critical_issues", 0)}</td></tr>
                    </table>
                    """

                elif test_name == "Visual Regression":
                    html += f"""
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        <tr><td>Total Tests</td><td>{details.get("total_tests", 0)}</td></tr>
                        <tr><td>Screenshots</td><td>{details.get("total_screenshots", 0)}</td></tr>
                        <tr><td>Visual Regressions</td><td>{details.get("visual_regressions", 0)}</td></tr>
                    </table>
                    """

                elif test_name == "Game Integration":
                    html += f"""
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        <tr><td>Test Duration</td><td>{details.get("test_duration", 0):.1f}s</td></tr>
                        <tr><td>Average FPS</td><td>{details.get("average_fps", 0):.1f}</td></tr>
                        <tr><td>Visual Bugs</td><td>{details.get("visual_bugs", 0)}</td></tr>
                        <tr><td>Audio Bugs</td><td>{details.get("audio_bugs", 0)}</td></tr>
                        <tr><td>Performance Issues</td><td>{details.get("performance_issues", 0)}</td></tr>
                        <tr><td>Crashes</td><td>{details.get("crashes", 0)}</td></tr>
                    </table>
                    """

            html += "</div>"

        return html

    def _print_final_summary(self, report: dict[str, Any]) -> None:
        """Print final test summary."""
        print("\n" + "=" * 60)
        print("🏁 FINAL TEST SUMMARY")
        print("=" * 60)

        summary = report["summary"]
        print(f"Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed']}")
        print(f"❌ Failed: {summary['failed']}")
        print(f"⚠️  Warnings: {summary['warnings']}")
        print(f"💥 Crashed: {summary['crashed']}")

        print(f"\n🐛 Total Issues Found: {summary['total_issues']}")
        print(f"🚨 Critical Issues: {summary['critical_issues']}")

        print("\n📋 Recommendations:")
        for rec in report["recommendations"]:
            print(f"  {rec}")

        print(f"\n📊 Full reports saved to: {self.session_dir}")
        print("🌐 Open report.html in a browser for detailed results")

        # Determine exit status
        if summary["failed"] > 0 or summary["crashed"] > 0:
            print("\n❌ TESTS FAILED - Please fix issues before release")
            return 1
        if summary["warnings"] > 0:
            print("\n⚠️  TESTS PASSED WITH WARNINGS - Review before release")
            return 2
        print("\n✅ ALL TESTS PASSED - Game is ready!")
        return 0


def main():
    """Run automated tests."""
    import argparse

    parser = argparse.ArgumentParser(description="Run automated tests for Danger Rose")
    parser.add_argument(
        "--quick", action="store_true", help="Run quick tests (30s instead of 2min)"
    )
    parser.add_argument(
        "--visual-only", action="store_true", help="Run only visual tests"
    )
    parser.add_argument(
        "--audio-only", action="store_true", help="Run only audio tests"
    )

    args = parser.parse_args()

    # Install dependencies if needed
    try:
        pass
    except ImportError:
        print("Installing required dependencies...")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "mutagen",
                "numpy",
                "pillow",
                "scipy",
            ]
        )

    runner = AutomatedTestRunner()

    if args.visual_only:
        # Run only visual tests
        from visual_regression_tester import VisualRegressionTester

        tester = VisualRegressionTester()
        report = tester.run_visual_tests()
        return 0 if report["visual_regressions"] == 0 else 1

    if args.audio_only:
        # Run only audio tests
        from audio_validator import AudioValidator

        validator = AudioValidator()
        report = validator.run_validation()
        return 0 if report["critical_issues"] == 0 else 1

    # Run all tests
    report = runner.run_all_tests(quick_mode=args.quick)

    summary = report["summary"]
    if summary["failed"] > 0 or summary["crashed"] > 0:
        return 1
    if summary["warnings"] > 0:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
