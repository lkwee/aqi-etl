# Activate conda
(& path\to\conda.exe shell.powershell hook) | Out-String | Invoke-Expression

# Activate your conda environment
conda activate api

# Navigate to the script directory
cd "path\to\your\directory"

# Run the Python script
python aqapi2.py
