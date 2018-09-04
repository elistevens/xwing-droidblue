.PHONY: all
all: droidblue/cards/raw.py

venv:
	python3.6 -m venv venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -r requirements.txt






.PHONY: yasb
yasb:
	curl -o misc/cards-common.coffee https://raw.githubusercontent.com/geordanr/xwing/master/coffeescripts/cards-common.coffee

droidblue/cards/raw.py: misc/cards-common.coffee misc/make_yasb_data.coffee
	node_modules/.bin/coffee -p $^ | node > $@

README_NAMES.md: src/xws_data_pilots.coffee src/xws_data_upgrades.coffee src/xws_validate.coffee src/make_readme_names.coffee
	node_modules/.bin/coffee -p $^ | node > $@

dist/xws.js: src/xws_data_pilots.coffee src/xws_data_upgrades.coffee src/xws_validate.coffee
	#cat a.coffee b.coffee c.coffee | coffee --compile --stdio > bundle.js
	cat $^ | node_modules/.bin/coffee -c --stdio > $@

dist/xws.min.js: dist/xws.js
	node_modules/.bin/uglifyjs $^ --screw-ie8 -o $@ -c

index.html: src/index.jade
	node_modules/.bin/jade --pretty --no-debug --out . $<
