#### Quantity initialization

| Code syntax        | Information           |
| ------------- |:-------------:|
| A = Quantity('Name', [Quantity Space])| Instantiating a quantity|
| A.Iplus(B, bi_dir=False) | A influences B positvely|
| A.Imin(B, bi_dir=False) | A influences B negatively|
| A.Pplus(B, bi_dir=False) | A influences B positvely proportionally|
| A.Pmin(B, bi_dir=False) | A influences B negatively proportionally|
| ValueConstraint(A(valueA), B(valueB)) |  When A's value is valueA then B's value is valueB|

