# radical-algebra

Tensor algebra on Chinese radicals — find valid CJKV character combinations via outer products and higher-rank tensor operations.

## Concept

Treat Chinese radicals as elements of a vector space. Tensor operations (outer products) generate compound characters, validated against CJKV Unicode (excluding simplified Chinese).

### Rank-2 Example: Wu Xing (五行) Outer Product

Given the Five Elements as a vector:

```
v = (金, 木, 水, 火, 土)ᵀ
```

The outer product v ⊗ vᵀ yields a 5×5 matrix of two-radical compounds:

```
         金    木    水    火    土
      ┌                            ┐
  金  │  鑫    鉢    淦    钬    钍  │
  木  │  鉢    林    沐    杣    杜  │
  水  │  淦    沐    淼    淡    汢  │
  火  │  钬    杣    淡    炎    灶  │
  土  │  钍    杜    汢    灶    圭  │
      └                            ┘
```

### Higher-Rank Tensors

Extend to rank-3 (three-radical), rank-4, rank-5 combinations:

```
Rank-3: v ⊗ v ⊗ v → 5×5×5 tensor (e.g., 鑫 = 金+金+金, 森 = 木+木+木, 淼 = 水+水+水)
Rank-4: v ⊗ v ⊗ v ⊗ v → 5×5×5×5 tensor
```

## Features

- **Predefined radical sets**: Wu Xing (五行), extensible to custom sets
- **CJKV validation**: Only output valid Unicode characters (CJK Unified Ideographs), excluding simplified Chinese
- **Tensor operations**: Support rank 2-5 outer products
- **Mathematical notation**: Text-based output with proper tensor notation

## Installation

```bash
# Using uv
uv pip install radical-algebra

# From source
git clone https://github.com/tianjianjiang/radical-algebra.git
cd radical-algebra
uv sync
```

## Usage

```python
from radical_algebra import RadicalSet, outer_product

# Define Wu Xing elements
wuxing = RadicalSet("五行", ["金", "木", "水", "火", "土"])

# Rank-2: Matrix of two-radical compounds
matrix = outer_product(wuxing, rank=2)
print(matrix)

# Rank-3: Tensor of three-radical compounds
tensor3 = outer_product(wuxing, rank=3)
print(tensor3)
```

## License

MIT
