@echo off
echo ==============================================
echo   VocalGuard Automatic GitHub Pusher
echo ==============================================
echo.

WHERE git >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is NOT installed.
    echo Please install Git from https://git-scm.com/download/win
    echo and try again.
    pause
    exit /b
)

echo [1/3] Adding all changes...
git add .

echo [2/3] Committing changes (Semantic Intent & PWA)...
git commit -m "feat: Final Solution - Semantic Intent Engine and PWA Support"

echo [3/3] Pushing to GitHub...
git push origin main

echo.
echo [SUCCESS] Code pushed to GitHub successfully!
pause
