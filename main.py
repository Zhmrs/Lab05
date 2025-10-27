import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO
    marca=ft.TextField(label="Marca")
    modello=ft.TextField(label="Modello")
    anno=ft.TextField(label="Anno")

    textOut = ft.TextField(width=100,
                           text_size=24,
                           disabled=True,  # DISABILITARE LA CASELLA DI TESTO (IMMODIFICABILE)
                           text_align=ft.TextAlign.CENTER)

    # INSERISCO IL VALROE INIZIALE
    textOut.value = 2

    # funzioni che aumentano e diminuiscono i valori
    def haldlerMinus(e):
        currentVal = textOut.value
        if currentVal > 0:  # se è maggiore di zero posso decrementare, senza andare sotto lo zero
            currentVal = currentVal - 1
            textOut.value = currentVal  # reimposto e collegare con il bottone
            textOut.update()  # AGGIORNO SOLO IL TESTO

    def haldlerPlus(e):
        currentVal = textOut.value
        currentVal = currentVal + 1
        textOut.value = currentVal  # reimposto e collegare con il bottone
        textOut.update()

    # AGGIUNGO DUE BOTTONI (icona)
    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE_CIRCLE_ROUNDED,
                             icon_size=24,
                             icon_color='red',
                             on_click=haldlerMinus)
    btnPlus = ft.IconButton(icon=ft.Icons.ADD_CIRCLE_ROUNDED,
                            icon_size=24,
                            icon_color='green',
                            on_click=haldlerPlus)

    contatore= ft.Row([btnMinus, textOut, btnPlus],
                 alignment=ft.MainAxisAlignment.CENTER)

    # ALLINEO IN UNA RIGA I CONTROLLI PER INSERIRE MARCA, MODELLO E ANNO
    row1=ft.Row([marca,modello,anno,contatore], alignment=ft.MainAxisAlignment.CENTER)

    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def aggiungi_automobile(e):
        marca_val = marca.value.strip()
        modello_val = modello.value.strip()
        anno_val = anno.value.strip()
        posti_val = textOut.value

        # Se l'anno inserito non è un numero
        if not anno_val.isdigit():
            alert.show_alert(f"❌ Errore:inserisci valori numerici validi per anno e posti")


        # Aggiunta alla struttura dati controllando che tutti i campi siano compilati
        if not marca_val or not modello_val or not anno_val:
            alert.show_alert("⚠️ Tutti i campi devono essere compilati.")
        else:
            autonoleggio.aggiungi_automobile(marca_val, modello_val, anno_val, posti_val)

        # Pulizia dei campi
        marca.value = ""
        modello.value = ""
        anno.value = ""
        textOut.value = 2
        page.update()

        # Aggiornamento della lista
        aggiorna_lista_auto()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    btn_aggiungi_automobile=ft.ElevatedButton('Aggiungi automobile',on_click=aggiungi_automobile)
    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Text('Aggiungi Nuova Automobile',size=20),
        row1,
        btn_aggiungi_automobile,
        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
