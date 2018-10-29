import argparse
from AutoMR import AutoMR


def run(args):
	auto = AutoMR(args.filename, args.action)
	if args.action == "create-mr":
		auto.create_mr()
	elif args.action == "accept-mr":
		auto.accept_mr()
	elif args.action == "new-tag":
		auto.create_tag()
	else:
		print("Wrong action, run script with -h")


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-a", "--action", help="actions: create, accept MR or new tag", dest="action", type=str, required=True)
	parser.add_argument("-f", "--filename", help="name of file with projects list", dest="filename", type=str, required=True)
	parser.set_defaults(func=run)
	args = parser.parse_args()
	args.func(args)


if __name__ == "__main__":
	main()
