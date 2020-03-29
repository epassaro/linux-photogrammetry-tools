IMG_DIR = examples/kermit
OUTPUT = work_dir
CLUSTER = 10

all:  clean images mesh

mesh: bundler bundle2pmvs cmvs pmvs

images:	
	@echo; echo -n " Copying files..."
	@mkdir -p work_dir
	@cp $(IMG_DIR)/*.jpg work_dir
	@cp utils/bundler.py work_dir
	@echo " OK"

bundler:
	@echo -n " Extracting focal distances..."
	@cd work_dir; python bundler.py --extract-focal
	@echo " OK"
	@echo -n " Running Bundler..."
	@cd work_dir; python bundler.py
	@echo " OK"

bundle2pmvs:
	@echo -n " Running Bundle2PMVS..."
	@cd work_dir; ../bin/Bundle2PMVS list.txt bundle/bundle.out > /dev/null 2>&1
	@cp work_dir/pmvs/* work_dir/
	@sed -i 4d work_dir/prep_pmvs.sh
	@export BUNDLER_BIN_PATH="../bin"; cd work_dir; sh prep_pmvs.sh > /dev/null 2>&1
	@echo " OK"
	
cmvs:
	@echo -n " Running CMVS..."
	@cd bin; ./cmvs ../work_dir/pmvs/ > /dev/null 2>&1
	@cd bin; ./genOption ../work_dir/pmvs/
	@echo " OK"

pmvs:
	@echo -n " Running PMVS..."
	@cd bin; ./pmvs2 ../work_dir/pmvs/ option-0000 > /dev/null 2>&1
	@echo " OK"
	@echo; echo "Finished."

clean:
	@rm -rf work_dir/*
