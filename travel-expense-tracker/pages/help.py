import tkinter as tk
from tkinter import ttk


class Help(tk.Frame):
    """Forneça informações sobre o aplicativo"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # text to be displayed for each topic
        self.about = ["Sobre",
                      "Bem-vindo ao Registro de Despesas de Viagem! Neste aplicativo você "
                      "pode:\n\n"
                      "\t1. Registrar as viagens em que você esteve\n"
                      "\t2. Adicionar despesas para as viagens que você registrou\n"
                      "\t3. Criar uma tabela de suas despesas com todos os "
                      "Custos convertidos para qualquer moeda de sua escolha!"]

        self.trip = ["Viagens",
                     "Você pode adicionar o quanto quiser a sua "
                     "mesa. Digite suas informações para cada uma das caixas de "
                     "entrada.\n\n"
                     "Nome da viagem: Nomeie sua viagem! Isso pode ser o \n"
                     "destino da sua viagem ou qualquer coisa que você queira "
                     "Chamar de viagem.\n"
                     "Data de início: O primeiro dia da sua viagem\n"
                     "Data de término: O último dia da sua viagem\n"
                     "Tipo de viagem: Esta é uma viagem de trabalho? Viagem em família? "
                     "Férias?\n"
                     "Notas: Todas as notas que você deseja inserir "
                     "para relatar sua viagem"]

        self.expenses = ["Expense Log",
                         "Use this page to log expenses for any of the trips "
                         "that you have gone on.\n"
                         "You can add as much or as little as you want to your "
                         "table. Type in your information to each of the "
                         "entry boxes.\n\n"
                         "Select Trip: Select a trip from the  dropdown "
                         "list. This list is populated by your trips on the "
                         "log trips page.\n"
                         "Date:  \tThe date the purchase was "
                         "made\n"
                         "Category:\tSelect a category from the dropdown "
                         "menu\n"
                         "Currency:\tWhat currency did you  make the "
                         "purchase?\n"
                         "Cost:  \tHow much it cost (in designated currency)\n"
                         "Notes:   \tAny notes that you want to  enter "
                         "relating to the expense"]

        self.conv_exp = ["Convert Expenses",
                         "Use this page to create a copy of your expense "
                         "table in any currency that you choose.\n "
                         "You can select your currency by:\n\n"

                         "Alphabetic Code:\n"
                         "\tIf you know the alphabetic code  for the "
                         "currency, type it into this box.\n\t"
                         "If it isn't right, you will get a message saying "
                         "that it is not a valid code and to try again!.\n\n"

                         "Search By Country:\n"
                         "\tStart typing in the second box "
                         "to look up the country where you made the "
                         "purchase.\n\t"
                         "The listbox below will be filtered to match "
                         "your entry.\n\t"
                         "Once you find the country, double click and"
                         "the code will be put in the alphabetic code entry "
                         "box.\n\n"

                         "Submit:\n"
                         "\tClick on submit to populate your "
                         "converted expenses. Each row will be sent \n\t "
                         "through  a currency converter microservice "
                         "that takes in the original currency it was logged "
                         "as,\n\t"
                         " the cost, and your new chosen currency. The app  "
                         "then adds this to a new table that is shown\n\t"
                         " on the convert expenses page."]

        self.commands = ["Command Buttons",
                         "The My Trips and My Expenses tabs both have a "
                         "group of command buttons on the bottom. Read "
                         "below\n to find out more about what they do!"

                         "Add Data:\n"
                         "\tAfter you have filled in all of the entry boxes "
                         "for the page, press the add entry button on the "
                         "bottom.\n\tThis button will add your entry to the "
                         "table on the screen as well as a saved table in "
                         "the database.\n\n"

                         "Edit Data\n"
                         "\tIf you made a mistake when entering a row, "
                         "need to make a change, or what to add something\n\t"
                         "new, click on the row that you want to edit. The "
                         "values will be automatically placed into the "
                         "entry\n\tboxes below the table. Once you have made"
                         "your changes to the values in the entry boxes,\n\t"
                         "press Update Entry and the values will be changed "
                         "on screen and in the saved database.\n\n"

                         "Delete Entry:\n"
                         "\tClick on the row in the table that you would "
                         "like to delete. Once you click on Delete Entry,\n\t "
                         "That row will be deleted from the table and the "
                         "database\n\n"

                         "Delete All Entries\n"
                         "\tIf you would like to clear the table "
                         "completely, click on Delete All Entries. This \n\t "
                         "removes every entry from the table on the page and"
                         "in the database.\n\n"

                         "Clear Record Box:\n"
                         "\tIf you no longer want the values in the entry "
                         "boxes, you can go into each one and delete them.\n\t"
                         "Or you can click on clear record entries and every "
                         "entry box will be set to its default state."
                         ]

        # buttons for each topic
        self.button_frame = ttk.LabelFrame(parent, text="Selecione o tópico")
        self.button_frame.pack(fill='y', padx=10, pady=20, side="left")
        self.b_about = ttk.Button(self.button_frame, text="Sobre",
                                  command=lambda: self.display_info(self.about))
        self.b_trip = ttk.Button(self.button_frame, text="Registro de viagens",
                                 command=lambda: self.display_info(self.trip))
        self.b_expenses = ttk.Button(self.button_frame, text="Registro de despesas",
                                     command=lambda: self.display_info(
                                         self.expenses))
        self.b_conv_exp = ttk.Button(self.button_frame, text="Converter "
                                                             "Despesas",
                                     command=lambda: self.display_info(
                                         self.conv_exp))
        self.b_command = ttk.Button(self.button_frame, text="Comando de botões",
                                    command=lambda: self.display_info(
                                        self.commands))

        # Grid buttons and frame
        self.b_about.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.b_trip.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.b_expenses.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.b_conv_exp.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.b_command.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        self.info_frame = ttk.LabelFrame(parent, text="Information")
        self.info_frame.pack(fill='both', padx=10, pady=20, side="left")
        self.info = ttk.Label(self.info_frame, text="Welcome!\n\nSelect any "
                                                    "button to learn more "
                                                    "information about this "
                                                    "app")
        self.info.grid()

    def display_info(self, text):
        """Display information for selected button"""
        self.info_frame.config(text=text[0])
        self.info.config(text=text[1])
