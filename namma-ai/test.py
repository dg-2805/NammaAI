import json
import csv
import time
from datetime import datetime
from pathlib import Path
from main import generate_response

# Load test queries
def load_queries(file_path):
    if file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError("Only JSON supported.")

# Run all queries through the agent
def run_tests(input_file, output_file="test_results.csv"):
    queries = load_queries(input_file)
    results = []

    print(f"Running {len(queries)} test queries...")
    
    for i, q in enumerate(queries):
        query = q["query"]
        expected_persona = q["persona"]
        test_type = q.get("test_type", "unknown")
        
        try:
            response, detected_persona = generate_response(query)
            print(f"[{i+1:02}] ✅ Query: {query[:60]}... → Detected: {detected_persona}")
        except Exception as e:
            response = f"ERROR: {str(e)}"
            detected_persona = "error"
            print(f"[{i+1:02}] ❌ Failed to run query: {query}")

        results.append({
            "query": query,
            "expected_persona": expected_persona,
            "detected_persona": detected_persona,
            "test_type": test_type,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        time.sleep(1)  # Optional: pause to avoid rate limits

    # Save results to CSV
    keys = results[0].keys()
    with open(output_file, "w", newline="", encoding="utf-8") as out_csv:
        writer = csv.DictWriter(out_csv, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n📝 Test run complete. Results saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    test_file = "query/queries.json"  # or .csv
    run_tests(test_file)
