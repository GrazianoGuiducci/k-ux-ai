// Adapt only generated source copy. Visitor drafts and runtime messages are untouched.
import fs from 'node:fs';
import {parse} from 'acorn';

export function translateCopy(text, entries) {
  const replacements=[...entries].sort((a,b)=>b.it.length-a.it.length);
  const pattern=new RegExp(replacements.map(x=>x.it.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|'),'g');
  const bySource=new Map(replacements.map(x=>[x.it,x.en]));
  return text.replace(pattern,source=>bySource.get(source));
}

export function localizeDocument(html, entries) {
  const chunks=[];let offset=0;
  for(const match of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/g)) {
    chunks.push(translateCopy(html.slice(offset,match.index),entries));
    if(match[1].includes('application/json')||match[1].includes('application/ld+json')) {
      chunks.push(match[0]);offset=match.index+match[0].length;continue;
    }
    const code=match[2],edits=[];
    const ast=parse(code,{ecmaVersion:'latest',sourceType:match[1].includes('module')?'module':'script'});
    function walk(node) {
      if(!node||typeof node!=='object')return;
      if(node.type==='Literal'&&typeof node.value==='string') {
        const translated=translateCopy(node.value,entries);
        if(translated!==node.value)edits.push({start:node.start,end:node.end,text:JSON.stringify(translated)});
      } else if(node.type==='TemplateElement') {
        const translated=translateCopy(node.value.cooked,entries);
        if(translated!==node.value.cooked)edits.push({start:node.start,end:node.end,
          text:translated.replace(/\\/g,'\\\\').replace(/`/g,'\\`').replace(/\$\{/g,'\\${')});
      }
      for(const [key,value] of Object.entries(node)) {
        if(['start','end','loc','raw'].includes(key)||(key==='value'&&['Literal','TemplateElement'].includes(node.type)))continue;
        if(Array.isArray(value))value.forEach(walk);else if(value&&typeof value==='object')walk(value);
      }
    }
    walk(ast);let localized=code;
    for(const edit of edits.sort((a,b)=>b.start-a.start))localized=localized.slice(0,edit.start)+edit.text+localized.slice(edit.end);
    parse(localized,{ecmaVersion:'latest',sourceType:match[1].includes('module')?'module':'script'});
    chunks.push('<script'+match[1]+'>'+localized+'</script>');offset=match.index+match[0].length;
  }
  chunks.push(translateCopy(html.slice(offset),entries));
  return chunks.join('');
}

if(process.argv[1]&&import.meta.url===new URL('file:///'+process.argv[1].replace(/\\/g,'/')).href) {
  const catalogue=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
  const input=fs.readFileSync(0,'utf8');
  process.stdout.write(localizeDocument(input,catalogue.entries));
}
