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
if rc:
 # Keep the full artifact and expose an actionable tail in CI annotations.
 import os, re
 lines = log.read_text(errors="replace").splitlines()
 # Docker's footer repeats the entire failed RUN instruction. Prefer actual
 # timestamped step output and stay below GitHub's 4096-character annotation cap.
 build_output = [line for line in lines if re.match(r"^#\d+\s+[\d.]+\s", line)]
 tail = "\n".join(line[:500] for line in (build_output or lines)[-30:])[-3500:]
 print(tail, flush=True)
 if os.environ.get("GITHUB_ACTIONS") == "true":
  escaped = tail.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
  print("::error title=Build or test command failed::" + escaped, flush=True)
sys.exit(rc)
