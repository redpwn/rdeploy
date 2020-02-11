import os, yaml, subprocess
from util import get_key

config = eval(open("config/config.json", "r").read().strip())
build_config = eval(open(config["exportDirectory"] + "/config.json", "r").read().strip())

def deploy(up=True):
  baseDir = config["problemDirectory"]

  cats = [(baseDir + "/" + x) for x in os.listdir(baseDir) if not x.startswith(".") and os.path.isdir(baseDir + "/" + x)]
 
  for cat in cats:
    problems = [(cat + "/" + x) for x in os.listdir(cat) if not x.startswith(".") and os.path.isdir(cat + "/" + x)]

    for problem in problems:
      key = get_key(problem, baseDir)
      port = None
      for d in build_config:
        if d["id"] == key:
          port = d["port"]

      assert port != None
      
      if os.path.exists(problem + "/docker-compose.yml"):
        p = subprocess.Popen(["docker-compose", "up" if up else "down", "-d"], cwd=problem, env={"PORT": str(port)})
        
        stdout, stderr = p.communicate()
        
        if p.returncode == 0:
          print("Successfully deployed " + problem)
        else:
          print("Error when deploying " + problem)

if __name__ == "__main__":
  deploy()
