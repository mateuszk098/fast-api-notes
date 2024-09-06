from argparse import ArgumentParser

from app.app import run

if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("--host", default="localhost", type=str, required=False)
    p.add_argument("--port", default=8000, type=int, required=False)
    args = p.parse_args()

    run(**vars(args))
