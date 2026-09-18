# Simulador de Filtros Digitais em Python

Projeto didático desenvolvido para demonstrar, de forma visual, o funcionamento de filtros digitais aplicados ao condicionamento de sinais.

A aplicação permite gerar um sinal senoidal, adicionar uma interferência de frequência diferente e observar o comportamento do sinal antes e depois da filtragem.

## Funcionalidades

- geração de um sinal senoidal desejado;
- geração de uma interferência senoidal;
- combinação do sinal desejado com a interferência;
- escolha do filtro por meio de uma interface gráfica;
- configuração das frequências de corte;
- comparação entre o sinal original, o sinal com interferência e o sinal filtrado;
- limpeza dos gráficos para iniciar uma nova simulação.

Os filtros disponíveis são:

- passa-baixa;
- passa-alta;
- passa-faixa;
- rejeita-faixa.

## Tecnologias utilizadas

- Python;
- Tkinter e `ttk`, para a interface gráfica;
- NumPy, para os cálculos numéricos e a geração dos sinais;
- Matplotlib, para a construção dos gráficos.

## Requisitos

É necessário possuir o Python 3 instalado.

As bibliotecas NumPy e Matplotlib podem ser instaladas pelo terminal:

```bash
pip install numpy matplotlib
```

O Tkinter normalmente acompanha a instalação oficial do Python. Em algumas distribuições Linux, pode ser necessário instalá-lo separadamente.

Exemplo para Ubuntu ou Debian:

```bash
sudo apt install python3-tk
```

## Como executar

1. Baixe ou clone este repositório.
2. Abra o terminal na pasta do projeto.
3. Execute o arquivo principal:

```bash
python sinalruidosopassabaixa.py
```

No Windows, caso o comando anterior não funcione, experimente:

```bash
py sinalruidosopassabaixa.py
```

## Como utilizar a interface

Preencha os campos da simulação:

| Campo | Significado |
|---|---|
| Frequência do sinal | Frequência, em hertz, do sinal que se deseja analisar |
| Frequência do ruído | Frequência da interferência adicionada ao sinal |
| Amplitude do ruído | Intensidade da interferência em relação ao sinal principal |
| Tipo de filtro | Filtro que será aplicado ao sinal com interferência |
| `fc1` | Primeira frequência de corte |
| `fc2` | Segunda frequência de corte, usada no passa-faixa e no rejeita-faixa |

Depois de preencher os valores:

1. escolha o tipo de filtro;
2. defina a frequência ou as frequências de corte;
3. clique em **APLICAR FILTRO**;
4. analise os dois gráficos apresentados;
5. clique em **LIMPAR GRÁFICOS** para iniciar outra simulação.

## Construção do sinal

O sinal desejado é criado por:

```python
sinal = np.sin(2 * np.pi * freq_sinal * t)
```

A interferência é criada por:

```python
ruido = amplitude_ruido * np.sin(2 * np.pi * freq_ruido * t)
```

O sinal medido é a soma das duas componentes:

```python
sinal_ruidoso = sinal + ruido
```

Em termos matemáticos:

$$
x(t)=\sin(2\pi f_s t)+A_r\sin(2\pi f_r t)
$$

onde:

- $f_s$ é a frequência do sinal desejado;
- $f_r$ é a frequência da interferência;
- $A_r$ é a amplitude da interferência;
- $t$ é o tempo.

## Frequência de amostragem

O programa utiliza:

```python
fs = 1000
```

Isso significa que são utilizadas 1.000 amostras por segundo. O intervalo entre duas amostras consecutivas é:

$$
\Delta t=\frac{1}{f_s}=\frac{1}{1000}=0{,}001\text{ s}
$$

## Filtro passa-baixa

O passa-baixa preserva principalmente as frequências menores que a frequência de corte e atenua as frequências mais altas.

```python
def filtro_passa_baixa(x, fc, fs):
    dt = 1 / fs
    RC = 1 / (2 * np.pi * fc)
    alpha = dt / (RC + dt)

    y = np.zeros_like(x)
    y[0] = x[0]

    for i in range(1, len(x)):
        y[i] = y[i - 1] + alpha * (x[i] - y[i - 1])

    return y
```

O cálculo da saída utiliza a amostra anterior de saída e a nova amostra de entrada. Isso produz uma suavização do sinal e reduz oscilações rápidas.

Exemplo: sinal desejado de 5 Hz, interferência de 50 Hz e frequência de corte de 10 Hz. O filtro tende a preservar a componente de 5 Hz e reduzir a componente de 50 Hz.

## Filtro passa-alta

O passa-alta preserva principalmente as frequências maiores que a frequência de corte e atenua as frequências menores.

```python
def filtro_passa_alta(x, fc, fs):
    dt = 1 / fs
    RC = 1 / (2 * np.pi * fc)
    alpha = RC / (RC + dt)

    y = np.zeros_like(x)

    for i in range(1, len(x)):
        y[i] = alpha * (y[i - 1] + x[i] - x[i - 1])

    return y
```

Exemplo: com corte em 40 Hz, uma componente de 5 Hz é fortemente reduzida, enquanto uma componente de 50 Hz é parcialmente preservada.

## Filtro passa-faixa

O passa-faixa preserva as frequências localizadas entre dois valores de corte.

```python
def filtro_passa_faixa(x, fc1, fc2, fs):
    y = filtro_passa_alta(x, fc1, fs)
    y = filtro_passa_baixa(y, fc2, fs)
    return y
```

O funcionamento ocorre em duas etapas:

1. o passa-alta reduz as frequências abaixo de `fc1`;
2. o passa-baixa reduz as frequências acima de `fc2`.

Assim, permanece principalmente a faixa compreendida entre `fc1` e `fc2`.

Exemplo: para `fc1 = 20 Hz` e `fc2 = 50 Hz`, uma componente de 30 Hz será preservada, enquanto componentes de 5 Hz e 80 Hz serão atenuadas.

## Filtro rejeita-faixa

O rejeita-faixa faz o contrário do passa-faixa: reduz as frequências entre dois valores de corte e preserva as frequências externas à faixa.

```python
def filtro_rejeita_faixa(x, fc1, fc2, fs):
    baixa = filtro_passa_baixa(x, fc1, fs)
    alta = filtro_passa_alta(x, fc2, fs)
    y = baixa + alta
    return y
```

O programa separa e soma duas regiões:

1. `baixa` contém principalmente as frequências inferiores a `fc1`;
2. `alta` contém principalmente as frequências superiores a `fc2`;
3. a soma preserva as duas regiões e reduz a faixa central.

Exemplo: para `fc1 = 20 Hz` e `fc2 = 50 Hz`, uma componente de 30 Hz será atenuada, enquanto componentes de 5 Hz e 80 Hz serão preservadas.

## Frequências de corte

A frequência de corte não representa uma divisão completamente abrupta. Como os filtros implementados são de primeira ordem, a atenuação ocorre gradualmente.

Próximo à frequência de corte, uma componente pode continuar aparecendo no sinal de saída, porém com amplitude reduzida.

Para os filtros passa-faixa e rejeita-faixa, deve ser obedecida a condição:

```text
fc1 < fc2
```

Caso contrário, o programa exibe uma mensagem de erro.

## Interpretação dos gráficos

O gráfico da esquerda apresenta:

- o sinal desejado;
- o sinal desejado somado à interferência.

O gráfico da direita apresenta:

- o sinal após a aplicação do filtro;
- o sinal desejado, usado como referência para comparação.

O eixo horizontal representa o tempo, em segundos. O eixo vertical representa a amplitude do sinal.

## Funções da interface

### `atualizar_interface()`

Exibe o campo `fc2` somente quando o filtro escolhido necessita de duas frequências de corte.

### `executar()`

Lê os valores informados, gera o sinal, adiciona a interferência, aplica o filtro selecionado e atualiza os gráficos.

### `limpar()`

Apaga os gráficos anteriores e prepara a interface para uma nova simulação.

## Sugestões de testes

### Teste 1 — Remover interferência de alta frequência

| Parâmetro | Valor |
|---|---:|
| Sinal desejado | 5 Hz |
| Interferência | 50 Hz |
| Amplitude da interferência | 0,4 |
| Filtro | Passa-baixa |
| `fc1` | 10 Hz |

### Teste 2 — Preservar a componente de alta frequência

| Parâmetro | Valor |
|---|---:|
| Sinal desejado | 5 Hz |
| Interferência | 50 Hz |
| Amplitude da interferência | 0,4 |
| Filtro | Passa-alta |
| `fc1` | 40 Hz |

### Teste 3 — Selecionar uma faixa

Utilize um sinal cuja frequência esteja entre `fc1` e `fc2`. As componentes externas à faixa serão reduzidas.

### Teste 4 — Rejeitar uma faixa

Utilize uma interferência cuja frequência esteja entre `fc1` e `fc2`. Essa componente será reduzida, enquanto as frequências externas serão preservadas.

## Estrutura do projeto

```text
.
├── README.md
└── sinalruidosopassabaixa.py
```

## Objetivo educacional

O projeto foi desenvolvido para apoiar o estudo de condicionamento de sinais, filtros digitais, frequência de corte, amostragem e visualização de resultados por meio de uma interface gráfica.

Ele pode ser utilizado em atividades de Sistemas Ciberfísicos, Internet das Coisas, processamento de sinais, automação e programação aplicada à Engenharia.

## Autoria

**Profa. Karla Roberto Sartin**  
Engenharia Elétrica — Centro Universitário do Distrito Federal (UDF)

