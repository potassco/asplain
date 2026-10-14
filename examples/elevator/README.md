# Elevator

This is an example of a temporal encoding modeling elevator movements between
different floors

## Usage

### Instance-Based Explanation

- `instances/02_asymetric.lp`
- `encoding.lp`
- `encoding_addables.lp`

Query: _"Is it possible that the elevator serves the lower floor first?"_ :
`holds(at(1),2)`

```bash
asplain examples/elevator/encoding.lp examples/elevator/encoding_addables.lp examples/elevator/instances/02_asymetric.lp 1 --query="holds(at(1),2)" --temporal --open
```

### Model-Based Explanation

- `instances/03_model.lp`
- `encoding.lp`
- `models/simple.lp`

Query: _"Why does the elevator serve the upper floor first in this model"_ :
`-holds(at(3),2)`

```bash
asplain examples/elevator/encoding.lp examples/elevator/instances/03_symetric.lp 1 examples/models/03_up.lp --query="-holds(at(3),2)" --temporal --open
```
