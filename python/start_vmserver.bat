setlocal
FOR /F "tokens=* eol=#" %%i in ('type .envTemplate') do SET %%i

waitress-serve --port=%VM_PORT% "vmserver:app"

endlocal