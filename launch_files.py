import subprocess
import sys
import time
    
    
    
for i in range(0, 6):
  subprocess.Popen([sys.executable, 'code/SlurmIter.py', f"{i}"])
  time.sleep(3)
  