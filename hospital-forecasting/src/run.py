import argparse
import importlib

STEPS = {
    "generate": "src.data_gen.generate_admissions",
    "upload": "src.load.upload_to_gcs",
    # Add more steps like "transform", "load_bq", etc.
}

def run_step(step: str):
    if step not in STEPS:
        print(f"❌ Unknown step: {step}")
        print("Available steps:", ", ".join(STEPS.keys()))
        return

    module = importlib.import_module(STEPS[step])
    if hasattr(module, "main"):
        module.main()
    else:
        print(f"❌ Module '{STEPS[step]}' does not have a 'main()' function.")

def main():
    parser = argparse.ArgumentParser(description="Run pipeline steps.")
    parser.add_argument("--step", required=True, help=f"Step to run: {', '.join(STEPS.keys())}")
    args = parser.parse_args()
    run_step(args.step)

if __name__ == "__main__":
    main()
