# 兼容性 shim：确保 bibtexparser.bibdatabase 可被导入（用于兼容不同版本的 bibtexparser）
import sys
import types

try:
    # 如果包路径存在，这里什么都不做
    import bibtexparser.bibdatabase  # type: ignore
except ModuleNotFoundError:
    # bibtexparser >=2 可能把类放在 bibtexparser.database
    try:
        from bibtexparser.database import BibDatabase  # type: ignore
    except Exception:
        BibDatabase = None

    mod = types.ModuleType("bibtexparser.bibdatabase")
    if BibDatabase is not None:
        mod.BibDatabase = BibDatabase
    # 将虚拟模块放入 sys.modules，使 `from bibtexparser.bibdatabase import BibDatabase` 能工作
    sys.modules["bibtexparser.bibdatabase"] = mod

# 现在安全导入 scholarly

from scholarly import scholarly
import jsonpickle
import json
from datetime import datetime
import os

author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
name = author['name']
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']:v for v in author['publications']}
print(json.dumps(author, indent=2))
os.makedirs('results', exist_ok=True)
with open(f'results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author['citedby']}",
}

with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)
