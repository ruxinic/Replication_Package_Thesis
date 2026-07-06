for ($i = 1; $i -le 30; $i++) {
    Write-Host "Running baseline iteration $i..."
    
    .\energibridge.exe --output "mock_results\g24_optimized_run_$i.csv" python g24_optimized.py
    
    Start-Sleep -Seconds 2
}