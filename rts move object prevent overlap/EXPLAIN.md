# 防止物件重疊 — 廣東話解釋

## 係咩問題？

喺 RTS 遊戲入面，如果唔做任何限制，多個單位可以疊埋一齊放，又或者移動時穿過對方，睇落好唔自然。呢個檔案解決咗呢個問題。

---

## 新增嘅常數

```js
const UNIT_RADIUS = 0.32;
```

每個單位都有個「佔地半徑」0.32 單位。兩個單位之間嘅距離一旦細過 `0.32 × 2 = 0.64`，就算係重疊。

---

## `wouldOverlap(position, excludeUnit)`

```js
function wouldOverlap(position, excludeUnit) {
    for (const unit of placedUnits) {
        if (unit === excludeUnit) continue;
        if (unit.position.distanceTo(position) < UNIT_RADIUS * 2) return true;
    }
    return false;
}
```

呢個函數係核心邏輯：
- 逐一檢查所有已放置嘅單位
- `excludeUnit` 係用嚟排除自己（移動嗰陣唔想同自己撞）
- 如果有任何單位距離目標位置細過 `UNIT_RADIUS * 2`，就返回 `true`（即係「會撞」）

---

## 放置單位時嘅保護

```js
function placeUnit(point, normal) {
    if (!selectedUnit) return;
    if (selectedUnit === 'ship' && !shipGeometry) return;
    if (wouldOverlap(point, null)) return;  // ← 新增
    ...
}
```

放單位之前先查一次，如果個位已經有人，就直接 `return`，唔放落去。

---

## 幽靈預覽變紅色

```js
isGhostValid = !wouldOverlap(point, null);
ghostMesh.traverse(child => {
    if (child.isMesh) {
        if (isGhostValid) {
            // 恢復原本顏色
        } else {
            child.material.color.set(0xff2222);   // 紅色 = 唔可以放
            child.material.emissive.set(0x440000);
        }
    }
});
```

移動滑鼠嗰陣，幽靈單位會即時顯示：
- **原本顏色** → 可以放
- **紅色** → 呢度已經有單位，唔可以放

原本顏色會保存喺 `material.userData.origColor` 同 `material.userData.origEmissive` 入面，方便之後還原。

---

## 移動時防碰撞

```js
if (wouldOverlap(newPos, unit)) {
    ud.moveProgress = 1;
    ud.moveTarget = null;
    continue;
}
```

每一幀更新單位位置之前，先算出下一個位置 `newPos`，然後查係咪會撞到其他單位。如果會撞，就即刻停低（`moveProgress = 1`，清除目標），唔再繼續移動，自然就形成「停喺對方門口」嘅效果。

---

## 總結流程

```
滑鼠移動
  └─ 幽靈預覽位置
       └─ wouldOverlap? → 紅色 / 正常色

左鍵點擊放單位
  └─ wouldOverlap? → 有：唔放 / 冇：放落去

每一幀更新移動中嘅單位
  └─ 計算下一步位置
       └─ wouldOverlap? → 有：停低 / 冇：移過去
```
