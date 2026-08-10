#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const visualDir = path.join(root, 'content', 'visuals');

const issues = [
  {
    output: '1968_first_catalog_siamese_booklet_index.html',
    title: '1968《全球概览》图解导读',
    eyebrow: '1968 · FALL',
    heading: '《全球概览》首刊',
    intro: '从目录的使用办法开始，依次进入整体系统、庇护所、工业、传播、共同体、游牧与学习，最后回到索引、机构和封底。九章沿着原刊顺序排成一条连续的阅读路径。',
    meta: ['9 章', '91 个条目', '原刊 n1–n67'],
    footer: '资料范围：1968《全球概览》首刊。历史价格、地址、医疗、药物、电气、化学与户外资料仅供历史阅读。',
    chapters: [
      ['00', '使用办法与目录政策', 'front-matter', '3 个条目', '1968_first_catalog_front_matter_final_booklet.html'],
      ['01', '整体系统', 'whole-systems', '8 个条目', '1968_first_catalog_whole_systems_final_booklet.html'],
      ['02', '庇护所与土地利用', 'shelter-land', '10 个条目', '1968_first_catalog_shelter_land_final_booklet.html'],
      ['03', '工业与手艺', 'industry-craft', '12 个条目', '1968_first_catalog_industry_craft_final_booklet.html'],
      ['04', '传播', 'communications', '12 个条目', '1968_first_catalog_communications_final_booklet.html'],
      ['05', '共同体', 'community', '11 个条目', '1968_first_catalog_community_final_booklet.html'],
      ['06', '游牧', 'nomadics', '13 个条目', '1968_first_catalog_nomadics_final_booklet.html'],
      ['07', '学习', 'learning', '16 个条目', '1968_first_catalog_learning_final_booklet.html'],
      ['08', '书末材料', 'back-matter', '6 个条目', '1968_first_catalog_back_matter_final_booklet.html'],
    ],
  },
  {
    output: '1974_epilog_siamese_booklet_index.html',
    title: '1974《全球概览·尾声》图解导读',
    eyebrow: '1974 · EPILOG',
    heading: '《全球概览·尾声》',
    intro: '整体系统为全书定下判断框架，土地、住所、软技术与手艺把问题放回材料和生活，随后进入共同体、游牧、通信与学习。出版业务、索引和封底收拢了这部“尾声”的生产网络。',
    meta: ['10 章', '81 个条目', '连续阅读'],
    footer: '资料范围：1974《全球概览·尾声》。历史价格、地址、医疗、药物、电气、化学、建造与户外资料仅供历史阅读。',
    chapters: [
      ['01', '整体系统', 'overall-systems', '8 个条目', '1974_epilog_overall_systems_final_booklet.html'],
      ['02', '土地使用', 'land-use', '11 个条目', '1974_epilog_land_use_final_booklet.html'],
      ['03', '住所', 'shelter', '9 个条目', '1974_epilog_shelter_final_booklet.html'],
      ['04', '软技术', 'soft-technology', '6 个条目', '1974_epilog_soft_technology_final_booklet.html'],
      ['05', '手艺', 'craft', '7 个条目', '1974_epilog_craft_final_booklet.html'],
      ['06', '共同体', 'community', '9 个条目', '1974_epilog_community_final_booklet.html'],
      ['07', '游牧', 'nomadics', '8 个条目', '1974_epilog_nomadics_final_booklet.html'],
      ['08', '通信', 'communications', '10 个条目', '1974_epilog_communications_final_booklet.html'],
      ['09', '学习', 'learning', '9 个条目', '1974_epilog_learning_final_booklet.html'],
      ['10', '出版业务、索引与封底', 'publishing-index', '4 个条目', '1974_epilog_publishing_index_final_booklet.html'],
    ],
  },
];

const css = `
    :root { --paper:#efe4cf; --sheet:#fff8e9; --ink:#211911; --muted:#6d6255; --line:#c7b796; --heavy:#3b2a1e; --blue:#245c83; --green:#546f46; }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body { margin:0; color:var(--ink); background:linear-gradient(rgba(33,25,17,.035) 1px,transparent 1px),radial-gradient(circle at 14% 8%,rgba(255,248,233,.88),transparent 26%),var(--paper); background-size:100% 22px,auto,auto; font-family:"Iowan Old Style","Songti SC","STSong","Noto Serif CJK SC",Georgia,serif; line-height:1.62; }
    a { color:inherit; }
    .skip-link { position:absolute; left:12px; top:-60px; z-index:2; padding:8px 12px; background:var(--ink); color:var(--sheet); }
    .skip-link:focus { top:12px; }
    .booklet { width:min(1360px,100%); margin:0 auto; padding:clamp(16px,3vw,38px); }
    .issue-header { display:grid; grid-template-columns:minmax(0,.78fr) minmax(0,1.22fr); gap:clamp(22px,5vw,72px); padding:clamp(30px,6vw,84px) 0 clamp(28px,5vw,68px); border-bottom:1px solid var(--line); align-items:end; }
    .eyebrow { margin:0 0 12px; color:var(--blue); font-size:13px; font-weight:700; letter-spacing:.14em; font-variant-numeric:tabular-nums; }
    .issue-header h1 { margin:0; max-width:12ch; font-size:clamp(42px,7vw,92px); line-height:1.02; font-weight:650; letter-spacing:-.025em; text-wrap:balance; }
    .issue-intro { display:grid; gap:24px; }
    .issue-intro > p { margin:0; max-width:42em; color:#392d22; font-size:clamp(18px,2vw,25px); line-height:1.72; text-wrap:pretty; }
    .issue-meta { display:flex; flex-wrap:wrap; gap:8px 18px; color:var(--muted); font-size:14px; font-variant-numeric:tabular-nums; }
    .issue-meta span + span { padding-left:18px; border-left:1px solid var(--line); }
    .issue-toc { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); border-bottom:1px solid var(--line); padding:18px 0 34px; }
    .issue-toc a { display:grid; grid-template-columns:38px 1fr auto; gap:12px; align-items:baseline; padding:15px 10px 15px 0; border-bottom:1px solid rgba(199,183,150,.58); text-decoration:none; transition:color .2s ease,transform .2s ease; }
    .issue-toc a:nth-child(odd) { margin-right:20px; }
    .issue-toc a:hover { color:var(--blue); transform:translateX(3px); }
    .issue-toc a:active { transform:translateX(3px) translateY(1px); }
    .issue-toc a:focus-visible,.toc a:focus-visible,.back-top:focus-visible { outline:2px solid var(--blue); outline-offset:3px; }
    .chapter-number { color:var(--blue); font-size:12px; font-weight:700; letter-spacing:.08em; font-variant-numeric:tabular-nums; }
    .chapter-title { font-size:clamp(18px,2vw,25px); font-weight:650; }
    .chapter-count { color:var(--muted); font-size:13px; }
    .chapter { padding-top:clamp(42px,7vw,96px); scroll-margin-top:12px; }
    .chapter-marker { display:flex; justify-content:space-between; gap:18px; align-items:baseline; padding-bottom:14px; border-bottom:1px solid var(--heavy); }
    .chapter-marker strong { font-size:14px; letter-spacing:.08em; font-variant-numeric:tabular-nums; }
    .back-top { color:var(--blue); font-size:13px; text-decoration:none; }
    .reader-guide,.phase { border-bottom:1px solid rgba(199,183,150,.72); }
    .reader-guide { display:grid; grid-template-columns:minmax(0,.72fr) minmax(0,1.28fr); gap:clamp(18px,4vw,48px); padding:clamp(22px,4vw,44px) 0; align-items:start; }
    .reader-guide h1,.phase h2 { margin:0; color:var(--ink); font-size:clamp(28px,4vw,52px); line-height:1.26; font-weight:650; letter-spacing:0; padding:0 0 .12em; text-wrap:balance; }
    .guide-copy { display:grid; gap:12px; color:#392d22; font-size:clamp(17px,1.6vw,21px); line-height:1.68; }
    .guide-copy p,.phase p,.copy p,h2 { margin:0; }
    .toc { display:flex; flex-wrap:wrap; gap:8px; padding:18px 0 10px; border-bottom:1px solid rgba(199,183,150,.66); }
    .toc a { color:var(--blue); text-decoration:none; border:1px solid rgba(36,92,131,.34); background:rgba(255,248,233,.62); padding:4px 9px; font-size:13px; transition:background .2s ease,color .2s ease; }
    .toc a:hover { background:var(--blue); color:var(--sheet); }
    .phase { display:grid; grid-template-columns:minmax(0,.46fr) minmax(0,1fr); gap:clamp(18px,4vw,44px); padding:clamp(24px,4vw,42px) 0; color:var(--muted); }
    .phase h2 { font-size:clamp(24px,3.2vw,42px); line-height:1.3; }
    .phase p { max-width:800px; font-size:clamp(16px,1.45vw,19px); line-height:1.72; }
    .phase-label { display:block; color:var(--blue); font-size:12px; font-weight:700; letter-spacing:.12em; margin-bottom:7px; }
    .spread { display:grid; grid-template-columns:minmax(0,1.42fr) minmax(320px,.58fr); gap:clamp(18px,3.5vw,42px); align-items:center; min-height:min(860px,calc(100vh - 24px)); padding:clamp(26px,5vw,66px) 0; border-bottom:1px solid rgba(199,183,150,.76); scroll-margin-top:18px; }
    .spread:nth-of-type(even) { grid-template-columns:minmax(320px,.58fr) minmax(0,1.42fr); }
    .spread:nth-of-type(even) .art { order:2; }
    .art { margin:0; padding:clamp(8px,1.2vw,14px); border:1.5px solid var(--heavy); border-radius:18px; background:var(--sheet); box-shadow:12px 12px 0 rgba(59,42,30,.09); min-width:0; }
    .art img { display:block; width:100%; height:auto; aspect-ratio:16/9; object-fit:cover; border-radius:12px; background:#f7ecd6; }
    .spread-final .art { background:#17120e; box-shadow:12px 12px 0 rgba(33,25,17,.18); }
    .copy { min-width:0; display:grid; gap:14px; align-content:center; }
    .module { color:var(--blue); font-size:13px; font-weight:700; letter-spacing:.05em; text-transform:uppercase; }
    .copy h2 { margin:0; font-size:clamp(27px,4vw,52px); line-height:1.25; font-weight:650; letter-spacing:0; padding-bottom:.08em; text-wrap:balance; }
    .copy p { margin:0; color:#392d22; font-size:clamp(16px,1.5vw,20px); line-height:1.72; }
    .anchor { padding-left:14px; border-left:3px solid var(--green); font-size:clamp(18px,2vw,23px) !important; line-height:1.58 !important; }
    .body { color:#392d22; font-size:15.5px !important; line-height:1.72; }
    .body + .body { margin-top:-4px; }
    .body strong { color:var(--ink); font-weight:700; }
    .tags { display:flex; flex-wrap:wrap; gap:8px; }
    .tags span { border:1px solid rgba(36,92,131,.42); color:var(--blue); background:rgba(255,248,233,.78); padding:3px 8px; font-size:13px; }
    .source { color:var(--muted) !important; font-size:13px !important; border-top:1px solid rgba(199,183,150,.64); padding-top:10px; }
    .issue-footer { color:var(--muted); font-size:13px; padding:28px 0 6px; border-top:1px solid var(--line); }
    @media (max-width:960px) { .issue-header,.reader-guide,.phase,.spread,.spread:nth-of-type(even) { grid-template-columns:1fr; min-height:auto; } .spread:nth-of-type(even) .art { order:0; } .art { border-radius:14px; } }
    @media (max-width:680px) { .booklet { padding:14px; } .issue-header { padding-top:34px; } .issue-header h1 { max-width:none; } .issue-toc { grid-template-columns:1fr; } .issue-toc a:nth-child(odd) { margin-right:0; } .issue-meta span + span { padding-left:0; border-left:0; } .chapter { padding-top:58px; } .chapter-count { display:none; } .art { border-radius:12px; box-shadow:6px 6px 0 rgba(59,42,30,.09); } .art img { border-radius:8px; } .body { font-size:15px !important; } }
`;

function extractChapter(filename) {
  const html = fs.readFileSync(path.join(visualDir, filename), 'utf8');
  const main = html.match(/<main\b[^>]*>([\s\S]*?)<\/main>/);
  if (!main) throw new Error(`Missing <main> in ${filename}`);

  return main[1]
    .replace(/<nav class="chapter-strip"[\s\S]*?<\/nav>\s*/i, '')
    .replace(/<div class="chapter-strip"[\s\S]*?<\/div>\s*/i, '')
    .replace(/<footer>[\s\S]*?<\/footer>\s*/i, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replaceAll('模块导航', '条目导航')
    .replaceAll('小册子目录', '条目目录')
    .replaceAll('模块', '条目')
    .trim();
}

function renderIssue(issue) {
  const toc = issue.chapters.map(([number, title, slug, count]) => `
      <a href="#chapter-${slug}">
        <span class="chapter-number">${number}</span>
        <span class="chapter-title">${title}</span>
        <span class="chapter-count">${count}</span>
      </a>`).join('');

  const chapters = issue.chapters.map(([number, title, slug, , filename]) => `
    <section class="chapter" id="chapter-${slug}" aria-labelledby="chapter-${slug}-label">
      <div class="chapter-marker">
        <strong id="chapter-${slug}-label">${number} · ${title}</strong>
        <a class="back-top" href="#top">回到全书目录</a>
      </div>
${extractChapter(filename)}
    </section>`).join('\n');

  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="${issue.title}，按原刊章节连续阅读。">
  <title>${issue.title}</title>
  <style>${css}
  </style>
</head>
<body>
  <a class="skip-link" href="#reading">跳到正文</a>
  <main class="booklet" id="reading">
    <header class="issue-header" id="top">
      <div>
        <p class="eyebrow">${issue.eyebrow}</p>
        <h1>${issue.heading}</h1>
      </div>
      <div class="issue-intro">
        <p>${issue.intro}</p>
        <div class="issue-meta">${issue.meta.map(item => `<span>${item}</span>`).join('')}</div>
      </div>
    </header>

    <nav class="issue-toc" aria-label="全书章节">${toc}
    </nav>
${chapters}

    <footer class="issue-footer">${issue.footer}</footer>
  </main>
</body>
</html>
`;
}

for (const issue of issues) {
  const output = path.join(visualDir, issue.output);
  fs.writeFileSync(output, renderIssue(issue).replace(/[ \t]+$/gm, ''));
  console.log(`built ${path.relative(root, output)}`);
}
