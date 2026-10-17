$ErrorActionPreference = 'Stop'

Write-Host '1/3 - Executando testes offline...'
python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw 'Os testes falharam; revise a saída antes de continuar.' }

Write-Host '2/3 - Coletando a PAM na API do IBGE/SIDRA...'
python src/collect_pam.py
if ($LASTEXITCODE -ne 0) {
    Write-Error 'A coleta não foi concluída. Verifique a conexão com apisidra.ibge.gov.br. A análise não será executada sem a base oficial.'
    exit 1
}

Write-Host '3/3 - Gerando tabelas e gráficos analíticos...'
python src/analyze_pam.py
if ($LASTEXITCODE -ne 0) { throw 'A análise falhou; confira as validações e o arquivo processado.' }

Write-Host 'Pipeline concluído. Confira reports/outputs e reports/figures.'
