# final_validation.py
import requests
import time
import sys

BASE_URL = "http://127.0.0.1:8000"

def log_test_result(name, condition, execution_time=None):
    time_str = f" [{execution_time:.2f}s]" if execution_time else ""
    if condition:
        print(f"✅ [PASS] {name}{time_str}")
        return True
    else:
        print(f"❌ [FAIL] {name}{time_str}")
        return False

def run_final_stress_and_edge_suite():
    print("🔬 [EduGenie QA Operations] Commencing Final E2E Validation Sweep...\n")
    success_count = 0
    total_tests = 5

    # --- TEST 1: System Routing & Static Asset Integrity ---
    start = time.time()
    try:
        health_check = requests.get(f"{BASE_URL}/health")
        css_check = requests.get(f"{BASE_URL}/static/css/style.css")
        status = (health_check.status_code == 200 and css_check.status_code == 200)
    except Exception:
        status = False
    success_count += log_test_result("Infrastructure Layer & Static Asset Mapping", status, time.time() - start)

    # --- TEST 2: Chat Pipeline Edge Case (Empty Request Validation) ---
    start = time.time()
    try:
        res = requests.post(f"{BASE_URL}/api/v2/chat", json={"message": "", "history": []})
        # Expecting structural error code or controlled handling instead of a 500 crash
        status = (res.status_code in [400, 422, 200]) 
    except Exception:
        status = False
    success_count += log_test_result("Chat Pipeline Edge Case (Null Input Safeguards)", status, time.time() - start)

    # --- TEST 3: Cloud Gemini Stress Ingestion (Text Synthesis Speed) ---
    start = time.time()
    long_prompt = "Review this educational objective and outline it: " + ("Learning is vital. " * 150)
    try:
        res = requests.post(f"{BASE_URL}/api/v2/chat", json={"message": long_prompt, "history": []})
        status = (res.status_code == 200 and "response" in res.json())
    except Exception:
        status = False
    success_count += log_test_result("Cloud Inference Ingestion (Large Text Payload)", status, time.time() - start)

    # --- TEST 4: Local Quiz Engine Pipeline Latency Check ---
    print("\n⏳ [Inference Alert] Evaluating local Hugging Face transformer pipeline. This runs on your CPU hardware...")
    start = time.time()
    try:
        res = requests.post(f"{BASE_URL}/api/v2/quiz", json={"topic": "Quantum Mechanics", "num_questions": 2})
        status = (res.status_code == 200 and "quiz_raw" in res.json())
    except Exception:
        status = False
    quiz_time = time.time() - start
    success_count += log_test_result("Local Transformer Assessment Engine Generation", status, quiz_time)

    # --- TEST 5: Telemetry Pipeline Verification ---
    start = time.time()
    try:
        res = requests.post(f"{BASE_URL}/api/v2/recommendations", json={"score": 0, "total_questions": 5, "topic": "History"})
        status = (res.status_code == 200 and "recommendations" in res.json())
    except Exception:
        status = False
    success_count += log_test_result("Local Performance Telemetry Resolution Loop", status, time.time() - start)

    # --- SCORE EVALUATION ---
    print("\n=======================================================")
    print(f"📊 FINAL VERIFICATION SCORE: {success_count}/{total_tests} TARGETS CONFIRMED")
    print("=======================================================")
    
    if success_count == total_tests:
        print("🏆 PROJECT DEPLOYMENT SIGN-OFF: APPROVED FOR PRODUCTION")
        sys.exit(0)
    else:
        print("⚠️ PROJECT DEPLOYMENT SIGN-OFF: REJECTED (Fix failing nodes)")
        sys.exit(1)

if __name__ == "__main__":
    run_final_stress_and_edge_suite()