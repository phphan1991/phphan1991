Generator for the three roadmap sheets.

- Run `python3 layout.py` from this folder. It writes `cost-management-roadmap.html` one level up.
- `gen_core.py` holds every computed number and every SVG. Change a figure there and the charts, the
  formulas and the copy all move together, so the sheets cannot drift out of agreement with each other.
- `content.py` holds the panel copy, `fixes_data.py` the correction log, `layout.py` the page assembly.
