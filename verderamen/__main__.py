from .manager import Manager

def main():
  manager = Manager()
  print('Manager setup running...')
  manager.setup()
  print('Manager setup done! Starting main loop...')
  while(True):
    manager.loop()


if __name__ == '__main__':
  main()