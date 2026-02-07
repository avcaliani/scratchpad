# 🥑 Positional File

![#](https://img.shields.io/badge/apache--spark-3.0.x-darkorange.svg)

This is an example of writing a single positinal file.  
In this example I'm using a [Avocado Prices](https://www.kaggle.com/neuromusic/avocado-prices) dataset, so thanks to [Justin Kiggins](https://www.kaggle.com/neuromusic) for sharing his dataset.

The important thing here is the code, but if you want to execute it there is a `run.sh` to help you out.

```sh
bash -x run.sh
```

### Positional File Contract

| Order | Field         | Type     | Size   | Observation                         |
|:-----:|---------------|----------|--------|-------------------------------------|
| 1     | Date          | `string` | `08`   | Date Pattern 👉 `yyyyMMdd`.         |
| 2     | Average Price | `float`  | `12`   | The last 2 digits are the decimals. |
| 3     | Total Volume  | `int`    | `10`   |                                     |
| 4     | Region        | `string` | `25`   | Must be in upper case.              |

> 💡 Characters per line = `55`.

For extra characters fill:

- `strings` with "whitespace" (` `).
- `float` and `int` with "zero" (`0`).

#### Data x File Example

Input data example.

```yml
date: "2020-09-01"
average_price: 11.50
total_volume: 1050
region: "Brazil"
```

Expected output file.

```text
202009010000000011500000001050                   BRAZIL
```

### Output

```bash
wc -l data/avocado.csv 
# 18250 data/avocado.csv

wc -l data/AVOCADO.TXT
# 18249 data/AVOCADO.TXT
# 1 line is missing, but it is the CSV header.

head data/AVOCADO.TXT
# 201501040000000001220004087328                   ALBANY
# 201501040000000001790000137395                   ALBANY
# 201501040000000000100043502149                  ATLANTA
# 201501040000000001760000384669                  ATLANTA
# 201501040000000001080078802506      BALTIMOREWASHINGTON
# 201501040000000001290001913728      BALTIMOREWASHINGTON
# 201501040000000001010008003432                    BOISE
# 201501040000000001640000150512                    BOISE
# 201501040000000001020004917380                   BOSTON
# 201501040000000001830000219213                   BOSTON
```

### Further Help

If you want to execute this code locally you have to download the dataset from [Kaggle](https://www.kaggle.com/neuromusic/avocado-prices) and then add the file into the folder `./data/`.
