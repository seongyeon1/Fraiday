startapp:
	chmod +x setup.sh
	./setup.sh

rerun:
	. .venv/bin/activate
	python app/main.py

ocr:
	python preprocessing/ocr.py data/snu_health4u.pdf data/snu_health4u_ocr.json
	python preprocessing/ocr.py data/생활응급처치_길라잡이.pdf data/생활응급처치_길라잡이_ocr.json

chunk:
	python preprocessing/chunking.py data/snu_health4u_ocr.json
	python preprocessing/chunking.py data/생활응급처치_길라잡이_ocr.json