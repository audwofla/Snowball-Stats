from src.pipeline.run import run_pipeline

if __name__ == "__main__":
    patch = run_pipeline()
    print(f"Built champion dataset for patch {patch}")
