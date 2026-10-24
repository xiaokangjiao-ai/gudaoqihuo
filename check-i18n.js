// 落地页语法自检：抽出所有 <script> 块做语法解析，并核对四语 i18n key 是否齐全
const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync(__dirname + '/index.html', 'utf8');
const blocks = [...html.matchAll(/<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]);
console.log('script blocks:', blocks.length);

let ok = true;
blocks.forEach((code, i) => {
  try {
    new vm.Script(code, { filename: `block${i}.js` });
    console.log(`block ${i}: OK (${code.length} chars)`);
  } catch (e) {
    ok = false;
    console.log(`block ${i}: SYNTAX ERROR -> ${e.message}`);
  }
});

// 四语 i18n key 对齐检查
const m = html.match(/const\s+I18N\s*=\s*\{([\s\S]*?)\n\s*\};/);
if (!m) {
  console.log('I18N object not found (跳过 key 对齐检查)');
} else {
  const sandbox = {};
  vm.createContext(sandbox);
  const i18n = vm.runInContext('({' + m[1] + '})', sandbox);
  const langs = Object.keys(i18n);
  console.log('langs:', langs.join(','));
  const base = Object.keys(i18n.zh);
  for (const lang of langs) {
    const keys = Object.keys(i18n[lang]);
    const missing = base.filter((k) => !keys.includes(k));
    const extra = keys.filter((k) => !base.includes(k));
    console.log(`${lang}: keys=${keys.length} missing=${missing.length}${missing.length ? ' -> ' + missing.join(',') : ''}${extra.length ? ' extra -> ' + extra.join(',') : ''}`);
    if (missing.length) ok = false;
  }
  // 反向检查：HTML 里用到的 data-i18n 是否都有定义（以 zh 为基准）
  const used = [...new Set([...html.matchAll(/data-i18n="([^"]+)"/g)].map((x) => x[1]))];
  const undef = used.filter((k) => !(k in i18n.zh));
  console.log(`data-i18n used=${used.length} undefined_in_zh=${undef.length}${undef.length ? ' -> ' + undef.join(',') : ''}`);
}

console.log(ok ? 'RESULT: PASS' : 'RESULT: FAIL');
