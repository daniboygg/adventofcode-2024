First iteration made in zig with allocators show worse relative performance as the first day.
This iteration is made in <commit>.

| Command          |    Mean [ms] | Min [ms] | Max [ms] |    Relative |
|:-----------------|-------------:|---------:|---------:|------------:|
| `./zig`          |   23.3 ± 4.9 |     16.1 |     31.5 |        1.00 |
| `python main.py` | 148.6 ± 17.6 |    122.7 |    199.7 | 6.37 ± 1.55 |

The second iteration (actual implementation) using buffers and
[slices](https://ziglang.org/documentation/0.13.0/#Slices)
show a different conclusion though.
This comparison is not fair since I think we could implement something similar in python with
[array](https://docs.python.org/3.10/library/array.html) but it would not be my first approach.

My guess is that in a language like zig using buffers with a defined amount of memory is more common.

| Command          |    Mean [ms] | Min [ms] | Max [ms] |      Relative |
|:-----------------|-------------:|---------:|---------:|--------------:|
| `./zig`          |    1.6 ± 0.8 |      0.2 |      3.6 |          1.00 |
| `python main.py` | 151.4 ± 18.2 |    115.8 |    189.5 | 96.56 ± 53.36 |
