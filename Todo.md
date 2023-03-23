# Todo
+ encode, solve, decode等の時間計測用クラスの作成
+ 未実装の制約作成
  + 実装済: Eq Add Mul
+ 算術演算子を用いた制約生成
  + pythonの特殊メソッドで出来ないか
    + Termとintの組み合わせでもできるのか
+ encodeクラスのdecode関数修正
  + 現在jarファイルを使いデコードしている → sugarのオプションで出来ないか
  + 現在
    + encode: sugar -n -map file.map -cnf file.cnf
    + decode: java -jar sugar-2.3.4.jar -decode file.out file.map