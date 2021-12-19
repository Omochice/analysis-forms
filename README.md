# analysis-forms

## Usase

Must register `SEC_WORD` as environment variable.
I recommend that using `.env` is useful because `pipenv` load it automatically.

```sh
pipenv run server
```

## Format of import data

Import data must has the headers like below:

```csv
ID,開始時刻,完了時刻,メール,名前,1班_発表資料,...アドバイス,2班_発表資料,...,
```

You can use group name like `[0-9０-９A-Za-z]班?`.

`_` is needed because it use as separater.

5 left side columns is ignored.

Remained N columns is devided given number(it specity on web interface).
Devideds will be like:

```csv
n班_発表資料,...,アドバイス
```

The scores must be `[1..5]`.
If cannot give score to group because it your own group, fill `0`. ( `0` will be ignore on aggregate.)

The `アドバイス` columns can have another name.
It can include empty cells too.


