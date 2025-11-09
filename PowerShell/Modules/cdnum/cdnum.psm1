# ---------------------------------------------------------------------------
# Module: cdnum
# Author: Richard Moreton
# Description:
#   Provides a PowerShell function for quickly navigating upward
#   through directory hierarchies using a numeric argument.
#
# Example Usage:
#   cdnum 2      -> moves up two directories
#   cdnum        -> displays current directory info and examples
#   ..n 3        -> moves up three directories (alias)
# ---------------------------------------------------------------------------

function cdnum {
    param([int]$num)

    # If no argument is provided, show information about the current directory.
    if (-not $num) {
        $currentPath = (Get-Location).Path
        $segments = $currentPath -split '[\\/]' | Where-Object { $_ -ne '' }
        $depth = $segments.Count

        Write-Host "Current directory:" -ForegroundColor Cyan
        Write-Host "   $currentPath" -ForegroundColor White
        Write-Host ""
        Write-Host "Directory depth: $depth" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Usage examples:" -ForegroundColor Green
        Write-Host "   cdnum 1  -> move up 1 directory"
        Write-Host "   cdnum 2  -> move up 2 directories"
        Write-Host "   cdnum 3  -> move up 3 directories"
        return
    }

    # Validate that the argument is a positive integer.
    if ($num -lt 1) {
        Write-Host "Please provide a positive number greater than zero." -ForegroundColor Yellow
        return
    }

    # Construct the relative path string (e.g., ../../..)
    $relativePath = ('../' * $num)

    try {
        # Compute and resolve the full target path.
        $targetPath = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $relativePath))
        Set-Location $targetPath

        Write-Host "Changed directory to:" -ForegroundColor Green
        Write-Host "   $targetPath" -ForegroundColor White
    }
    catch {
        Write-Host "Error: Unable to move up $num directories from the current location." -ForegroundColor Red
    }
}

# Create an alias for quick use, allowing '..n 3' as shorthand for 'cdnum 3'.
Set-Alias ..n cdnum

# Register tab-completion for numbers 1–10.
Register-ArgumentCompleter -CommandName cdnum -ParameterName num -ScriptBlock {
    param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)

    1..10 | ForEach-Object {
        [System.Management.Automation.CompletionResult]::new(
            $_.ToString(),
            $_.ToString(),
            'ParameterValue',
            "Move up $_ director" + ($(if ($_ -eq 1) { 'y' } else { 'ies' }))
        )
    }
}

# Export the function and alias so they become available when the module is imported.
Export-ModuleMember -Function cdnum -Alias ..n
