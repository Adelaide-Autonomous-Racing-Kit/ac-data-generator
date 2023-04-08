.ONESHELL:
SHELL = /bin/zsh
CONDA_ENV_PATH=./envs
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate ; conda activate

build: setup-conda setup-pre-push
	@echo "Finished building environment"

setup-conda:
ifneq ($(wildcard $(CONDA_ENV_PATH)),)
	@echo "Environment $(CONDA_ENV_PATH) already exists, do you want to delete it and create a new one? [y/n]"
	@read ans; \
	if [ $$ans = 'y' ]; then \
		conda env remove -p $(CONDA_ENV_PATH); \
	fi
endif
	# Create conda environment and install packages
	conda create -y -p $(CONDA_ENV_PATH) -c conda-forge opencv numpy pyyaml pillow python=3.9 \
		black flake8-black flake8 isort loguru pytest pytest-parallel py pytest-benchmark coverage \
		pyautogui loguru yaml tqdm halo embree==2.17.7 pyembree pre_commit prettytable
	
	$(CONDA_ACTIVATE) $(CONDA_ENV_PATH)
	# Install packages using pip
	pip3 install trimesh\[all\]
	pip3 install -e .


setup-pre-push:
	@echo "Setting up pre-push hook..."
	@cp pre_push.sh .git/hooks/pre-push
	@chmod +x .git/hooks/pre-push
	@echo "Done!"

run:
	@echo $(CONDA_ENV_PATH)
	@source activate $(CONDA_ENV_PATH)

test:
	@echo "Starting all non gpu related tests"
	@pytest --workers 4 src/ -m "not benchmark and not gpu" 

lint:
	@black "src/" 
	@isort --settings-file=linters/isort.ini "src/"
	@flake8 --config=linters/flake8.ini "src/"
	@echo "all done"
