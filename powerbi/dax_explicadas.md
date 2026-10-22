# Medidas DAX — explicação e validação

## Contexto do projeto

As medidas foram preparadas para a tabela `Emprego`, carregada de `data/processed/caged_resumo_municipal_2025_secundario.csv`. O arquivo atual contém uma linha por município em 2025. Os valores são de fonte secundária e ainda precisam de conciliação com os microdados oficiais do Novo CAGED/MTE.

DAX significa *Data Analysis Expressions*. No Power BI, uma medida calcula um valor sob o contexto de filtro atual do visual, da página e do relatório.

## 1. Total de Admissões

```dax
Total de Admissões =
    SUM ( Emprego[admissoes] )
```

Soma a coluna de admissões nos registros incluídos pelos filtros. Com os três municípios da base atual, o resultado esperado é **77.514**.

## 2. Total de Desligamentos

```dax
Total de Desligamentos =
    SUM ( Emprego[desligamentos] )
```

Soma os desligamentos no contexto atual. Com os três municípios, o resultado esperado é **74.163**.

## 3. Saldo Calculado

```dax
Saldo Calculado =
    [Total de Admissões] - [Total de Desligamentos]
```

Calcula o saldo como admissões menos desligamentos. O resultado esperado para as três cidades em conjunto é **+3.351**. Ele descreve a diferença entre fluxos, não o estoque de empregos.

## 4. Saldo Informado

```dax
Saldo Informado =
    SUM ( Emprego[saldo] )
```

Soma a coluna de saldo encontrada na base. Foi separada da medida calculada para facilitar a auditoria aritmética.

## 5. Diferença entre Saldo Informado e Calculado

```dax
Diferença entre Saldo Informado e Calculado =
    [Saldo Informado] - [Saldo Calculado]
```

Com a base atual, espera-se zero. Isso só confirma a consistência aritmética entre colunas do mesmo CSV. **Não comprova que os dados tenham sido reconciliados com os microdados oficiais**, nem resolve divergências entre publicações diferentes.

## 6. Municípios no Recorte

```dax
Municípios no Recorte =
    DISTINCTCOUNT ( Emprego[municipio] )
```

Conta municípios distintos visíveis após a aplicação de filtros. O resultado esperado com a base inteira é **3**.

## 7. Admissões por 1.000 Habitantes

```dax
Admissões por 1.000 Habitantes =
    DIVIDE (
        [Total de Admissões],
        SUM ( Emprego[populacao_estimada] )
    ) * 1000
```

Apresenta um indicador descritivo para comparar o volume de admissões com a população estimada. Não deve ser apresentado como taxa oficial de contratação ou de emprego. Esta fórmula assume a granularidade atual, de uma linha por município em 2025. Ao acrescentar anos, a população precisa ser modelada com cuidado para não ser somada repetidamente.

## 8. Participação no Saldo Total (%)

```dax
Participação no Saldo Total (%) =
    DIVIDE (
        [Saldo Calculado],
        CALCULATE (
            [Saldo Calculado],
            ALL ( Emprego[municipio] )
        )
    )
```

Compara o saldo do município com o saldo total dos municípios, removendo o filtro de município, mas preservando outros filtros. Formate como porcentagem. Se o saldo total for zero, `DIVIDE` retorna em branco. Como o indicador usa saldo líquido, a participação pode ser negativa ou superar 100% em outros conjuntos de dados; interprete junto aos valores absolutos.

## Como conferir

1. Importe o CSV em Power BI Desktop e nomeie a tabela como `Emprego`.
2. Crie cada medida separadamente em **Modelagem → Nova medida**.
3. Coloque município, admissões, desligamentos e saldo numa tabela visual.
4. Compare o saldo calculado com a subtração manual de admissões e desligamentos para cada cidade.
5. Filtre uma cidade e depois remova o filtro; verifique que as medidas respondem ao contexto.
6. Registre versão da base, data da análise e limitações no projeto.

## O que esta validação não significa

Os números de referência ajudam a conferir se as fórmulas foram importadas e aplicadas como esperado. Não confirmam a acurácia externa da base. O projeto continua sendo exploratório até que os dados sejam conciliados com as fontes oficiais.
