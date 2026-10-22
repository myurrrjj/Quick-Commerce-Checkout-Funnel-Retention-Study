import os
import runpy
import pandas as pd

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)


def run(name):
    print("\n" + "=" * 60)
    print("running", name)
    print("=" * 60)
    runpy.run_path(os.path.join(here, name), run_name="__main__")


run("gen_data.py")
run("analyze.py")
run("charts.py")
run("load_db.py")

k = pd.read_csv(os.path.join(root, "outputs", "kpi_summary.csv"), header=None, index_col=0)
print("\n" + "=" * 60)
print("KPI SUMMARY")
print("=" * 60)
print(k.to_string(header=False))
