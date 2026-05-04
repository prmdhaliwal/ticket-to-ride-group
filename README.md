# FIT3077 Ticket to Ride Prototype

This repository contains the Sprint 2 Python/Tkinter prototype for Ticket to Ride: London.

## Target Platform

The executable is built for Windows.

## Run the Executable

1. Open the project folder.
2. Go to:

   ```powershell
   Sprint 2\dist
   ```

3. Run:

   ```powershell
   .\TicketToRideLondon.exe
   ```

The executable should run without an IDE. The required Python/Tkinter files are packaged into the executable.

## Build the Executable

Use these steps if you need to rebuild the executable from the source code.

1. Open PowerShell in the repository root.
2. Move into the Sprint 2 folder:

   ```powershell
   cd "Sprint 2"
   ```

3. Build the executable:

   ```powershell
   python -m PyInstaller TicketToRideLondon.spec --noconfirm
   ```

4. After the build finishes, the executable will be created at:

   ```powershell
   Sprint 2\dist\TicketToRideLondon.exe
   ```

## If the Build Command Fails

Make sure Python and PyInstaller are available on the build machine:

```powershell
python --version
python -m PyInstaller --version
```

If PyInstaller is missing, install it with:

```powershell
python -m pip install pyinstaller
```

Then run the build command again from the `Sprint 2` folder.
