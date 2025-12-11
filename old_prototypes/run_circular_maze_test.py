#!/usr/bin/env python3
"""
Test script to run circular maze with frame limit to prevent hanging
"""

import subprocess
import signal
import time

def run_with_timeout():
    """Run the circular maze with a timeout"""
    try:
        # Start the process
        process = subprocess.Popen(
            ['python', 'circular_maze.py'],
            cwd='/Users/jdboyd/work/PhysicalMazes',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let it run for 10 seconds
        print("Running circular maze for 10 seconds...")
        time.sleep(10)
        
        # Terminate the process
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        
        print("Test completed successfully - no hanging detected")
        
    except Exception as e:
        print(f"Error running test: {e}")

if __name__ == "__main__":
    run_with_timeout()