@echo off

:: path to java executable, by default %JAVA_HOME%\java.exe
:: change if desired, e.g. to use a different version
set "JAVA=java"
:: JVM options
set "J_OPTS=-Xmx4G"
:: command line options for the server
set "S_OPTS=--nogui"


set esc=[
set _infs=%esc%0m[
set "_infe= INFO]: " :: trailing spaces
set _errs=%esc%91m[
set "_erre= ERROR]: " :: ditto _infe
set _rst=%esc%0m

set ERRORLEVEL=0

for /f "tokens=*" %%i in ('dir /b *.jar 2^>nul') do set _jar=%%i
if [%_jar%]==[] (
	echo %_errs%%time:~0,8%%_erre%No .jar file found.%_rst%
	set ERRORLEVEL=1
	goto F
)

title %_jar%
echo %_infs%%time:~0,8%%_infe%Starting %_jar%
%JAVA% %J_OPTS% -jar %_jar% %S_OPTS%

:F
if %ERRORLEVEL% gtr 0 (
	set _exc=%esc%91m
) else (
	set _exc=%esc%0m
)
echo %_infs%%time:~0,8%%_infe%Exiting... (%_exc%%ERRORLEVEL%%_rst%)
rem exit %ERRORLEVEL%
