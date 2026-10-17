# Especificação inicial — Power BI

## Objetivo

Dashboard exploratório para comparar produção agrícola e emprego formal nos três municípios, após validação das fontes oficiais.

## Páginas planejadas

1. **Visão geral:** município e período; cobertura e data de atualização visíveis.
2. **Produção agrícola:** produção, área e rendimento por cultura e ano. Evitar somar produtos com unidades físicas diferentes.
3. **Emprego formal:** admissões, desligamentos e saldo mensal por setor e município, quando os microdados oficiais estiverem harmonizados.
4. **Qualidade e fontes:** cobertura, ausências, definições e registros de auditoria.

## Filtros

Município, ano/mês, cultura e setor (conforme a granularidade disponível).

## Regras de publicação

- Marcar claramente dados secundários como piloto e não os misturar sem distinção aos oficiais.
- Exibir unidade e período junto a cada indicador.
- Não mostrar conclusões causais a partir de simples correlação temporal.
- Valores monetários históricos necessitam deflator explícito.
