# main.py - Run complete demo

import subprocess
import sys

def run_step(script, description):
    print(f"\n{'='*50}")
    print(f"RUNNING: {description}")
    print(f"{'='*50}")
    result = subprocess.run(
        [sys.executable, script],
        capture_output=False
    )
    return result.returncode

if __name__ == "__main__":
    print("="*50)
    print("QUANTUM SAFE SELF-HEALING CONTRACT")
    print("Complete Demo")
    print("="*50)
    
    steps = [
        ("scripts/deploy_contract.py", 
         "Deploy Contract"),
        ("monitoring/attack_simulator.py", 
         "Attack Simulation"),
        ("results/performance_metrics.py", 
         "Performance Analysis")
    ]
    
    for script, desc in steps:
        code = run_step(script, desc)
        if code != 0:
            print(f"[ERROR] {desc} failed!")
            break
    
    print("\n[COMPLETE] Full demo finished!")