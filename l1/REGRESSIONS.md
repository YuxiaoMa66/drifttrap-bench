# L1 回归用例候选（决定 B11⑤：先作为 L1 回归用例记录，暂不提 issue）

均在 GMR 0.6.6（`GMR-latest/target/release/gmr`）上于 2026-09-24 实测。复现只需一个 git 仓库和 `gmr init`。

## R1 `路径#/json/pointer` 被路由到整文件探针，之后永远报漂移

- 复现：`{"timeout":60,"mode":"prod"}` 写入 `c/r.json`，`gmr anchor 'c/r.json#/timeout'` 与 `'c/r.json#/mode'`；只改 timeout。
- 现象：两个锚点都交还，状态 `drifted`，诊断 “path matched, name did not”；把文件改回原样后仍交还。换成 `#timeout`、`#$.timeout` 结果相同。
- 原因：坐标被路由到 addr-map，它的 `name` 是文件名，永远对不上。
- 正确写法：`file://c/r.json#/timeout`（`--as` 命名），只交还真正变化的键（本仓库 L1 在 CAL 上 165/165 符合）。
- 期望：带 `#` 的坐标若没有探针能按名字解析，应在 `anchor` 时拒绝，而不是静默接受。

## R2 `路径#Class.method` 被接受但从不解析

- 复现：Python 文件，`gmr anchor 'repo/pynetbox/core/query.py#Request.__init__'`。
- 现象：`anchor` 返回 probe ast-map、`barren: false`，但 position 没有 `shape`；仓库任何变化后状态为 `absent`（“nothing there answered to any of file · name”），即使该方法仍在。`Class::method` 相同。
- 对照：`#Request`（类）与 `#RequestError` 正常解析，漂移后分别为 `signature-changed`、`logic-changed`。
- 期望：同 R1，解析不到应在 `anchor` 时报错。

## R3 裸方法名有歧义

- 复现：同一文件有 `Request.__init__` 与 `RequestError.__init__`，`gmr anchor 'repo/pynetbox/core/query.py#__init__'`。
- 现象：解析到其中一个（本例是 `Request.__init__`），没有提示存在多个候选。
- 期望：有多个同名候选时报告候选数或拒绝。

## R4 `--as` 名字里的 `_` 被改成 `-`

- 现象：`--as primary_region` 得到锚点名 `primary-region`；`gmr check` 以改名后的名字交还。
- 影响：调用方按原名匹配会漏掉（本仓库 `arms/assemble.py::anchored_keys` 已做映射）。路径坐标忽略 `--as`，以坐标为名。

## R5（语义记录，非缺陷）交还是“粘性”的

- 值被某次 `check` 看到与基线不同后，一直交还，即使值改回；只有 `accept --baseline` 清除。L0 的 `tests/state_machine.rs` 以此为参考模型。
