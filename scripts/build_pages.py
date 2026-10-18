"""Reproducible static publication containing the existing Python source."""
from pathlib import Path
import json
import shutil
root=Path(__file__).resolve().parents[1]
out=root/'dist'
if out.exists():shutil.rmtree(out)
shutil.copytree(root/'web',out)
(out/'py').mkdir(exist_ok=True)
for name in ('engine.py','systems.py','resources.py'):shutil.copy2(root/name,out/'py'/name)
(out/'runtime-config.json').write_text(json.dumps({'mode':'browser-python'}))
(out/'.nojekyll').touch()
print('Static Pages build:',out)
