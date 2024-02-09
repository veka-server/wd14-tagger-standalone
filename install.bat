@echo off
Title WD14 - install

:: telecharger/update les sources depuis github
if exist wd14-tagger-standalone\ (
	cd wd14-tagger-standalone\
	git pull
) else (
	git clone https://github.com/veka-server/wd14-tagger-standalone.git
	cd wd14-tagger-standalone\
)

:: creer environement virtuel
python.exe -m venv venv

:: mettre a jour pip
venv\Scripts\python.exe -m pip install --upgrade pip

:: installer torch avec support cuda 12
 venv\Scripts\pip.exe install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
:: venv\Scripts\pip.exe install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

:: install onnxruntime avec support cuda
venv\Scripts\pip.exe install onnxruntime-gpu --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/

:: installer les dependances
venv\Scripts\pip.exe install -r requirements.txt

:: afficher version de torch
:: venv\Scripts\python.exe  -c "import torch; print(torch.__version__)"

:: check si torch cuda est bien reconnu en affichant le nombre de GPU
:: venv\Scripts\python.exe  -c "import torch;  num_of_gpus = torch.cuda.device_count(); print(num_of_gpus);"

