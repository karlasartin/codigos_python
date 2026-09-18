import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def filtro_passa_baixa(x, fc, fs):

    dt = 1 / fs
    RC = 1 / (2 * np.pi * fc)

    alpha = dt / (RC + dt)

    y = np.zeros_like(x)
    y[0] = x[0]

    for i in range(1, len(x)):

        y[i] = (
            y[i - 1]
            + alpha * (x[i] - y[i - 1])
        )

    return y


def filtro_passa_alta(x, fc, fs):

    dt = 1 / fs
    RC = 1 / (2 * np.pi * fc)

    alpha = RC / (RC + dt)

    y = np.zeros_like(x)

    for i in range(1, len(x)):

        y[i] = alpha * (
            y[i - 1]
            + x[i]
            - x[i - 1]
        )

    return y


def filtro_passa_faixa(x, fc1, fc2, fs):

    y = filtro_passa_alta(
        x,
        fc1,
        fs
    )

    y = filtro_passa_baixa(
        y,
        fc2,
        fs
    )

    return y


def filtro_rejeita_faixa(x, fc1, fc2, fs):

    baixa = filtro_passa_baixa(
        x,
        fc1,
        fs
    )

    alta = filtro_passa_alta(
        x,
        fc2,
        fs
    )

    y = baixa + alta

    return y


def atualizar_interface(event=None):

    tipo = combo_filtro.get()

    if tipo in ["Passa-faixa", "Rejeita-faixa"]:

        label_fc2.grid()
        entry_fc2.grid()

    else:

        label_fc2.grid_remove()
        entry_fc2.grid_remove()


def limpar():

    ax1.clear()
    ax2.clear()

    ax1.set_title("Grafico do sinal de entrada")
    ax2.set_title("Grafico do sinal filtrado")

    ax1.set_xlabel("Tempo (s)")
    ax2.set_xlabel("Tempo (s)")

    ax1.set_ylabel("Amplitude")
    ax2.set_ylabel("Amplitude")

    ax1.grid(True)
    ax2.grid(True)

    figura.tight_layout(pad=4)
    canvas.draw()

    label_resultado.config(
        text="Graficos limpos. Configure uma nova simulacao."
    )

def executar():

    try:

        freq_sinal = float(
            entry_sinal.get()
        )

        freq_ruido = float(
            entry_ruido.get()
        )

        amplitude_ruido = float(
            entry_amplitude.get()
        )

        fc1 = float(
            entry_fc1.get()
        )

        tipo = combo_filtro.get()

        if tipo == "":

            messagebox.showerror(
                "Erro",
                "Escolha um tipo de filtro."
            )

            return

        fs = 1000

        duracao = 2

        t = np.arange(
            0,
            duracao,
            1 / fs
        )

        sinal = np.sin(
            2
            * np.pi
            * freq_sinal
            * t
        )

        ruido = (
            amplitude_ruido
            * np.sin(
                2
                * np.pi
                * freq_ruido
                * t
            )
        )

        sinal_ruidoso = (
            sinal
            + ruido
        )

        if tipo == "Passa-baixa":

            sinal_filtrado = filtro_passa_baixa(
                sinal_ruidoso,
                fc1,
                fs
            )

            descricao = (
                f"Passa-baixa | fc = {fc1:.1f} Hz"
            )


        elif tipo == "Passa-alta":

            sinal_filtrado = filtro_passa_alta(
                sinal_ruidoso,
                fc1,
                fs
            )

            descricao = (
                f"Passa-alta | fc = {fc1:.1f} Hz"
            )


        elif tipo == "Passa-faixa":

            fc2 = float(
                entry_fc2.get()
            )

            if fc1 >= fc2:

                messagebox.showerror(
                    "Erro",
                    "fc1 deve ser menor que fc2."
                )

                return

            sinal_filtrado = filtro_passa_faixa(
                sinal_ruidoso,
                fc1,
                fc2,
                fs
            )

            descricao = (
                f"Passa-faixa | "
                f"{fc1:.1f} Hz a {fc2:.1f} Hz"
            )


        elif tipo == "Rejeita-faixa":

            fc2 = float(
                entry_fc2.get()
            )

            if fc1 >= fc2:

                messagebox.showerror(
                    "Erro",
                    "fc1 deve ser menor que fc2."
                )

                return

            sinal_filtrado = filtro_rejeita_faixa(
                sinal_ruidoso,
                fc1,
                fc2,
                fs
            )

            descricao = (
                f"Rejeita-faixa | "
                f"{fc1:.1f} Hz a {fc2:.1f} Hz"
            )


        ax1.clear()
        ax2.clear()

        ax1.plot(
            t,
            sinal_ruidoso,
            label="Sinal + ruido"
        )

        ax1.plot(
            t,
            sinal,
            label="Sinal desejado"
        )

        ax1.set_title(
            "Sinal antes da filtragem"
        )

        ax1.set_xlabel(
            "Tempo (s)"
        )

        ax1.set_ylabel(
            "Amplitude"
        )

        ax1.grid(True)

        ax1.legend()


        ax2.plot(
            t,
            sinal_filtrado,
            label="Sinal filtrado"
        )

        ax2.plot(
            t,
            sinal,
            label="Sinal desejado"
        )

        ax2.set_title(
            descricao
        )

        ax2.set_xlabel(
            "Tempo (s)"
        )

        ax2.set_ylabel(
            "Amplitude"
        )

        ax2.grid(True)

        ax2.legend()


        canvas.draw()


        label_resultado.config(
            text=descricao
        )


    except ValueError:

        messagebox.showerror(
            "Erro",
            "Digite valores numericos validos."
        )


janela = tk.Tk()

janela.title(
    "Simulador de Condicionamento de Sinais"
)

janela.geometry(
    "1300x800"
)


titulo = tk.Label(
    janela,
    text="SIMULADOR DE FILTROS",
    font=(
        "Arial",
        20,
        "bold"
    )
)

titulo.pack(
    pady=10
)


frame = ttk.LabelFrame(
    janela,
    text="Parametros da Simulacao"
)

frame.pack(
    padx=20,
    pady=10,
    fill="x"
)


ttk.Label(
    frame,
    text="Freq. sinal (Hz)"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=10
)

entry_sinal = ttk.Entry(
    frame,
    width=8
)

entry_sinal.insert(
    0,
    "5"
)

entry_sinal.grid(
    row=0,
    column=1,
    padx=5
)


ttk.Label(
    frame,
    text="Freq. ruido (Hz)"
).grid(
    row=0,
    column=2,
    padx=5
)

entry_ruido = ttk.Entry(
    frame,
    width=8
)

entry_ruido.insert(
    0,
    "50"
)

entry_ruido.grid(
    row=0,
    column=3,
    padx=5
)


ttk.Label(
    frame,
    text="Amplitude ruido"
).grid(
    row=0,
    column=4,
    padx=5
)

entry_amplitude = ttk.Entry(
    frame,
    width=8
)

entry_amplitude.insert(
    0,
    "0.4"
)

entry_amplitude.grid(
    row=0,
    column=5,
    padx=5
)


ttk.Label(
    frame,
    text="Tipo de filtro"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=10
)

combo_filtro = ttk.Combobox(
    frame,
    values=[
        "Passa-baixa",
        "Passa-alta",
        "Passa-faixa",
        "Rejeita-faixa"
    ],
    state="readonly",
    width=15
)

combo_filtro.grid(
    row=1,
    column=1,
    padx=5
)

combo_filtro.set(
    "Passa-baixa"
)

combo_filtro.bind(
    "<<ComboboxSelected>>",
    atualizar_interface
)


ttk.Label(
    frame,
    text="fc1 (Hz)"
).grid(
    row=1,
    column=2,
    padx=5
)

entry_fc1 = ttk.Entry(
    frame,
    width=8
)

entry_fc1.insert(
    0,
    "10"
)

entry_fc1.grid(
    row=1,
    column=3,
    padx=5
)


label_fc2 = ttk.Label(
    frame,
    text="fc2 (Hz)"
)

label_fc2.grid(
    row=1,
    column=4,
    padx=5
)

entry_fc2 = ttk.Entry(
    frame,
    width=8
)

entry_fc2.insert(
    0,
    "60"
)

entry_fc2.grid(
    row=1,
    column=5,
    padx=5
)


botao = ttk.Button(
    frame,
    text="APLICAR FILTRO",
    command=executar
)

botao.grid(
    row=1,
    column=6,
    padx=10
)

botao_limpar = ttk.Button(
    frame,
    text="LIMPAR GRAFICOS",
    command=limpar
)

botao_limpar.grid(
    row=1,
    column=7,
    padx=10
)

label_resultado = tk.Label(
    janela,
    text="Escolha o filtro e execute a simulacao.",
    font=(
        "Arial",
        11,
        "bold"
    )
)

label_resultado.pack(
    pady=5
)


figura, (
    ax1,
    ax2
) = plt.subplots(
    1,
    2,
    figsize=(
        12,
        5
    )
)

figura.tight_layout(
    pad=4
)


canvas = FigureCanvasTkAgg(
    figura,
    master=janela
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


atualizar_interface()

janela.mainloop()