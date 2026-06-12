# Elevator

This is an example of a temporal encoding modeling elevator movements between
different floors

## Usage

### Asymteric Example

- `instances/02_asymetric.lp`
- `encoding.lp`
- `encoding_addables.lp`

```bash
asplain examples/elevator/encoding.lp examples/elevator/encoding_addables.lp examples/elevator/instances/02_asymetric.lp 1 --query="holds(at(1),2)" --prune=CHANGES --open
```
