# analysis-forms

## Usase

```sh
pipenv run python run.py
```

## Format of import data

Import data must has the headers like below:

```csv
ID,開始時刻,完了時刻,メール,名前,1班_発表資料,...アドバイス,2班_発表資料,...,
```

The 5 left side columns is ignored.

Remained N columns is devided given number(it specity on web interface).
Devideds will be like:

```csv
n班_発表資料,...,アドバイス
```

The scores must be `[1..5]`.
If cannot give score to group because it your own group, fill `0`. ( `0` will be ignore on aggregate.)

The `アドバイス` columns can have another name.
It can include empty cells too.


