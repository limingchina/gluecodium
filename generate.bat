@echo off
if "%~1"=="" (
    %~dp0\gradlew.bat -q run
) else (
    %~dp0\gradlew.bat -q run --args="%*"
)
