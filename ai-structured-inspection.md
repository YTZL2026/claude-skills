# AI 结构性质检引擎

## 适用场景
按预定义标准对文档/报告/表单进行逐项检查，输出结构化 JSON，再导入表单/台账/报表。

通用模式：**标准项 → LLM 逐项检查 → 结构化 JSON → 表单填充 → Excel 导出**

## 提示词模板

```python
ANALYSIS_PROMPT = """你是{domain}专家。请对照以下标准，逐项检查这份{文档类型}，输出 JSON 格式结果。

## 检查标准（{N}个大维，{M}项细则）

{标准列表——按维度分组，每项编号}

## 一票否决项

{触发即不合格的严重问题列表}

## 输出格式（严格 JSON，不要任何解释）
{
  "subject_name": "被检查对象名称",
  "subject_id": "编号",
  "category": "分类/科室",
  "handler": "负责人",
  "summary": "一句话总结",
  "items": [
    {
      "dimension": "维度名",
      "item": "检查项名称",
      "status": "pass/fail/na",
      "finding": "发现的问题描述",
      "responsible": "责任人",
      "severity": "high/medium/low"
    }
  ],
  "veto_items": ["触及的一票否决项"],
  "overall_pass": true,
  "score": 85
}

## 规则
1. 合格项不列入 items（减少输出长度）
2. 描述用专业客观措辞，如"需关注""建议完善"
3. 负责任从文档中提取署名，无署名填"待确认"
4. 只输出 JSON，不要任何解释性文字
"""
```

## 调用示例

```python
def analyze_document(filepath):
    with open(filepath, encoding='utf-8') as f:
        text = f.read()[:8000]  # 截断控制 token

    cfg = load_config()['llm']
    result = call_llm([
        {'role': 'system', 'content': ANALYSIS_PROMPT},
        {'role': 'user', 'content': f'请分析：\n\n{text}'}
    ], {**cfg, 'max_tokens': 1500, 'temperature': 0.1})
    # temperature=0.1 保证输出一致性

    # 从回复中提取 JSON（LLM 可能包裹在 markdown 中）
    import re
    m = re.search(r'\{[\s\S]*\}', result)
    if not m:
        return None  # 解析失败
    return json.loads(m.group())
```

## 前端对接：JSON → 表单自动填充

```javascript
function fillFormFromResult(analysis) {
  // 1. 基本信息
  document.getElementById('subjectName').value = analysis.subject_name;
  document.getElementById('handler').value = analysis.handler;

  // 2. 逐项匹配到表单行
  const items = analysis.items || [];
  items.forEach(item => {
    // 用文本相似度或关键词匹配找到对应表单行
    const row = findMatchingRow(item.dimension, item.item);
    if (row) {
      row.querySelector('textarea').value = item.finding;
      row.querySelector('.person input').value = item.responsible;
    }
  });

  // 3. 一票否决勾选
  (analysis.veto_items || []).forEach(v => {
    document.querySelector(`[data-label="${v}"]`).checked = true;
  });
}

function findMatchingRow(dimension, itemName) {
  // 匹配策略：去数字/去标点/共有字比例
  const norm = s => s.replace(/[\d\.\s、，,（）()【】\[\]\/\-]/g, '');
  let best = null, bestScore = 0;
  document.querySelectorAll('.dim-row').forEach(row => {
    const label = row.querySelector('.label').textContent;
    const na = norm(itemName), nb = norm(label);
    const score = [...na].filter(c => nb.includes(c)).length / Math.max(na.length, nb.length);
    if (score > bestScore && score > 0.2) { bestScore = score; best = row; }
  });
  return best;
}
```

## 可复用的业务模式

| 场景 | 标准来源 | 输出 |
|------|---------|------|
| 病历质控 | 六维34项质控标准 | 缺陷台账 Excel |
| 合同审查 | 法务审查清单 | 风险点汇总 |
| 代码审查 | 编码规范 | 问题列表 |
| 安全检查 | 安全基线 | 漏洞报告 |
| 评分表 | 评分标准 | 分数+评语 |

核心不变：**标准文档 → LLM → JSON → 表单 → Excel**，只换提示词和表单模板。
