# ECE567 Project 7 Benchmarking

### Setup:
```bash
$ uv sync
```
If you encounter installation errors with `pettingzoo[all]`, comment it out of the `pyproject.toml` and try to install it in your venv some other way. Good luck.

If you have `nix` installed on your system, instead run
```bash
$ nix develop
```
to get a fully replicated environment. This automatically syncs uv and drops you into the venv.


### Running Benchmarks
```bash
$ python3 pettingzoo_bench.py
$ python3 vmas_bench.py
$ python3 render_results.py
```
