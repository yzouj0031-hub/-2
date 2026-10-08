#!/usr/bin/env python3
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""
为角色卡添加三个数据库同步方案：
1. 方案1：在AI思维链中增加"数据库一致性检查"步骤
2. 方案3：添加触发词"刷新数据库"的世界书条目
3. 修改现有数据库条目，增加版本快照机制提示
"""

import json
import os
import copy
import glob

# 找到JSON文件
json_files = glob.glob(os.path.join(os.path.dirname(__file__), '*.json'))
# 排除 output.txt 等
json_files = [f for f in json_files if f.endswith('.json')]
if not json_files:
    print("ERROR: No JSON file found!")
    exit(1)

input_path = json_files[0]
print(f"Processing: {input_path}")

with open(input_path, 'r', encoding='utf-8') as f:
    card = json.load(f)

entries = card['data']['character_book']['entries']

# ============================================================
# 方案1：修改现有的"AI思维链"条目(ID 70)，增加数据库一致性检查步骤
# ============================================================

for entry in entries:
    if entry['id'] == 70:
        original_content = entry['content']
        
        # 在思维链的最后（第6步之后）追加第7步
        db_check_section = """

  ## 7. 数据库一致性验证（删回复后防错乱）
  **这是最关键的一步。** 在输出回复之前，必须执行以下检查：
  
  *   **回溯验证:** 仔细阅读当前聊天记录中**实际存在的最后几条对话**，对比〈目录〉中`TavernDB-ACU-ReadableDataTable`的各项数据（当前位置、当前时间、角色状态、事件进展等）。
  *   **不一致检测:** 如果发现数据库中记录的某些状态/事件，在当前聊天记录中**找不到对应的发生依据**（即：聊天里从未出现过导致该状态变化的对话或行动），则判定为"因删除回复导致的数据库脏数据"。
  *   **自动修正:** 对于检测到的脏数据，在本次回复的`<!--run: ... -->`指令中，将这些字段**回滚到与当前聊天记录一致的状态**。具体做法：
      - 将不一致的字段值恢复为聊天记录中能找到依据的**最后一个合理状态**。
      - 在`小总结`表中添加一条修正记录，注明"[数据库自动修正] 因上下文不一致，已回滚XX字段"。
  *   **预防原则:** 如果无法确定应该回滚到哪个值，优先采用**更早/更保守**的状态，而非更晚/更激进的状态。"""
        
        entry['content'] = original_content + db_check_section
        print(f"✅ 方案1完成: 已修改 ID 70 (AI思维链)，追加了数据库一致性验证步骤")
        break

# ============================================================
# 方案3：添加新的世界书条目——触发词"刷新数据库"
# ============================================================

new_entry_refresh = {
    "comment": "触发词-刷新数据库",
    "constant": False,
    "content": """# 🔄 数据库刷新指令

> **当{{user}}发送"刷新数据库"时，执行以下完整流程：**

## 执行步骤

### 第一步：全面扫描聊天记录
逐条回顾当前聊天中**所有实际存在的对话记录**，提取以下信息：
- {{user}}角色当前实际所在的位置
- 当前实际的游戏内时间
- 所有NPC的最后已知状态和位置
- 所有已发生的事件和其结果
- {{user}}角色的当前属性、物品、技能状态
- 所有关系变化

### 第二步：对比数据库
将扫描结果与`TavernDB-ACU-ReadableDataTable`中的每一项数据逐一对比，列出所有不一致之处。

### 第三步：生成修正报告并更新
以以下格式输出修正报告：

```
📊 数据库刷新报告
━━━━━━━━━━━━━━━━

✅ 一致项：[列出一致的关键项]

⚠️ 发现不一致：
  ┌ 字段：[字段名]
  │ 数据库值：[旧值]  
  │ 实际值：[根据聊天记录应有的值]
  └ 已修正为：[新值]

  ┌ 字段：[字段名]  
  │ ...
  └ ...

🔄 数据库已同步更新。
```

### 第四步：执行更新
在`<!--run: ... -->`指令中，将所有不一致的字段更新为正确值。同时更新`TavernDB-ACU-ImportantPersonsIndex`中的人物索引（如有变化）。

## 注意事项
- 此操作**不算作游戏内的一个回合**，不推进时间，不触发任何事件。
- 这是一个**纯粹的系统维护操作**。
- 修正完成后，恢复正常的游戏叙事模式，等待{{user}}的下一步行动。""",
    "enabled": True,
    "extensions": {
        "automation_id": "",
        "case_sensitive": None,
        "cooldown": 0,
        "delay": 0,
        "delay_until_recursion": False,
        "depth": 4,
        "display_index": 0,
        "exclude_recursion": False,
        "group": "",
        "group_override": False,
        "group_weight": 100,
        "ignore_budget": False,
        "match_character_depth_prompt": False,
        "match_character_description": False,
        "match_character_personality": False,
        "match_creator_notes": False,
        "match_persona_description": False,
        "match_scenario": False,
        "match_whole_words": None,
        "outlet_name": "",
        "position": 0,
        "prevent_recursion": False,
        "probability": 100,
        "role": 0,
        "scan_depth": None,
        "selectiveLogic": 0,
        "sticky": 0,
        "triggers": [],
        "useProbability": True,
        "use_group_scoring": False,
        "vectorized": False
    },
    "id": 102,
    "insertion_order": 100,
    "keys": ["刷新数据库", "同步数据库", "修复数据库", "检查数据库", "数据库刷新", "数据库同步", "数据库修复"],
    "position": "before_char",
    "secondary_keys": [],
    "selective": False,
    "use_regex": False
}

entries.append(new_entry_refresh)
print(f"✅ 方案3完成: 已添加 ID 102 (触发词-刷新数据库)")

# ============================================================
# 额外优化：在"数据库世界引擎"条目(ID 75)中增加快照提示
# ============================================================

for entry in entries:
    if entry['id'] == 75:
        # 在数据库世界引擎的开头追加一段快照机制说明
        snapshot_note = """
### 数据库快照机制（防删回复数据错乱）

**核心原则：** 数据库的状态必须始终与聊天记录中**实际存在的对话内容**保持一致。

1. **每次更新数据库时**，AI必须在`<!--run: ... -->`中明确标注本次更新了哪些字段、从什么值改为什么值。
2. **每次生成回复前**，AI必须快速检查：当前数据库的状态是否与聊天记录中的实际事件匹配。如果发现"数据库记录了某件事发生了，但聊天记录中找不到这件事"的情况，则自动回滚该条记录。
3. **当{{user}}发送"刷新数据库"时**，执行全面的数据库一致性检查和修复。

"""
        entry['content'] = snapshot_note + entry['content']
        print(f"✅ 额外优化完成: 已修改 ID 75 (数据库世界引擎)，追加了快照机制说明")
        break

# ============================================================
# 保存修改后的角色卡
# ============================================================

output_path = os.path.join(os.path.dirname(input_path), os.path.splitext(os.path.basename(input_path))[0] + '_已修改.json')

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(card, f, ensure_ascii=False, indent=2)

print(f"\n🎉 全部完成! 修改后的角色卡已保存至:")
print(f"   {output_path}")
print(f"\n修改总结:")
print(f"   1. [方案1] 修改了AI思维链(ID 70)，增加了自动数据库一致性验证步骤")
print(f"   2. [方案3] 新增触发词条目(ID 102)，发送'刷新数据库'即可触发全面检查")
print(f"   3. [额外] 在数据库世界引擎(ID 75)中增加了快照机制说明")
print(f"\n使用方法:")
print(f"   1. 将修改后的 JSON 文件导入酒馆即可自动生效")
print(f"   2. 正常聊天时，AI会自动检查数据库一致性（方案1）")
print(f"   3. 如需手动刷新，发送 '刷新数据库' 即可（方案3）")
