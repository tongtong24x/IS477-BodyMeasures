import subprocess
from pathlib import Path
import sys

# BASESCRIPTS_DIR_DIR = Path("/Users/ooooona/Downloads/477")
SCRIPTS_DIR = Path(__file__).resolve().parent


def run(script_name: str) -> None:
    script_path = SCRIPTS_DIR / script_name
    print(f"\n[run_all] Running {script_path} ...")
    subprocess.run([sys.executable, str(script_path)], check=True)


def main() -> None:
    steps = [
        "process_mendeley.py",
        "process_nhanes.py",
        "integrate_datasets.py",
        "quality_report.py",
        "analysis_clustering.py",
        "integrated_analysis.py",
    ]

    for script in steps:
        run(script)

    print("\n[run_all] Done. All steps finished.")


if __name__ == "__main__":
    main()
