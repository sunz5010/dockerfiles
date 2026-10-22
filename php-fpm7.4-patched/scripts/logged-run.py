#!/usr/bin/env python3
import subprocess, sys, json, datetime
from pathlib import Path
log=Path(sys.argv[1]); log.parent.mkdir(parents=True,exist_ok=True)
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with log.open("w") as f:
 f.write("COMMAND: "+repr(sys.argv[2:])+"\n"); f.flush()
 rc=subprocess.run(sys.argv[2:],stdout=f,stderr=subprocess.STDOUT).returncode
with log.open("a") as f: f.write("\nEXIT_CODE: "+str(rc)+"\n")
with (log.parent/"commands.jsonl").open("a") as f: f.write(json.dumps(dict(start=start,command=sys.argv[2:],exit_code=rc,log=str(log)))+"\n")
print(str(log)+": exit "+str(rc),flush=True)
sys.exit(rc)
