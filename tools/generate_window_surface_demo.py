"""Create an offline, single-file preview from the reusable modules.
Browser-test convenience only; canonical sources stay modular.
"""
from pathlib import Path
import re
base=Path(__file__).resolve().parents[1]
html=(base/'examples/window-surface/index.html').read_text()
style='\n'.join((base/x).read_text() for x in ['src/ui/window-surface.css','src/ui/chat-form-module.css'])
html=re.sub(r'<link rel="stylesheet" href="\.\./\.\./src/ui/[^\"]+">','',html)
html=html.replace('</head>','<style>'+style+'</style></head>')
def module_src(path,name):return (base/path).read_text().replace('export function '+name,'function '+name)
main=re.sub(r'^import .*?;\n','',(base/'examples/window-surface/main.js').read_text(),flags=re.M)
code=''.join('const {'+name+'}=(()=>{'+module_src(path,name)+';return {'+name+'};})();\n' for path,name in [('src/medium.js','createMedium'),('src/ui/window-surface.js','createWindowSurface'),('src/ui/chat-form-module.js','createChatFormModule')])
out=html.replace('<script type="module" src="./main.js"></script>','<script>'+code+main+'</script>')
(base/'examples/window-surface/standalone.html').write_text(out)
print('Generated:',base/'examples/window-surface/standalone.html')
