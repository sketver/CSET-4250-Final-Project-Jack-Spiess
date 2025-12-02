# Configuration
$InstallPath = "C:\StudentGradingApp"
# Link to the github repository
$ExeUrl = "https://github.com/sketver/CSET-4250-Final-Project-Jack-Spiess/raw/refs/heads/main/Main.exe"
$ExeName = "Main.exe"
$ShortcutName = "Student Grading App.lnk"

# Create the folder on the C drive
Write-Host "Creating installation directory at $InstallPath..." -ForegroundColor Cyan
if (-not (Test-Path -Path $InstallPath)) {
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    Write-Host "Directory created successfully." -ForegroundColor Green
} else {
    Write-Host "Directory already exists." -ForegroundColor Yellow
}

# Download files
Write-Host "Downloading application files..." -ForegroundColor Cyan

try {
  
    Write-Host "Downloading Executable..."
    Invoke-WebRequest -Uri $ExeUrl -OutFile "$InstallPath\$ExeName"
    
    Write-Host "Download complete." -ForegroundColor Green
}
catch {
    Write-Error "Failed to download files. Please check your internet connection or the URL."
    Break
}

# Create Shortcut for All Users
Write-Host "Creating Desktop Shortcut for all users..." -ForegroundColor Cyan

$PublicDesktop = "$env:PUBLIC\Desktop"
$ShortcutPath = "$PublicDesktop\$ShortcutName"
$TargetExe = "$InstallPath\$ExeName"

try {
    # Create the Shell Object
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    
    # Set Shortcut Properties
    $Shortcut.TargetPath = $TargetExe
    
    # Ensure the correct icon is presented.
    $Shortcut.IconLocation = "$TargetExe,0" 
    
    $Shortcut.Description = "Launch the Student Grading Application"
    $Shortcut.WorkingDirectory = $InstallPath
    
    # Save the Shortcut
    $Shortcut.Save()
    
    Write-Host "Shortcut created successfully at $ShortcutPath" -ForegroundColor Green
}
catch {
    Write-Error "Failed to create shortcut. Ensure you are running as Administrator."
}

Write-Host "`nInstallation Complete!" -ForegroundColor Green