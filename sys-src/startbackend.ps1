#create a script that starts the venv and runs the backend
$backendPath = "C:\GIT_Workspaces\opcua_netzwerk\backend"
$venvPath = "C:\GIT_Workspaces\opcua_netzwerk\venv\Scripts\activate.ps1"
$backendScript = "python -m backend"

#start the virtual environment
& $venvPath

#navigate to the backend path
cd $backendPath

#start the backend
& $backendScript