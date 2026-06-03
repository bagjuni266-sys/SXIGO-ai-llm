@echo off
setlocal enabledelayedexpansion
set "SXIGO_VERSION=1.0.0"
set "SXIGO_ROOT=%~dp0"
set "SXIGO_PY=%SXIGO_ROOT%SXIGO.py"
set "SXIGO_HTML=%SXIGO_ROOT%SXIGOai.html"
set "SXIGO_DB=%USERPROFILE%\.sxigo"
set "SXIGO_LOG=%SXIGO_DB%\logs"
set "OLLAMA_HOST=http://localhost:11434"
set "SXIGO_HOST=0.0.0.0"
set "SXIGO_PORT=8765"
set "SXIGO_MODEL=llama3"
set "SXIGO_PID_FILE=%TEMP%\sxigo_server.pid"
set "SXIGO_LOG_FILE=%TEMP%\sxigo_server.log"
if not "%PYTHON_CMD%"=="" set "PYTHON=%PYTHON_CMD%"
if "%PYTHON%"=="" set "PYTHON=python"

if not exist "%SXIGO_DB%" mkdir "%SXIGO_DB%"
if not exist "%SXIGO_LOG%" mkdir "%SXIGO_LOG%"

chcp 65001 >nul 2>&1

:main_menu
cls
call :print_banner
echo.
echo.
echo.    Host: http://localhost:%SXIGO_PORT%  |  Ollama: %OLLAMA_HOST%
echo.
echo.                       [1] Start SXIGO AI Server
echo.                       [2] Stop SXIGO AI Server
echo.                       [3] Restart SXIGO AI Server
echo.                       [4] Open Web Interface
echo.                       [5] Server Status
echo.                       [6] View Server Logs
echo.                       [7] Manage Models
echo.                       [8] Database Tools
echo.                       [9] Settings
echo.                       [0] Configuration
echo.                       [S] Schedule restart
echo.                       [C] Quick console chat
echo.                       [W] Enter URL directly
echo.                       [H] Help / About
echo.                       [Q] Quit
echo.
set /p "choice=Select option: "
if /i "!choice!"=="1" goto :start_server
if /i "!choice!"=="2" goto :stop_server
if /i "!choice!"=="3" goto :restart_server
if /i "!choice!"=="4" goto :open_web
if /i "!choice!"=="5" goto :server_status
if /i "!choice!"=="6" goto :view_logs
if /i "!choice!"=="7" goto :manage_models
if /i "!choice!"=="8" goto :database_tools
if /i "!choice!"=="9" goto :settings_menu
if /i "!choice!"=="0" goto :config_menu
if /i "!choice!"=="S" goto :schedule_restart
if /i "!choice!"=="s" goto :schedule_restart
if /i "!choice!"=="C" goto :quick_chat
if /i "!choice!"=="c" goto :quick_chat
if /i "!choice!"=="H" goto :help_about
if /i "!choice!"=="h" goto :help_about
if /i "!choice!"=="Q" goto :quit
if /i "!choice!"=="q" goto :quit
if /i "!choice!"=="W" goto :open_url
if /i "!choice!"=="w" goto :open_url
echo Invalid option. Press any key to try again...
pause >nul
goto :main_menu

:print_banner
echo.
echo   ==================================================
echo       SXIGO AI v%SXIGO_VERSION% - Intelligent Assistant
echo       Host: http://localhost:%SXIGO_PORT%
echo   ==================================================
echo.
exit /b 0

:start_server
cls
call :print_header "Starting SXIGO AI Server"
echo.
call :check_ollama
if !ERRORLEVEL! neq 0 (
    call :print_error "Ollama is not running. Attempting to start..."
    call :start_ollama_service
)
call :check_python
if !ERRORLEVEL! neq 0 (
    call :print_error "Python is not installed or not in PATH"
    pause
    goto :main_menu
)
call :check_server_running
if !ERRORLEVEL! equ 0 (
    call :print_error "Server is already running (PID: !SERVER_PID!)"
    echo.
    echo Would you like to restart instead? (Y/N)
    set /p "choice="
    if /i "!choice!"=="Y" goto :restart_server
    pause
    goto :main_menu
)
echo.
echo Starting SXIGO AI Server...
echo Port: %SXIGO_PORT%
echo Model: %SXIGO_MODEL%
echo Ollama: %OLLAMA_HOST%
echo.
if not "%PYTHON_CMD%"=="" set "PYTHON=%PYTHON_CMD%"
if "%PYTHON%"=="" set "PYTHON=python"
start "SXIGO Server" cmd /c "%PYTHON% "%SXIGO_PY%" > "%SXIGO_LOG_FILE%" 2>&1"
timeout /t 3 /nobreak >nul
call :check_server_running
if !ERRORLEVEL! equ 0 (
    call :print_success "SXIGO AI Server started successfully!"
    call :print_success "      http://localhost:%SXIGO_PORT%"
    echo.
    echo Host Address: http://localhost:%SXIGO_PORT%
    echo.
    echo Press any key to open the web interface...
    pause >nul
    start "" "http://localhost:%SXIGO_PORT%"
) else (
    call :print_error "Server failed to start. Check logs for details."
    type "%SXIGO_LOG_FILE%" 2>nul
)
pause
goto :main_menu

:stop_server
cls
call :print_header "Stopping SXIGO AI Server"
echo.
call :check_server_running
if !ERRORLEVEL! neq 0 (
    call :print_error "Server is not running"
    pause
    goto :main_menu
)
echo Stopping server with PID: !SERVER_PID!
taskkill /PID !SERVER_PID! /F >nul 2>&1
del "%SXIGO_PID_FILE%" 2>nul
timeout /t 2 /nobreak >nul
call :check_server_running
if !ERRORLEVEL! neq 0 (
    call :print_success "Server stopped successfully"
) else (
    call :print_error "Failed to stop server. Try manual kill."
)
pause
goto :main_menu

:restart_server
cls
call :print_header "Restarting SXIGO AI Server"
echo.
call :stop_server_no_pause
timeout /t 2 /nobreak >nul
goto :start_server

:stop_server_no_pause
call :check_server_running
if !ERRORLEVEL! equ 0 (
    taskkill /PID !SERVER_PID! /F >nul 2>&1
    del "%SXIGO_PID_FILE%" 2>nul
    timeout /t 2 /nobreak >nul
)
exit /b 0

:open_url
cls
call :print_header "Enter URL"
echo.
echo Enter the full URL to open (e.g., http://localhost:8765):
echo.
set /p "custom_url="
if "!custom_url!"=="" goto :main_menu
start "" "!custom_url!"
call :print_success "Opened: !custom_url!"
timeout /t 2 /nobreak >nul
goto :main_menu

:open_web
cls
call :print_header "Opening Web Interface"
echo.
call :check_server_running
if !ERRORLEVEL! neq 0 (
    call :print_error "Server is not running"
    echo Start the server first (Option 1)
    pause
    goto :main_menu
)
echo Host Address: http://localhost:%SXIGO_PORT%
start "" "http://localhost:%SXIGO_PORT%"
call :print_success "Web interface opened in browser"
timeout /t 2 /nobreak >nul
goto :main_menu

:server_status
cls
call :print_header "Server Status"
echo.
call :check_server_running
set "RUNNING=!ERRORLEVEL!"
if !RUNNING! equ 0 (
    call :print_success "Server: RUNNING"
    echo PID: !SERVER_PID!
    echo Port: %SXIGO_PORT%
    echo.
    powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:%SXIGO_PORT%/api/health' -UseBasicParsing -TimeoutSec 5; $d = $r.Content | ConvertFrom-Json; Write-Host 'Status: ' -NoNewline; Write-Host $d.status -ForegroundColor Green; Write-Host 'Uptime: ' -NoNewline; Write-Host ('{0}d {1}h {2}m' -f [math]::Floor($d.uptime_seconds/86400), [math]::Floor(($d.uptime_seconds%%86400)/3600), [math]::Floor(($d.uptime_seconds%%3600)/60)) -ForegroundColor Cyan; Write-Host 'Ollama: ' -NoNewline; if ($d.ollama.connected) { Write-Host 'Connected' -ForegroundColor Green } else { Write-Host 'Disconnected' -ForegroundColor Red }; Write-Host 'Models: ' -NoNewline; Write-Host ($d.ollama.models -join ', ') -ForegroundColor Yellow } catch { Write-Host 'API Error: ' -NoNewline; Write-Host $_.Exception.Message -ForegroundColor Red }"
) else (
    call :print_error "Server: STOPPED"
    echo.
    echo The SXIGO AI Server is not running.
    echo Use Option 1 to start the server.
)
echo.
call :check_ollama
set "OLLAMA_OK=!ERRORLEVEL!"
if !OLLAMA_OK! equ 0 (
    call :print_success "Ollama: RUNNING"
    powershell -Command "try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/tags' -UseBasicParsing -TimeoutSec 3; $d = $r.Content | ConvertFrom-Json; Write-Host 'Available Models: ' -NoNewline; $d.models | ForEach-Object { Write-Host $_.name -ForegroundColor Yellow -NoNewline; Write-Host ' ' -NoNewline }; Write-Host '' } catch {}"
) else (
    call :print_error "Ollama: STOPPED"
)
echo.
echo Database: %SXIGO_DB%
echo Log file: %SXIGO_LOG_FILE%
echo Python: %SXIGO_PY%
echo HTML: %SXIGO_HTML%
pause
goto :main_menu

:view_logs
cls
call :print_header "Server Logs"
echo.
if not exist "%SXIGO_LOG_FILE%" (
    call :print_error "No log file found"
    pause
    goto :main_menu
)
echo Recent log entries (last 50 lines):
echo.
powershell -Command "Get-Content '%SXIGO_LOG_FILE%' -Tail 50 -Encoding UTF8"
echo.
echo [L] Load full log  [C] Clear log  [R] Refresh  [Any key] Back
set /p "log_choice="
if /i "!log_choice!"=="L" goto :view_full_log
if /i "!log_choice!"=="C" goto :clear_log
if /i "!log_choice!"=="R" goto :view_logs
goto :main_menu

:view_full_log
cls
call :print_header "Full Server Log"
echo.
if exist "%SXIGO_LOG_FILE%" (
    type "%SXIGO_LOG_FILE%"
) else (
    call :print_error "No log file"
)
echo.
echo Press any key to return...
pause >nul
goto :view_logs

:clear_log
if exist "%SXIGO_LOG_FILE%" (
    del "%SXIGO_LOG_FILE%"
    call :print_success "Log cleared"
) else (
    call :print_error "No log file to clear"
)
timeout /t 2 /nobreak >nul
goto :view_logs

:manage_models
cls
call :print_header "Model Management"
echo.
echo Available Models:
echo.
powershell -Command "try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/tags' -UseBasicParsing -TimeoutSec 5; $d = $r.Content | ConvertFrom-Json; $i = 1; $d.models | ForEach-Object { $size = if ($_.size -gt 1GB) { '{0:N1} GB' -f ($_.size / 1GB) } elseif ($_.size -gt 1MB) { '{0:N1} MB' -f ($_.size / 1MB) } else { '{0:N1} KB' -f ($_.size / 1KB) }; Write-Host ('  [{0}] {1,-25} {2,>8}' -f $i, $_.name, $size) -ForegroundColor Yellow; $i++ } } catch { Write-Host '  Could not connect to Ollama' -ForegroundColor Red }"
echo.
echo.
echo Commands:
echo   [P] Pull new model
echo   [D] Delete a model
echo   [R] Refresh list
echo   [Back] Return to main menu
echo.
set /p "model_choice="
if /i "!model_choice!"=="P" goto :pull_model
if /i "!model_choice!"=="D" goto :delete_model
if /i "!model_choice!"=="R" goto :manage_models
goto :main_menu

:pull_model
cls
call :print_header "Pull New Model"
echo.
echo Enter model name (e.g., llama3, llama3.1, mistral, codellama):
set /p "model_name="
if "!model_name!"=="" goto :manage_models
echo.
echo Pulling model: !model_name!
echo This may take a while depending on model size...
echo.
ollama pull !model_name!
if !ERRORLEVEL! equ 0 (
    call :print_success "Model !model_name! pulled successfully"
) else (
    call :print_error "Failed to pull model !model_name!"
)
pause
goto :manage_models

:delete_model
cls
call :print_header "Delete Model"
echo.
echo Enter model name to delete:
set /p "del_model="
if "!del_model!"=="" goto :manage_models
echo.
echo Are you sure you want to delete !del_model!? (Y/N)
set /p "confirm="
if /i "!confirm!"=="Y" (
    ollama rm !del_model!
    if !ERRORLEVEL! equ 0 (
        call :print_success "Model !del_model! deleted"
    ) else (
        call :print_error "Failed to delete model !del_model!"
    )
)
pause
goto :manage_models

:database_tools
cls
call :print_header "Database Tools"
echo.
echo   [1] View database info
echo   [2] Backup database
echo   [3] Vacuum database
echo   [4] Restore backup
echo   [5] Delete all conversations
echo   [6] Export all data
echo   [Back] Return to main menu
echo.
set /p "db_choice="
if /i "!db_choice!"=="1" goto :db_info
if /i "!db_choice!"=="2" goto :db_backup
if /i "!db_choice!"=="3" goto :db_vacuum
if /i "!db_choice!"=="4" goto :db_restore
if /i "!db_choice!"=="5" goto :db_clear
if /i "!db_choice!"=="6" goto :db_export
goto :main_menu

:db_info
cls
call :print_header "Database Information"
echo.
call :check_server_running
if !ERRORLEVEL! equ 0 (
    powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:%SXIGO_PORT%/api/database/info' -UseBasicParsing -TimeoutSec 5; $d = $r.Content | ConvertFrom-Json; Write-Host 'Path: ' -NoNewline; Write-Host $d.path -ForegroundColor Cyan; Write-Host 'Size: ' -NoNewline; Write-Host $d.size -ForegroundColor Yellow; Write-Host 'Tables: ' -NoNewline; Write-Host ($d.tables -join ', ') -ForegroundColor Green } catch { Write-Host 'API Error: ' -NoNewline; Write-Host $_.Exception.Message -ForegroundColor Red }"
) else (
    if exist "%SXIGO_DB%\sxigo_data.db" (
        for %%F in ("%SXIGO_DB%\sxigo_data.db") do (
            call :print_info "Database: %SXIGO_DB%\sxigo_data.db"
            call :print_info "Size: %%~zF bytes"
        )
    ) else (
        call :print_error "Database file not found"
    )
)
echo.
pause
goto :database_tools

:db_backup
cls
call :print_header "Backup Database"
echo.
call :check_server_running
set "WAS_RUNNING=!ERRORLEVEL!"
if !WAS_RUNNING! equ 0 (
    call :print_info "Server is running. Stopping for backup..."
    call :stop_server_no_pause
    timeout /t 2 /nobreak >nul
)
for /f %%D in ('powershell -Command "Get-Date -Format 'yyyyMMdd_HHmmss'"') do set "BACKUP_TS=%%D"
set "BACKUP_FILE=%SXIGO_DB%\backup_!BACKUP_TS!.db"
if exist "%SXIGO_DB%\sxigo_data.db" (
    copy "%SXIGO_DB%\sxigo_data.db" "!BACKUP_FILE!" >nul
    call :print_success "Backup created: !BACKUP_FILE!"
) else (
    call :print_error "No database to backup"
)
if !WAS_RUNNING! equ 0 (
    call :print_info "Restarting server..."
    goto :start_server
)
pause
goto :database_tools

:db_vacuum
cls
call :print_header "Vacuum Database"
echo.
call :check_server_running
if !ERRORLEVEL! equ 0 (
    powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:%SXIGO_PORT%/api/database/vacuum' -Method Post -UseBasicParsing -TimeoutSec 30; Write-Host 'Database vacuumed successfully' -ForegroundColor Green } catch { Write-Host 'Error: ' -NoNewline; Write-Host $_.Exception.Message -ForegroundColor Red }"
) else (
    call :print_error "Server must be running to vacuum"
)
echo.
pause
goto :database_tools

:db_restore
cls
call :print_header "Restore Database"
echo.
echo Available backups:
echo.
set "COUNT=0"
for %%F in ("%SXIGO_DB%\backup_*.db") do (
    set /a "COUNT+=1"
    echo [%COUNT%] %%~nxF (%%~zF bytes)
)
echo.
if !COUNT! equ 0 (
    call :print_error "No backups found"
    pause
    goto :database_tools
)
echo Enter the number to restore, or 0 to cancel:
set /p "restore_num="
if "!restore_num!"=="0" goto :database_tools
set "RESTORE_FILE="
set "IDX=0"
for %%F in ("%SXIGO_DB%\backup_*.db") do (
    set /a "IDX+=1"
    if !IDX! equ !restore_num! set "RESTORE_FILE=%%F"
)
if "!RESTORE_FILE!"=="" (
    call :print_error "Invalid selection"
    pause
    goto :database_tools
)
echo.
echo Restoring from: !RESTORE_FILE!
echo This will overwrite the current database. Continue? (Y/N)
set /p "confirm="
if /i "!confirm!"=="Y" (
    call :stop_server_no_pause
    copy "!RESTORE_FILE!" "%SXIGO_DB%\sxigo_data.db" /Y >nul
    call :print_success "Database restored"
) else (
    call :print_info "Restore cancelled"
)
pause
goto :database_tools

:db_clear
cls
call :print_header "Clear Database"
echo.
echo WARNING: This will delete ALL conversations and messages!
echo Are you sure? (Y/N)
set /p "confirm="
if /i "!confirm!"=="Y" (
    echo Type CONFIRM to proceed:
    set /p "double_confirm="
    if /i "!double_confirm!"=="CONFIRM" (
        call :check_server_running
        if !ERRORLEVEL! equ 0 (
            powershell -Command "try { Invoke-WebRequest -Uri 'http://localhost:%SXIGO_PORT%/api/clear' -Method Post -UseBasicParsing -TimeoutSec 10; Write-Host 'Database cleared' -ForegroundColor Green } catch { Write-Host 'Error' -ForegroundColor Red }"
        ) else (
            del "%SXIGO_DB%\sxigo_data.db" 2>nul
            call :print_success "Database deleted"
        )
    ) else (
        call :print_info "Cancelled - confirmation did not match"
    )
) else (
    call :print_info "Cancelled"
)
pause
goto :database_tools

:db_export
cls
call :print_header "Export All Data"
echo.
call :check_server_running
if !ERRORLEVEL! equ 0 (
    echo Exporting conversations...
    set "EXPORT_DIR=%SXIGO_DB%\exports"
    if not exist "!EXPORT_DIR!" mkdir "!EXPORT_DIR!"
    powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:%SXIGO_PORT%/api/conversations?limit=1000' -UseBasicParsing -TimeoutSec 10; $d = $r.Content | ConvertFrom-Json; $d.conversations | ForEach-Object { $c = $_; $mr = Invoke-WebRequest -Uri ('http://localhost:%SXIGO_PORT%/api/conversations/' + $c.id) -UseBasicParsing -TimeoutSec 10; $md = $mr.Content | ConvertFrom-Json; $md | ConvertTo-Json -Depth 10 | Out-File -FilePath ('!EXPORT_DIR!/' + $c.id.Substring(0,8) + '.json') -Encoding UTF8; Write-Host ('Exported: ' + $c.title) -ForegroundColor Yellow } } catch { Write-Host 'Error: ' -NoNewline; Write-Host $_.Exception.Message -ForegroundColor Red }"
    call :print_success "Export complete. Files saved to !EXPORT_DIR!"
) else (
    call :print_error "Server must be running"
)
pause
goto :database_tools

:settings_menu
cls
call :print_header "Settings"
echo.
echo Current Configuration:
echo ---------------------
echo Model        : %SXIGO_MODEL%
echo Port         : %SXIGO_PORT%
echo Ollama Host  : %OLLAMA_HOST%
echo Server Host  : %SXIGO_HOST%
echo Database     : %SXIGO_DB%
echo.
echo   [1] Change default model
echo   [2] Change server port
echo   [3] Change Ollama host
echo   [4] Reset to defaults
echo   [Back] Return to main menu
echo.
set /p "set_choice="
if /i "!set_choice!"=="1" goto :set_model
if /i "!set_choice!"=="2" goto :set_port
if /i "!set_choice!"=="3" goto :set_ollama
if /i "!set_choice!"=="4" goto :reset_defaults
goto :main_menu

:set_model
cls
call :print_header "Change Default Model"
echo.
echo Current model: %SXIGO_MODEL%
echo.
echo Available models:
powershell -Command "try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/tags' -UseBasicParsing -TimeoutSec 5; $d = $r.Content | ConvertFrom-Json; $d.models | ForEach-Object { Write-Host ('  - ' + $_.name) -ForegroundColor Yellow } } catch { Write-Host '  (Could not fetch model list)' }"
echo.
echo Enter model name:
set /p "SXIGO_MODEL="
if "!SXIGO_MODEL!"=="" set "SXIGO_MODEL=llama3"
call :print_success "Model set to: %SXIGO_MODEL%"
timeout /t 2 /nobreak >nul
goto :settings_menu

:set_port
cls
call :print_header "Change Server Port"
echo.
echo Current port: %SXIGO_PORT%
echo Enter new port (1024-65535):
set /p "new_port="
if "!new_port!"=="" goto :settings_menu
set "SXIGO_PORT=!new_port!"
call :print_success "Port set to: %SXIGO_PORT%"
echo Server restart required to apply.
timeout /t 2 /nobreak >nul
goto :settings_menu

:set_ollama
cls
call :print_header "Change Ollama Host"
echo.
echo Current: %OLLAMA_HOST%
echo Enter new Ollama host URL:
set /p "OLLAMA_HOST="
if "!OLLAMA_HOST!"=="" set "OLLAMA_HOST=http://localhost:11434"
call :print_success "Ollama host set to: %OLLAMA_HOST%"
timeout /t 2 /nobreak >nul
goto :settings_menu

:reset_defaults
cls
call :print_header "Reset Defaults"
echo.
echo Reset all settings to defaults? (Y/N)
set /p "confirm="
if /i "!confirm!"=="Y" (
    set "OLLAMA_HOST=http://localhost:11434"
    set "SXIGO_HOST=0.0.0.0"
    set "SXIGO_PORT=8765"
    set "SXIGO_MODEL=llama3"
    call :print_success "Settings reset to defaults"
) else (
    call :print_info "Reset cancelled"
)
timeout /t 2 /nobreak >nul
goto :settings_menu

:config_menu
cls
call :print_header "Configuration"
echo.
echo   [1] View environment variables
echo   [2] Test Ollama connection
echo   [3] Test Python dependencies
echo   [4] Run diagnostics
echo   [5] View installed Python packages
echo   [6] Check system resources
echo   [7] Network configuration
echo   [8] Performance monitor
echo   [9] Quick console chat
echo   [0] Install / update dependencies
echo   [U] Check for updates
echo   [Back] Return to main menu
echo.
set /p "cfg_choice="
if /i "!cfg_choice!"=="1" goto :view_env
if /i "!cfg_choice!"=="2" goto :test_ollama
if /i "!cfg_choice!"=="3" goto :test_deps
if /i "!cfg_choice!"=="4" goto :run_diagnostics
if /i "!cfg_choice!"=="5" goto :list_packages
if /i "!cfg_choice!"=="6" goto :system_resources
if /i "!cfg_choice!"=="7" goto :network_config
if /i "!cfg_choice!"=="8" goto :performance_monitor
if /i "!cfg_choice!"=="9" goto :quick_chat
if /i "!cfg_choice!"=="0" goto :install_deps
if /i "!cfg_choice!"=="U" goto :update_check
if /i "!cfg_choice!"=="u" goto :update_check
goto :main_menu

:view_env
cls
call :print_header "Environment Variables"
echo.
echo SXIGO Configuration:
echo --------------------
echo SXIGO_ROOT     = %SXIGO_ROOT%
echo SXIGO_PY       = %SXIGO_PY%
echo SXIGO_HTML     = %SXIGO_HTML%
echo SXIGO_DB       = %SXIGO_DB%
echo SXIGO_PID_FILE = %SXIGO_PID_FILE%
echo SXIGO_LOG_FILE = %SXIGO_LOG_FILE%
echo.
echo Runtime Configuration:
echo ---------------------
echo OLLAMA_HOST = %OLLAMA_HOST%
echo SXIGO_HOST  = %SXIGO_HOST%
echo SXIGO_PORT  = %SXIGO_PORT%
echo SXIGO_MODEL = %SXIGO_MODEL%
echo.
echo System Information:
echo ------------------
echo OS: %OS%
echo Computer: %COMPUTERNAME%
echo User: %USERNAME%
echo Processor: %PROCESSOR_ARCHITECTURE%
echo.
echo Python Path:
%PYTHON% --version 2>&1
echo.
echo File Status:
if exist "%SXIGO_PY%" (call :print_success "SXIGO.py: Found") else (call :print_error "SXIGO.py: Missing")
if exist "%SXIGO_HTML%" (call :print_success "SXIGOai.html: Found") else (call :print_error "SXIGOai.html: Missing")
if exist "%SXIGO_DB%\sxigo_data.db" (call :print_success "Database: Found") else (call :print_info "Database: Not yet created")
echo.
pause
goto :config_menu

:test_ollama
cls
call :print_header "Test Ollama Connection"
echo.
echo Testing connection to %OLLAMA_HOST% ...
echo.
powershell -Command "try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%' -UseBasicParsing -TimeoutSec 5; Write-Host 'Ollama: ' -NoNewline; Write-Host 'Connected' -ForegroundColor Green } catch { Write-Host 'Ollama: ' -NoNewline; Write-Host 'Connection failed' -ForegroundColor Red; Write-Host ('Error: ' + $_.Exception.Message) -ForegroundColor Red }"
echo.
echo Testing API endpoints...
echo.
powershell -Command "try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/tags' -UseBasicParsing -TimeoutSec 5; $d = $r.Content | ConvertFrom-Json; Write-Host 'API /api/tags: ' -NoNewline; Write-Host ('OK (' + $d.models.Count + ' models)' ) -ForegroundColor Green } catch { Write-Host 'API /api/tags: ' -NoNewline; Write-Host 'Failed' -ForegroundColor Red }"
powershell -Command "try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/version' -UseBasicParsing -TimeoutSec 5; Write-Host 'API /api/version: ' -NoNewline; Write-Host 'OK' -ForegroundColor Green } catch { Write-Host 'API /api/version: ' -NoNewline; Write-Host 'Failed' -ForegroundColor Red }"
echo.
echo Testing model inference...
echo.
if exist "%TEMP%\ollama_test.txt" del "%TEMP%\ollama_test.txt"
echo Testing model %SXIGO_MODEL%...
ollama run %SXIGO_MODEL% "Say exactly 'Hello from SXIGO' and stop." 2>nul | findstr /I "Hello" >nul
if !ERRORLEVEL! equ 0 (
    call :print_success "Model %SXIGO_MODEL%: Inference working"
) else (
    call :print_error "Model %SXIGO_MODEL%: Inference failed (might be loading)"
)
echo.
pause
goto :config_menu

:test_deps
cls
call :print_header "Test Python Dependencies"
echo.
echo Checking required Python packages...
echo.
%PYTHON% -c "import fastapi; print('fastapi: OK (' + fastapi.__version__ + ')')" 2>&1
%PYTHON% -c "import uvicorn; print('uvicorn: OK (' + uvicorn.__version__ + ')')" 2>&1
%PYTHON% -c "import httpx; print('httpx: OK (' + httpx.__version__ + ')')" 2>&1
%PYTHON% -c "import pydantic; print('pydantic: OK (' + pydantic.__version__ + ')')" 2>&1
%PYTHON% -c "import sqlite3; print('sqlite3: OK')" 2>&1
%PYTHON% -c "import asyncio; print('asyncio: OK')" 2>&1
echo.
echo Checking optional packages...
%PYTHON% -c "import sse_starlette; print('sse_starlette: OK (' + sse_starlette.__version__ + ')')" 2>&1 || echo sse_starlette: Not installed
%PYTHON% -c "import websockets; print('websockets: OK')" 2>&1 || echo websockets: Not installed
%PYTHON% -c "import aiofiles; print('aiofiles: OK')" 2>&1 || echo aiofiles: Not installed
echo.
echo Python version:
%PYTHON% --version
echo.
pause
goto :config_menu

:run_diagnostics
cls
call :print_header "System Diagnostics"
echo.
echo Running full diagnostic check...
echo.
echo [1/6] Checking Python installation...
%PYTHON% --version >nul 2>&1
if !ERRORLEVEL! equ 0 (call :print_success "Python OK") else (call :print_error "Python not found")
echo.
echo [2/6] Checking Ollama service...
powershell -Command "try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/tags' -UseBasicParsing -TimeoutSec 3; Write-Host 'Ollama: ' -NoNewline; Write-Host 'OK' -ForegroundColor Green } catch { Write-Host 'Ollama: ' -NoNewline; Write-Host 'Not running' -ForegroundColor Red }"
echo.
echo [3/6] Checking SXIGO server...
call :check_server_running
if !ERRORLEVEL! equ 0 (call :print_success "SXIGO Server: Running (PID: !SERVER_PID!)") else (call :print_warning "SXIGO Server: Not running")
echo.
echo [4/6] Checking database...
if exist "%SXIGO_DB%\sxigo_data.db" (
    for %%F in ("%SXIGO_DB%\sxigo_data.db") do (
        set "DB_SIZE=%%~zF"
    )
    call :print_success "Database: Found (!DB_SIZE! bytes)"
) else (
    call :print_warning "Database: Not found"
)
echo.
echo [5/6] Checking file integrity...
if exist "%SXIGO_PY%" (
    for %%F in ("%SXIGO_PY%") do set "PY_SIZE=%%~zF"
    call :print_success "SXIGO.py: !PY_SIZE! bytes"
) else (
    call :print_error "SXIGO.py: Missing"
)
if exist "%SXIGO_HTML%" (
    for %%F in ("%SXIGO_HTML%") do set "HTML_SIZE=%%~zF"
    call :print_success "SXIGOai.html: !HTML_SIZE! bytes"
) else (
    call :print_error "SXIGOai.html: Missing"
)
echo.
echo [6/6] Checking disk space...
powershell -Command "$drv = Get-PSDrive -Name ($env:SXIGO_DB -split ':' -split '\\')[0]; $free = [math]::Round($drv.Free/1GB, 1); $used = [math]::Round(($drv.Used)/1GB, 1); Write-Host ('Disk: ' + $drv.Name + ': ' + $used + 'GB used, ' + $free + 'GB free') -ForegroundColor Yellow"
echo.
echo Diagnostics complete.
pause
goto :config_menu

:list_packages
cls
call :print_header "Installed Python Packages"
echo.
    %PYTHON% -m pip list 2>&1
echo.
pause
goto :config_menu

:system_resources
cls
call :print_header "System Resources"
echo.
echo CPU and Memory:
echo ----------------
powershell -Command "$cpu = (Get-CimInstance Win32_Processor).LoadPercentage; $os = Get-CimInstance Win32_OperatingSystem; $totalMem = [math]::Round($os.TotalVisibleMemorySize/1MB, 1); $freeMem = [math]::Round($os.FreePhysicalMemory/1MB, 1); $usedMem = $totalMem - $freeMem; Write-Host ('CPU Usage: ' + $cpu + '%') -ForegroundColor Cyan; Write-Host ('Memory: ' + $usedMem + 'GB / ' + $totalMem + 'GB (' + $freeMem + 'GB free)') -ForegroundColor Yellow"
echo.
echo Disk Usage:
echo -----------
powershell -Command "Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{N='Size(GB)';E={[math]::Round($_.Used/1GB,1) + '/' + [math]::Round(($_.Used+$_.Free)/1GB,1)}}, @{N='Free(GB)';E={[math]::Round($_.Free/1GB,1)}} | Format-Table -AutoSize"
echo.
echo Network:
echo --------
powershell -Command "Get-NetAdapter | Where-Object {$_.Status -eq 'Up'} | Select-Object Name, Status, LinkSpeed | Format-Table -AutoSize"
echo.
echo Running Processes (SXIGO related):
echo ----------------------------------
tasklist /FI "IMAGENAME eq python.exe" 2>nul
echo.
pause
goto :config_menu

:help_about
cls
call :print_header "Help & About"
echo.
echo                     SXIGO AI v%SXIGO_VERSION%
echo                     ======================
echo.
echo DESCRIPTION:
echo   SXIGO AI is an intelligent AI assistant powered by
echo   Ollama and the llama3 language model. It provides
echo   real-time streaming responses through a beautiful
echo   web interface with Claude/Gemini/Grok-inspired design.
echo.
echo CORE FEATURES:
echo   - Real-time streaming AI responses with cursor animation
echo   - Multiple conversation management with auto-titling
echo   - Full Markdown rendering with code syntax highlighting
echo   - Adjustable AI parameters (temperature, top_p, max_tokens)
echo   - Model management (list, pull, delete, switch models)
echo   - Database backup, restore, vacuum, and export tools
echo   - Conversation export (JSON, Markdown, HTML formats)
echo   - Beautiful colorful UI with 6 themes (Default, Ocean, Sunset, Forest, Neon, Mono)
echo   - Quick console chat mode for terminal-based interaction
echo   - Server performance monitoring and benchmarking
echo   - Network configuration and diagnostics
echo   - Auto-restart scheduling
echo   - System resource monitoring
echo.
echo UI/STYLE:
echo   - Claude/Gemini/Grok inspired design
echo   - Gradient backgrounds and glassmorphism effects
echo   - Smooth animations and transitions
echo   - Responsive layout (desktop and mobile)
echo   - Copy-to-clipboard for code blocks
echo   - Typing indicators and streaming text animation
echo.
echo REQUIREMENTS:
echo   - Python 3.8+ with packages: fastapi, uvicorn, httpx, pydantic
echo   - Ollama server running (default: http://localhost:11434)
echo   - llama3 model (or any other Ollama model)
echo.
echo FILES:
echo   SXIGO.py      - Python backend server (FastAPI, 1300+ lines)
echo   SXIGOai.html  - Web frontend interface (1300+ lines)
echo   SXIGO.bat     - Management script (1000+ lines)
echo.
echo QUICK START:
echo   1. Ensure Ollama is running (ollama serve)
echo   2. Run SXIGO.bat
echo   3. Select option [1] to start server
echo   4. Select option [4] to open web interface
echo   5. Start chatting with AI!
echo.
echo PORTS:
echo   - SXIGO Server: Port %SXIGO_PORT% (configurable)
echo   - Ollama API: Port 11434 (configurable)
echo.
echo SHORTCUTS:
echo   - Main menu: Q=Quit, H=Help
echo   - Chat: Enter=Send, Shift+Enter=New line
echo   - Settings: Click gear icon
echo.
echo TROUBLESHOOTING:
echo   - If server won't start, check Python dependencies
echo   - If models won't load, check Ollama connection
echo   - If UI won't open, check firewall settings
echo   - Use diagnostics (Option 4 in Config) for full check
echo.
echo SUPPORT:
echo   Documentation and source code: https://sxigo.ai
echo   Report issues: https://github.com/sxigo/sxigo-ai/issues
echo.
echo LICENSE:
echo   MIT License - Free to use, modify, and distribute
echo.
powershell -Command "Write-Host '  [L] View full license  [Any key] Return to menu' -ForegroundColor DarkGray"
set /p "help_choice="
if /i "!help_choice!"=="L" goto :show_license
pause >nul
goto :main_menu

:quit
cls
echo.
powershell -Command "Write-Host '  Thank you for using SXIGO AI v%SXIGO_VERSION%!' -ForegroundColor Yellow"
powershell -Command "Write-Host '  Goodbye!' -ForegroundColor Cyan"
echo.
timeout /t 2 /nobreak >nul
endlocal
exit /b 0

:check_ollama
powershell -Command "try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/tags' -UseBasicParsing -TimeoutSec 3; exit 0 } catch { exit 1 }"
exit /b !ERRORLEVEL!

:check_python
if "%PYTHON%"=="" set "PYTHON=python"
%PYTHON% --version >nul 2>&1
if !ERRORLEVEL! equ 0 (
    %PYTHON% -c "import fastapi, uvicorn, httpx, pydantic" >nul 2>&1
    if !ERRORLEVEL! equ 0 exit /b 0
)
py -3 --version >nul 2>&1
if !ERRORLEVEL! equ 0 (
    set "PYTHON=py -3"
    py -3 -c "import fastapi, uvicorn, httpx, pydantic" >nul 2>&1
    if !ERRORLEVEL! equ 0 exit /b 0
)
exit /b 1

:check_server_running
set "SERVER_PID="
if exist "%SXIGO_PID_FILE%" (
    set /p "SERVER_PID="<"%SXIGO_PID_FILE%"
    tasklist /FI "PID eq !SERVER_PID!" 2>nul | findstr /I "python" >nul
    if !ERRORLEVEL! equ 0 exit /b 0
)
powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:%SXIGO_PORT%/api/health' -UseBasicParsing -TimeoutSec 2; $pid = $r.Headers['X-PID']; if ($pid) { Set-Content -Path '%SXIGO_PID_FILE%' -Value $pid }; exit 0 } catch { exit 1 }"
exit /b !ERRORLEVEL!

:start_ollama_service
echo Attempting to start Ollama service...
if exist "%PROGRAMFILES%\Ollama\ollama.exe" (
    start "" "%PROGRAMFILES%\Ollama\ollama.exe" serve
    timeout /t 5 /nobreak >nul
    call :check_ollama
    if !ERRORLEVEL! equ 0 (
        call :print_success "Ollama started successfully"
        exit /b 0
    )
)
if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" (
    start "" "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" serve
    timeout /t 5 /nobreak >nul
    call :check_ollama
    if !ERRORLEVEL! equ 0 (
        call :print_success "Ollama started successfully"
        exit /b 0
    )
)
call :print_error "Could not start Ollama automatically"
echo Please start Ollama manually and try again.
exit /b 1

:print_header
cls
echo ==============================================
echo   %~1
echo ==============================================
echo.
exit /b 0

:print_success
echo   [OK] %~1
exit /b 0

:print_error
echo   [ERROR] %~1
exit /b 0

:print_warning
echo   [WARN] %~1
exit /b 0

:print_info
echo   [INFO] %~1
exit /b 0

:install_deps
cls
call :print_header "Install Dependencies"
echo.
echo Installing required Python packages...
echo.
    %PYTHON% -m pip install --upgrade pip
    echo.
    %PYTHON% -m pip install fastapi uvicorn httpx pydantic sse-starlette websockets aiofiles
if !ERRORLEVEL! equ 0 (
    call :print_success "Dependencies installed successfully"
) else (
    call :print_error "Failed to install dependencies"
)
echo.
echo Optional: install dev tools
echo pip install black ruff pytest mypy
echo.
pause
goto :config_menu

:network_config
cls
call :print_header "Network Configuration"
echo.
echo   [1] Show network interfaces
echo   [2] Test port availability
echo   [3] Show active connections
echo   [4] Show firewall rules
echo   [Back] Return to config menu
echo.
set /p "net_choice="
if /i "!net_choice!"=="1" goto :show_interfaces
if /i "!net_choice!"=="2" goto :test_port
if /i "!net_choice!"=="3" goto :show_connections
if /i "!net_choice!"=="4" goto :show_firewall
goto :config_menu

:show_interfaces
cls
call :print_header "Network Interfaces"
echo.
powershell -Command "Get-NetIPAddress -AddressFamily IPv4 | Select-Object InterfaceAlias, IPAddress, PrefixLength | Format-Table -AutoSize"
echo.
pause
goto :network_config

:test_port
cls
call :print_header "Port Availability"
echo.
echo Enter port number to test:
set /p "test_port="
echo.
powershell -Command "try { $l = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, %test_port%); $l.Start(); Write-Host ('Port ' + %test_port% + ': Available') -ForegroundColor Green; $l.Stop() } catch { Write-Host ('Port ' + %test_port% + ': In use') -ForegroundColor Red }"
echo.
pause
goto :network_config

:show_connections
cls
call :print_header "Active Connections"
echo.
echo Active connections on port %SXIGO_PORT% and 11434:
echo.
netstat -ano | findstr ":%SXIGO_PORT% 11434" 2>nul || echo No active connections found.
echo.
pause
goto :network_config

:show_firewall
cls
call :print_header "Firewall Rules"
echo.
echo Windows Firewall rules for Python and Ollama:
echo.
powershell -Command "Get-NetFirewallRule -Direction Inbound | Where-Object { $_.DisplayName -match 'Python|Ollama|SXIGO' } | Select-Object DisplayName, Direction, Action, Enabled | Format-Table -AutoSize" 2>nul
if !ERRORLEVEL! neq 0 (
    echo No specific rules found or cannot access firewall settings.
    echo Run as Administrator to view firewall rules.
)
echo.
pause
goto :config_menu

:performance_monitor
cls
call :print_header "Performance Monitor"
echo.
echo Real-time performance data:
echo.
echo [1] CPU and Memory (single check)
echo [2] SXIGO Server response time
echo [3] Ollama performance test
echo [4] Run all benchmarks
echo [Back] Return to config menu
echo.
set /p "perf_choice="
if /i "!perf_choice!"=="1" goto :perf_simple
if /i "!perf_choice!"=="2" goto :perf_server
if /i "!perf_choice!"=="3" goto :perf_ollama
if /i "!perf_choice!"=="4" goto :perf_all
goto :config_menu

:perf_simple
cls
call :print_header "System Performance"
echo.
powershell -Command "$cpu = (Get-CimInstance Win32_Processor).LoadPercentage; $os = Get-CimInstance Win32_OperatingSystem; $totalMem = [math]::Round($os.TotalVisibleMemorySize/1MB, 1); $freeMem = [math]::Round($os.FreePhysicalMemory/1MB, 1); $usedMem = $totalMem - $freeMem; Write-Host ('CPU: ' + $cpu + '%') -ForegroundColor Cyan; Write-Host ('Memory: ' + $usedMem + 'GB / ' + $totalMem + 'GB (' + $freeMem + 'GB free)') -ForegroundColor Yellow; $pct = [math]::Round(($usedMem/$totalMem)*100, 1); Write-Host ('Memory Usage: ' + $pct + '%') -ForegroundColor Magenta"
echo.
echo Top memory processes:
powershell -Command "Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 Name, @{N='MB';E={[math]::Round($_.WorkingSet64/1MB,1)}} | Format-Table -AutoSize"
echo.
pause
goto :performance_monitor

:perf_server
cls
call :print_header "Server Performance"
echo.
call :check_server_running
if !ERRORLEVEL! equ 0 (
    echo Measuring server response time (5 requests)...
    echo.
    for /l %%i in (1,1,5) do (
        powershell -Command "$t = Measure-Command { try { Invoke-WebRequest -Uri 'http://localhost:%SXIGO_PORT%/api/health' -UseBasicParsing -TimeoutSec 5 } catch {} }; Write-Host ('Request %%i: ' + [math]::Round($t.TotalMilliseconds, 1) + 'ms') -ForegroundColor Yellow"
    )
    echo.
    powershell -Command "try { $r = Invoke-WebRequest -Uri 'http://localhost:%SXIGO_PORT%/api/metrics' -UseBasicParsing -TimeoutSec 5; $d = $r.Content | ConvertFrom-Json; Write-Host ('Total Requests: ' + $d.total_requests) -ForegroundColor Cyan; Write-Host ('Avg Response: ' + $d.average_response_time) -ForegroundColor Green; Write-Host ('Error Rate: ' + $d.error_rate) -ForegroundColor Magenta } catch {}"
) else (
    call :print_error "Server is not running"
)
echo.
pause
goto :performance_monitor

:perf_ollama
cls
call :print_header "Ollama Performance"
echo.
echo Testing Ollama response time...
echo.
for /l %%i in (1,1,3) do (
    powershell -Command "$t = Measure-Command { try { Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/tags' -UseBasicParsing -TimeoutSec 5 } catch {} }; Write-Host ('API Request %%i: ' + [math]::Round($t.TotalMilliseconds, 1) + 'ms') -ForegroundColor Yellow"
)
echo.
echo Testing model inference speed...
echo.
echo Sending test prompt to %SXIGO_MODEL%...
echo.
powershell -Command "$t = Measure-Command { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/generate' -Method Post -Body '{\"model\":\"%SXIGO_MODEL%\",\"prompt\":\"Say hello in one word\",\"stream\":false}' -ContentType 'application/json' -UseBasicParsing -TimeoutSec 30 }; $d = $r.Content | ConvertFrom-Json; Write-Host ('Response: ' + $d.response) -ForegroundColor Green; Write-Host ('Total duration: ' + [math]::Round($t.TotalMilliseconds, 0) + 'ms') -ForegroundColor Cyan"
echo.
pause
goto :performance_monitor

:perf_all
cls
call :print_header "Full Benchmark Suite"
echo.
echo Running all benchmarks...
echo.
echo ===== System Resources =====
powershell -Command "$cpu = (Get-CimInstance Win32_Processor).LoadPercentage; $os = Get-CimInstance Win32_OperatingSystem; $totalMem = [math]::Round($os.TotalVisibleMemorySize/1MB, 1); $freeMem = [math]::Round($os.FreePhysicalMemory/1MB, 1); Write-Host ('CPU: ' + $cpu + '% | Memory: ' + [math]::Round(($totalMem-$freeMem),1) + '/' + $totalMem + 'GB (' + $freeMem + 'GB free)') -ForegroundColor Yellow"
echo.
echo ===== Server Response =====
call :check_server_running
if !ERRORLEVEL! equ 0 (
    powershell -Command "$t = Measure-Command { try { Invoke-WebRequest -Uri 'http://localhost:%SXIGO_PORT%/api/health' -UseBasicParsing -TimeoutSec 5 } catch {} }; Write-Host ('SXIGO Server: ' + [math]::Round($t.TotalMilliseconds, 1) + 'ms') -ForegroundColor Green"
) else (
    Write-Host 'SXIGO Server: Not running' -ForegroundColor Red
)
echo.
echo ===== Ollama API =====
powershell -Command "$t = Measure-Command { try { Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/tags' -UseBasicParsing -TimeoutSec 5 } catch {} }; Write-Host ('Ollama API: ' + [math]::Round($t.TotalMilliseconds, 1) + 'ms') -ForegroundColor Green"
echo.
echo ===== Model Inference =====
powershell -Command "$t = Measure-Command { try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/generate' -Method Post -Body '{\"model\":\"%SXIGO_MODEL%\",\"prompt\":\"Say hello\",\"stream\":false}' -ContentType 'application/json' -UseBasicParsing -TimeoutSec 30 } catch {} }; Write-Host ('Model Inference: ' + [math]::Round($t.TotalMilliseconds, 0) + 'ms') -ForegroundColor Magenta"
echo.
echo ===== Disk Speed =====
powershell -Command "$t = Measure-Command { $null = Get-ChildItem '%SXIGO_DB%' -Recurse -ErrorAction SilentlyContinue }; Write-Host ('DB Read Test: ' + [math]::Round($t.TotalMilliseconds, 1) + 'ms') -ForegroundColor Yellow"
echo.
echo Benchmark complete.
pause
goto :config_menu

:update_check
cls
call :print_header "Update Check"
echo.
echo Checking for updates...
echo.
echo Current version: %SXIGO_VERSION%
echo.
echo SXIGO AI v%SXIGO_VERSION%
echo -------------------------
echo.
echo File checksums:
echo.
powershell -Command "if (Test-Path '%SXIGO_PY%') { $hash = Get-FileHash '%SXIGO_PY%' -Algorithm SHA256; Write-Host ('SXIGO.py: ' + $hash.Hash.Substring(0, 16) + '...') -ForegroundColor Gray }"
powershell -Command "if (Test-Path '%SXIGO_HTML%') { $hash = Get-FileHash '%SXIGO_HTML%' -Algorithm SHA256; Write-Host ('SXIGOai.html: ' + $hash.Hash.Substring(0, 16) + '...') -ForegroundColor Gray }"
powershell -Command "if (Test-Path '%~f0') { $hash = Get-FileHash '%~f0' -Algorithm SHA256; Write-Host ('SXIGO.bat: ' + $hash.Hash.Substring(0, 16) + '...') -ForegroundColor Gray }"
echo.
echo To update, visit: https://sxigo.ai/downloads
echo.
pause
goto :config_menu

:quick_chat
cls
call :print_header "Quick Console Chat"
echo.
echo One-shot chat with %SXIGO_MODEL%
echo Type your message (or /back to return):
echo.
set /p "quick_prompt="
if "!quick_prompt!"=="" goto :quick_chat
if /i "!quick_prompt!"=="/back" goto :main_menu
echo.
echo SXIGO AI: Thinking...
echo.
powershell -Command "$body = @{model='%SXIGO_MODEL%'; prompt='!quick_prompt!'; stream=$false; options=@{temperature=0.7}} | ConvertTo-Json; try { $r = Invoke-WebRequest -Uri '%OLLAMA_HOST%/api/generate' -Method Post -Body $body -ContentType 'application/json' -UseBasicParsing -TimeoutSec 60; $d = $r.Content | ConvertFrom-Json; Write-Host ''; Write-Host $d.response -ForegroundColor Cyan; Write-Host '' } catch { Write-Host ('Error: ' + $_.Exception.Message) -ForegroundColor Red }"
echo.
echo [Enter] Ask again  [Back] Return to menu
set /p "after_chat="
if /i "!after_chat!"=="/back" goto :main_menu
goto :quick_chat

:schedule_restart
cls
call :print_header "Schedule Restart"
echo.
echo Schedule automatic server restart?
echo.
echo [1] Restart in 1 hour
echo [2] Restart in 6 hours
echo [3] Restart in 24 hours
echo [4] Cancel scheduled restart
echo [Back] Return
echo.
set /p "sched_choice="
if /i "!sched_choice!"=="1" set "SCHED_HOURS=1"
if /i "!sched_choice!"=="2" set "SCHED_HOURS=6"
if /i "!sched_choice!"=="3" set "SCHED_HOURS=24"
if /i "!sched_choice!"=="4" (
    schtasks /Delete /TN "SXIGO_Restart" /F >nul 2>&1
    call :print_info "Scheduled restart cancelled"
    pause
    goto :main_menu
)
if not defined SCHED_HOURS (
    if /i NOT "!sched_choice!"=="4" (
        pause
        goto :main_menu
    )
)
for /f %%A in ('powershell -Command "(Get-Date).AddHours(!SCHED_HOURS!).ToString('HH:mm')"') do set "SCHED_TIME=%%A"
for /f %%B in ('powershell -Command "(Get-Date).AddHours(!SCHED_HOURS!).ToString('MM/dd/yyyy')"') do set "SCHED_DATE=%%B"
schtasks /Create /SC ONCE /TN "SXIGO_Restart" /TR "cmd /c \"%~f0\"" /ST !SCHED_TIME! /SD !SCHED_DATE! /F >nul 2>&1
if !ERRORLEVEL! equ 0 (
    call :print_success "Restart scheduled in !SCHED_HOURS! hour(s) at !SCHED_TIME! on !SCHED_DATE!"
) else (
    call :print_error "Failed to schedule restart"
)
pause
goto :main_menu

:show_license
cls
call :print_header "License"
echo.
echo SXIGO AI v%SXIGO_VERSION%
echo ========================
echo.
echo MIT License
echo.
echo Copyright (c) 2026 SXIGO
echo.
echo Permission is hereby granted, free of charge, to any person obtaining a copy
echo of this software and associated documentation files (the "Software"), to deal
echo in the Software without restriction, including without limitation the rights
echo to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
echo copies of the Software, and to permit persons to whom the Software is
echo furnished to do so, subject to the following conditions:
echo.
echo The above copyright notice and this permission notice shall be included in all
echo copies or substantial portions of the Software.
echo.
echo THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
echo IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
echo FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
echo AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
echo LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
echo OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
echo SOFTWARE.
echo.
pause
goto :help_about
