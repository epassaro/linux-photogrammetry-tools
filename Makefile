IMG_DIR = examples/kermit
RESIZE = True
MAX_SIZE = 1200
LOGFILE = log.txt
OWNER = $(USER)

all:  clean images cloud output

cloud: bundler bundle2pmvs cmvs pmvs

images:
	@echo; echo -n " Copying files..."
	@mkdir -p work_dir
	@rsync -a --ignore-missing-args $(IMG_DIR)/*.jpg work_dir
	@rsync -a --ignore-missing-args $(IMG_DIR)/*.JPG work_dir
	@cp utils/bundler.py work_dir
	@echo " OK"
ifeq ("$(RESIZE)", "True")
	@echo -n " Resizing pictures..."
	@cp utils/resizer.py work_dir
	@cd work_dir; python3 resizer.py $(MAX_SIZE)
	@echo " OK"
endif

bundler:
	@echo -n " Extracting focal distances..."
	@cd work_dir; python3 bundler.py --extract-focal
	@echo " OK"
	@echo -n " Running Bundler..."
	@cd work_dir; python3 bundler.py --verbose > $(LOGFILE) 2>&1
	@echo " OK"

bundle2pmvs:
	@echo -n " Running Bundle2PMVS..."
	@cd work_dir; ../bin/Bundle2PMVS list.txt bundle/bundle.out >> $(LOGFILE) 2>&1
	@cd work_dir; sed -i 4d pmvs/prep_pmvs.sh
	@cd work_dir; sed -i 5d pmvs/prep_pmvs.sh
	@cd work_dir; export BUNDLER_BIN_PATH="../bin"; sh pmvs/prep_pmvs.sh >> $(LOGFILE) 2>&1
	@echo " OK"
	
cmvs:
	@echo -n " Running CMVS..."
	@cd work_dir; ../bin/cmvs ./pmvs/ >> $(LOGFILE) 2>&1
	@cd work_dir; ../bin/genOption ./pmvs/ >> $(LOGFILE) 2>&1
	@echo " OK"

pmvs:
	@echo -n " Running PMVS..."
	@cd work_dir; ../bin/pmvs2 ./pmvs/ option-0000 >> $(LOGFILE) 2>&1
	@echo " OK"

output:
	@echo -n " Copying results..."
	@mkdir -p $(IMG_DIR)/output
	@cp work_dir/pmvs/models/*.ply $(IMG_DIR)/output
	@echo " OK"
	@echo -n " Setting folder ownership..."
	@chown -R $(OWNER) $(IMG_DIR)/output
	@echo " OK"
	@echo; echo "Finished."

clean:
	@rm -rf work_dir/*
