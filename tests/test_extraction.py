import json
import time
from pathlib import Path
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['jd_extractor']
user = db.users.find_one({'username': 'sai01'})
profile = db.profiles.find_one({'user_id': user['_id']})

from myapp.services.llm.client import LLMClient

TESTCASES_FILE = Path(__file__).parent / "testcases.json"
RESULTS_FILE = Path(__file__).parent / "results.json"


def load_testcases():
    with open(TESTCASES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_results(results):
    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)


def main():
    testcases = load_testcases()
    llm_client = LLMClient()
    results = []

    for testcase in testcases:
        print(f"Running testcase {testcase['id']}...")

        start_time = time.perf_counter()

        try:
            extraction = llm_client.generate_match_feedback(
                profile, testcase["description"]
            )

            end_time = time.perf_counter()
            latency = end_time - start_time

            results.append({
                "id": testcase["id"],
                "description": testcase["description"],
                "status": "success",
                "latency_seconds": round(latency, 3),
                "response": extraction.model_dump()
            })

            print(f"Completed in {latency:.3f} seconds")

        except Exception as exc:
            end_time = time.perf_counter()
            latency = end_time - start_time

            results.append({
                "id": testcase["id"],
                "description": testcase["description"],
                "status": "failed",
                "latency_seconds": round(latency, 3),
                "error": str(exc)
            })

            print(f"Failed after {latency:.3f} seconds")

    save_results(results)

    print(f"\nResults saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()