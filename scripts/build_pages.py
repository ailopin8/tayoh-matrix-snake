"""Reproducible static publication containing the existing Python source."""
from pathlib import Path
import hashlib
import json
import re
import shutil
root=Path(__file__).resolve().parents[1]
out=root/'dist'
if out.exists():shutil.rmtree(out)
shutil.copytree(root/'web',out)
(out/'py').mkdir(exist_ok=True)
for name in ('engine.py','systems.py','resources.py'):shutil.copy2(root/name,out/'py'/name)
(out/'runtime-config.json').write_text(json.dumps({'mode':'browser-python'}))
# One content fingerprint binds HTML, modules, config and Python files to a build.
h=hashlib.sha256()
for file in sorted(out.rglob('*')):
    if file.is_file():h.update(str(file.relative_to(out)).encode());h.update(file.read_bytes())
revision=h.hexdigest()[:16]
for file in [*out.glob('*.js'),*out.glob('*.mjs')]:
    code=file.read_text()
    code=re.sub(r"(['\"])(\./[^'\"]+\.(?:js|mjs|json))\1",lambda m:m[1]+m[2]+'?v='+revision+m[1],code)
    file.write_text(code)
html=(out/'index.html').read_text().replace('href="style.css"',f'href="style.css?v={revision}"').replace('src="app.js"',f'src="app.js?v={revision}"')
(out/'index.html').write_text(html)
(out/'.nojekyll').touch()
print('Static Pages build:',out,'revision',revision)
