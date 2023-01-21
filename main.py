from note import *
from cli import *
import sys

notes = Notes()
cli = CLI(notes)

#np.save('notes', notes.notes)

def main() -> int:
	cli.startup()
	while cli.state != 0:
		if cli.state == 1:
			cli.menu()
		elif cli.state == 2:
			cli.practice()
		elif cli.state == 3:
			cli.analyze()
		elif cli.state == 4:
			cli.listen()

	

if __name__ == '__main__':
	sys.exit(main())
