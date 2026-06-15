# ExcelJS 前端导出模板

## 适用场景
纯前端生成带格式的 Excel 文件并下载，无需后端参与。适合台账、报表、统计汇总等场景。

## 依赖

```html
<script src="https://cdn.jsdelivr.net/npm/exceljs@4.4.0/dist/exceljs.min.js"></script>
```

## 完整模板

```javascript
async function exportExcel(allRows, filename) {
  const ExcelJS = window.ExcelJS;
  const wb = new ExcelJS.Workbook();

  // ====== Sheet 1: 明细 ======
  const ws = wb.addWorksheet('明细表');

  // 颜色定义
  const C = {
    primary: '1A5276',    // 深色标题背景
    mid: '2E7D32',        // 表头背景
    light: 'C8E6C9',      // 浅色
    bg: 'E8F5E9',         // 交替行背景
    white: 'FFFFFF',
    black: '1A1A1A',
    gray: '757575',
    red: 'C62828',
  };

  const cols = ['日期','部门','项目','描述','责任人'];  // 你的列
  const colWidths = [12, 8, 30, 40, 10];               // 列宽

  // 设置列宽
  cols.forEach((_, i) => ws.getColumn(i + 1).width = colWidths[i]);

  let row = 1;

  // --- 标题行（深色背景 + 白色粗体）---
  ws.mergeCells(row, 1, row, cols.length);
  const title = ws.getCell(row, 1);
  title.value = 'XXX 台账';   // 标题文字
  title.font = { bold: true, size: 16, color: { argb: C.white } };
  title.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: C.primary } };
  title.alignment = { horizontal: 'center', vertical: 'middle' };
  ws.getRow(row).height = 36; row++;

  // --- 副标题（浅色背景）---
  ws.mergeCells(row, 1, row, cols.length);
  const sub = ws.getCell(row, 1);
  const now = new Date();
  sub.value = `导出时间：${now.toLocaleDateString()}  |  共 ${allRows.length} 条`;
  sub.font = { size: 9, color: { argb: C.gray } };
  sub.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: C.light } };
  sub.alignment = { horizontal: 'center' };
  ws.getRow(row).height = 22; row++;
  ws.getRow(row).height = 8; row++;  // 空行

  // --- 表头（中色背景 + 白色粗体）---
  cols.forEach((col, i) => {
    const cell = ws.getCell(row, i + 1);
    cell.value = col;
    cell.font = { bold: true, size: 10, color: { argb: C.white } };
    cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: C.mid } };
    cell.alignment = { horizontal: 'center', vertical: 'middle', wrapText: true };
    cell.border = {
      top: { style: 'thin' }, bottom: { style: 'thin' },
      left: { style: 'thin' }, right: { style: 'thin' }
    };
  });
  ws.getRow(row).height = 22; row++;

  // --- 数据行（交替背景）---
  allRows.forEach((r, idx) => {
    cols.forEach((col, i) => {
      const cell = ws.getCell(row, i + 1);
      cell.value = r[col] || '';
      cell.font = { size: 10 };
      cell.alignment = { vertical: 'middle', wrapText: true };
      // 条件着色：严重项标红
      if (r.severity === 'high') {
        cell.font = { size: 10, color: { argb: C.red }, bold: true };
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF5F5' } };
      } else if (idx % 2 === 1) {
        cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: C.bg } };
      }
    });
    // 行高自适应内容长度
    ws.getRow(row).height = Math.max(20, Math.ceil((r['描述'] || '').length / 50) * 16);
    row++;
  });

  // --- 底部汇总 ---
  ws.getRow(row).height = 8; row++;
  ['涉及部门：XX', `总数：${allRows.length} 条`, `严重项：${allRows.filter(r=>r.severity==='high').length} 条`]
    .forEach(txt => {
      ws.getCell(row, 2).value = txt;
      ws.getCell(row, 2).font = { size: 10, bold: true, color: { argb: C.primary } };
      ws.mergeCells(row, 2, row, 5);
      row++;
    });

  // ====== Sheet 2: 汇总统计 ======
  const ws2 = wb.addWorksheet('汇总统计');
  ws2.getColumn(1).width = 25;
  ws2.getColumn(2).width = 15;
  let r2 = 1;

  // 标题
  ws2.mergeCells(r2, 1, r2, 2);
  const s2t = ws2.getCell(r2, 1);
  s2t.value = '汇总统计';
  s2t.font = { bold: true, size: 14, color: { argb: C.white } };
  s2t.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: C.primary } };
  s2t.alignment = { horizontal: 'center' };
  ws2.getRow(r2).height = 28; r2 += 2;

  // 按维度统计
  const dimCount = {};
  allRows.forEach(r => { dimCount[r.dimension] = (dimCount[r.dimension]||0) + 1; });
  Object.entries(dimCount).forEach(([k, v]) => {
    ws2.getCell(r2, 1).value = k; ws2.getCell(r2, 2).value = v + ' 条';
    r2++;
  });

  // 按责任人统计
  r2++;
  const personCount = {};
  allRows.forEach(r => { if(r.person) personCount[r.person] = (personCount[r.person]||0) + 1; });
  Object.entries(personCount).forEach(([k, v]) => {
    ws2.getCell(r2, 1).value = k; ws2.getCell(r2, 2).value = v + ' 条';
    r2++;
  });

  // --- 下载 ---
  const buf = await wb.xlsx.writeBuffer();
  const blob = new Blob([buf], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename || `export_${now.toISOString().slice(0,10)}.xlsx`;
  a.click();
  URL.revokeObjectURL(url);
}
```

## 快速定制清单

1. 改 `cols` 和 `colWidths` 定义你的列
2. 改 `C` 颜色对象适配你的品牌色
3. 改条件着色逻辑（如 `r.severity === 'high'`）
4. 改 Sheet 2 的统计维度
5. 改 `filename` 的命名规则
