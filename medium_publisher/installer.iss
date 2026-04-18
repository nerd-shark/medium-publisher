; Inno Setup Script for Medium Article Publisher
; This script creates a Windows installer for the application
;
; Requirements:
;   - Inno Setup 6.x (https://jrsoftware.org/isinfo.php)
;   - Built executable in dist\ directory
;
; Build command:
;   iscc installer.iss

#define MyAppName "Medium Article Publisher"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Medium Publisher"
#define MyAppURL "https://github.com/yourusername/medium-article-publisher"
#define MyAppExeName "MediumArticlePublisher.exe"

[Setup]
; Application information
AppId={{8F9A2B3C-4D5E-6F7A-8B9C-0D1E2F3A4B5C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output configuration
OutputDir=installer_output
OutputBaseFilename=MediumArticlePublisher_Setup_v{#MyAppVersion}
Compression=lzma
SolidCompression=yes

; Windows version requirements
MinVersion=10.0
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; UI configuration
WizardStyle=modern
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; License and info files
LicenseFile=LICENSE.txt
InfoBeforeFile=README.md

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Configuration files
Source: "config\default_config.yaml"; DestDir: "{app}\config"; Flags: ignoreversion
Source: "config\selectors.yaml"; DestDir: "{app}\config"; Flags: ignoreversion

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs

; Post-installation script
Source: "setup_playwright.cmd"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Setup Playwright"; Filename: "{app}\setup_playwright.cmd"; Comment: "Install Playwright browser"
Name: "{group}\Documentation"; Filename: "{app}\docs"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Offer to run setup_playwright.cmd after installation
Filename: "{app}\setup_playwright.cmd"; Description: "Install Playwright browser (required)"; Flags: postinstall shellexec skipifsilent

; Offer to launch application after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  
  // Check Windows version
  if not IsWindows10OrLater() then
  begin
    MsgBox('This application requires Windows 10 or later.', mbError, MB_OK);
    Result := False;
  end;
end;

function IsWindows10OrLater(): Boolean;
var
  Version: TWindowsVersion;
begin
  GetWindowsVersionEx(Version);
  Result := (Version.Major >= 10);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create user data directory
    CreateDir(ExpandConstant('{userappdata}\{#MyAppName}'));
  end;
end;

[UninstallDelete]
; Clean up user data on uninstall (optional - ask user)
Type: filesandordirs; Name: "{userappdata}\{#MyAppName}"
