import yaml, os, sys

def exists(file):
  return os.path.isfile(file)

def touch(file):
  with open(file, 'a'):
    os.utime(file, None)

file = os.path.dirname(__file__) + "/config.yaml"

def load_conf():
  with open(file, "r") as ymlfile:
    return yaml.safe_load(ymlfile)

def gen_conf():
  g = {
    'postgresql' : {
      'host' : 'localhost',
      'port' : '5432',
      'user' : 'username',
      'pass' : 'password',
      'db' : 'bnbwithme'
    }
  }
  out = yaml.dump(g, Dumper=yaml.CDumper, default_flow_style=False)
  touch(file)

  with open(file, 'w') as f:
    f.writelines(out)

def get():
  if exists(file):
    return load_conf()
  gen_conf()
  print("Conf generated at \'{}\', fill that in before starting".format(file))
  sys.exit(0)

