# Mercado de trabalho formal regional — piloto 2025

**Status:** análise descritiva preliminar baseada em páginas secundárias que atribuem a fonte ao Novo CAGED/MTE. Não equivale à extração e reconciliação dos microdados oficiais.

## Resumo municipal

| Município | Admissões | Desligamentos | Saldo reportado | Salário médio de admissão | Saldo por mil habitantes* |
|---|---:|---:|---:|---:|---:|
| Lucas do Rio Verde | 27.976 | 26.173 | +1.803 | R$ 2.372,62 | 18,8 |
| Sorriso | 31.519 | 30.648 | +871 | R$ 2.400,79 | 7,0 |
| Nova Mutum | 18.019 | 17.342 | +677 | R$ 2.308,16 | 10,7 |

*O saldo por mil habitantes usa a população estimada apresentada pelo painel. Não representa probabilidade individual de contratação e depende do denominador escolhido.

## Comparação setorial

- **Lucas do Rio Verde:** Construção Civil +853; Serviços +595; Indústria +206; Comércio +122; Agropecuária +34; Administração Pública -7.
- **Sorriso:** Serviços +514; Indústria +312; Agropecuária +246; Administração Pública +6; Comércio -39; Construção Civil -168.
- **Nova Mutum:** Serviços +429; Construção Civil +114; Agropecuária +84; Comércio +64; Indústria -14.

## Auditoria de fonte — Lucas do Rio Verde

Há divergência no saldo de emprego de 2025: a página secundária da Coalize informa +1.803, enquanto notícia da Prefeitura de Lucas do Rio Verde, citando Novo CAGED, informa +1.767. A diferença é 36 empregos. A causa não foi estabelecida. Os números não foram conciliados; ver `data/processed/auditoria_fontes_saldo_lucas_2025.csv`.

## Limites de inferência

O piloto é descritivo, transversal e usa fonte secundária. Não permite concluir que produção agrícola causou mudança no emprego. Para estudar coincidência temporal, precisamos obter dados mensais harmonizados do Novo CAGED, validar o layout dos microdados oficiais e relacioná-los depois à PAM anual. O saldo de movimentações não é estoque total de emprego nem desemprego.

## Fontes

- [Coalize / Lucas do Rio Verde / 2025](https://dados.coalize.com.br/mapa-do-emprego/cidade/mt/lucas-do-rio-verde/2025)
- [Coalize / Sorriso / 2025](https://dados.coalize.com.br/mapa-do-emprego/cidade/mt/sorriso/2025)
- [Coalize / Nova Mutum / 2025](https://dados.coalize.com.br/mapa-do-emprego/cidade/mt/nova-mutum/2025)
- [Prefeitura de Lucas do Rio Verde — saldo de 2025](https://lucasdorioverde.mt.gov.br/site/secretaria-noticias?cod=14574&text=desenvolvimento-economico-planejamento-e-cidade)
- [MTE — microdados RAIS e CAGED](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/estatisticas-trabalho/microdados-rais-e-caged)
