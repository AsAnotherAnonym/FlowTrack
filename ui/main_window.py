import customtkinter as ctk
from models.finance_manager import FinanceManager
from utils.constants import UIConstants
from utils.helpers import DateHelper, CurrencyHelper
from ui.components import UIComponents, TransactionCard

class FinanceApp(ctk.CTk):
    """
    Main Application Window
    
    Class UI utama aplikasi yang mengatur dan manage semua komponen
    dan berinteraksi dengan backend FinanceManager
    """
    
    def __init__(self):
        super().__init__()
        
        # Backend Manager (Business Logic)
        self.manager = FinanceManager()
        
        # Window Configuration
        self.title("FlowTrack - Personal Finance Manager")
        self.geometry(f"{UIConstants.WINDOW_WIDTH}x{UIConstants.WINDOW_HEIGHT}")
        self.resizable(True, True)
        
        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=UIConstants.DARK_BG)
        
        # UI Components
        self.widgets = {}
        
        # Build Interface
        self._create_ui()
        
        # Initial data load
        self.refresh_display()
    
    def _create_ui(self):
        # Configure Grid Layout (1 Row, 2 Columns)
        self.grid_columnconfigure(0, weight=0) # Sidebar fixed width
        self.grid_columnconfigure(1, weight=1) # Main content expands
        self.grid_rowconfigure(0, weight=1)    # Full height

        # LEFT PANEL (SIDEBAR)
        self.left_panel = ctk.CTkFrame(self, width=350, corner_radius=0, fg_color=UIConstants.CARD_BG)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.left_panel.pack_propagate(False) # Prevent shrinking

        # RIGHT PANEL (MAIN CONTENT)
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # --- Populate Sections ---
        # Left Panel Components
        self._create_app_title(self.left_panel)
        self._create_input_form_section(self.left_panel)
        self._create_highest_expense_section(self.left_panel)

        # Right Panel Components
        self._create_header_section(self.right_panel) # Stats
        self._create_transaction_feed_section(self.right_panel) # List

    def _create_app_title(self, parent):
        ctk.CTkLabel(
            parent, 
            text="FlowTrack (alpha)", 
            font=("Roboto", 24, "bold"),
            text_color=UIConstants.TEXT_PRIMARY
        ).pack(pady=(30, 20))
    
    # ==================== UI SECTIONS ====================

    def _create_header_section(self, parent):
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Layout Horizontal untuk Stats di Desktop
        # Total Balance (Kiri)
        balance_container = UIComponents.create_card_frame(header_frame)
        balance_container.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(balance_container, text="Total Balance", font=UIConstants.FONT_LABEL, text_color=UIConstants.TEXT_SECONDARY).pack(pady=(15,0))
        self.widgets["balance_value"] = ctk.CTkLabel(balance_container, text="Rp 0", font=UIConstants.FONT_BALANCE, text_color=UIConstants.TEXT_PRIMARY)
        self.widgets["balance_value"].pack(pady=(5, 15))

        # Income/Expense Summary (Kanan)
        stats_container = UIComponents.create_card_frame(header_frame)
        stats_container.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        stats_inner = ctk.CTkFrame(stats_container, fg_color="transparent")
        stats_inner.pack(expand=True, pady=15)
        
        # Income
        inc_frame = ctk.CTkFrame(stats_inner, fg_color="transparent")
        inc_frame.pack(side="left", padx=20)
        inc_lbl, inc_val = UIComponents.create_stat_display(inc_frame, "↓ Income", "Rp 0", UIConstants.INCOME_COLOR)
        inc_lbl.pack(); inc_val.pack()
        self.widgets["income_value"] = inc_val

        # Expense
        exp_frame = ctk.CTkFrame(stats_inner, fg_color="transparent")
        exp_frame.pack(side="left", padx=20)
        exp_lbl, exp_val = UIComponents.create_stat_display(exp_frame, "↑ Expense", "Rp 0", UIConstants.EXPENSE_COLOR)
        exp_lbl.pack(); exp_val.pack()
        self.widgets["expense_value"] = exp_val

    def _create_highest_expense_section(self, parent):
        # Tidak perlu Card Frame lagi karena sidebar sudah berwarna gelap
        container = ctk.CTkFrame(parent, fg_color="transparent") 
        container.pack(padx=20, pady=(20, 10), fill="x", side="bottom") # Taruh di bawah sidebar

        ctk.CTkLabel(container, text="🔥 Highest Expense (Max-Heap)", font=(UIConstants.FONT_FAMILY, 12, "bold"), text_color=UIConstants.TEXT_SECONDARY).pack(anchor="w")
        
        self.widgets["highest_expense"] = ctk.CTkLabel(
            container, text="No expenses yet", font=("Roboto", 16, "bold"), 
            text_color=UIConstants.EXPENSE_COLOR, anchor="w"
        )
        self.widgets["highest_expense"].pack(fill="x", pady=(5, 0))

    def _create_input_form_section(self, parent):
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(padx=20, fill="x")

        ctk.CTkLabel(form_frame, text="New Transaction", font=UIConstants.FONT_TITLE, text_color=UIConstants.TEXT_PRIMARY).pack(pady=(0, 15), anchor="w")

        # Date
        self.widgets["date_entry"] = UIComponents.create_input_field(form_frame, "Date")
        self.widgets["date_entry"].pack(pady=5, fill="x")
        self.widgets["date_entry"].insert(0, DateHelper.get_today())

        # Title
        self.widgets["title_entry"] = UIComponents.create_input_field(form_frame, "Title")
        self.widgets["title_entry"].pack(pady=5, fill="x")

        # Amount
        self.widgets["amount_entry"] = UIComponents.create_input_field(form_frame, "Amount")
        self.widgets["amount_entry"].pack(pady=5, fill="x")

        # Category
        self.widgets["category_entry"] = UIComponents.create_input_field(form_frame, "Category")
        self.widgets["category_entry"].pack(pady=5, fill="x")

        # Radio Buttons
        self.widgets["type_var"] = ctk.StringVar(value="Expense")
        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.pack(pady=10, fill="x")
        
        ctk.CTkRadioButton(type_frame, text="Income", variable=self.widgets["type_var"], value="Income", fg_color=UIConstants.INCOME_COLOR).pack(side="left", padx=(0, 10))
        ctk.CTkRadioButton(type_frame, text="Expense", variable=self.widgets["type_var"], value="Expense", fg_color=UIConstants.EXPENSE_COLOR).pack(side="left")

        # Add Button
        UIComponents.create_button(form_frame, "Add Transaction", self.add_transaction, "primary").pack(pady=20, fill="x")

    def _create_transaction_feed_section(self, parent):
        # Header Label for List
        ctk.CTkLabel(parent, text="History (Doubly Linked List)", font=UIConstants.FONT_TITLE, text_color=UIConstants.TEXT_PRIMARY).pack(anchor="w", pady=(10, 10))

        # Scrollable Frame that expands
        self.widgets["scrollable_frame"] = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.widgets["scrollable_frame"].pack(fill="both", expand=True)
    
    # ==================== EVENT HANDLERS ====================
    
    def add_transaction(self):
        """
        Handler klik tombol tambah transaksi
        Memvalidasi input dan memasukkan ke dalam DLL
        """
        try:
            # Get input values
            date = self.widgets["date_entry"].get().strip()
            title = self.widgets["title_entry"].get().strip()
            amount_str = self.widgets["amount_entry"].get().strip()
            trans_type = self.widgets["type_var"].get()
            category = self.widgets["category_entry"].get().strip()
            
            # Validation
            if not all([date, title, category, amount_str]):
                self._show_error("All fields are required")
                return
            
            amount = float(amount_str)
            if amount <= 0:
                self._show_error("Amount must be positive")
                return
            
            # INSERT AT HEAD OF DOUBLY LINKED LIST
            self.manager.insert_at_head(date, title, amount, trans_type, category)
            
            # Save to file
            self.manager.save_to_file()
            
            # Clear inputs
            self._clear_form()
            
            # Refresh UI
            self.refresh_display()
            
        except ValueError:
            self._show_error("Invalid amount. Please enter a number.")
    
    def delete_transaction(self, trans_id: int):
        """
        Handle hapus transaksi
        Mengapus node dari DLL dan memperbarui UI
        
        Args:
            trans_id: ID of transaction to delete
        """
        node = self.manager.find_node_by_id(trans_id)
        if node:
            self.manager.delete_node(node)
            self.manager.save_to_file()
            self.refresh_display()
    
    # ==================== UI UPDATE METHODS ====================
    
    def refresh_display(self):
        """
        Me-refresh seluruh komponen UI dengan data terkini
        Menggunakan Hash Map untuk mengelompokkan transaksi berdasarkan tanggal
        """
        # Update dashboard statistics
        stats = self.manager.get_stats()
        
        self.widgets["balance_value"].configure(
            text=CurrencyHelper.format_amount(stats["balance"])
        )
        self.widgets["income_value"].configure(
            text=CurrencyHelper.format_amount(stats["total_income"])
        )
        self.widgets["expense_value"].configure(
            text=CurrencyHelper.format_amount(stats["total_expense"])
        )
        
        # UPDATE HIGHEST EXPENSE FROM MAX-HEAP
        highest = self.manager.get_highest_expense()
        if highest:
            highest_text = f"{highest.title} - {CurrencyHelper.format_amount(highest.amount)}"
            self.widgets["highest_expense"].configure(
                text=highest_text,
                text_color=UIConstants.EXPENSE_COLOR
            )
        else:
            self.widgets["highest_expense"].configure(
                text="No expenses yet",
                text_color=UIConstants.TEXT_SECONDARY
            )
        
        # Clear transaction feed
        for widget in self.widgets["scrollable_frame"].winfo_children():
            widget.destroy()
        
        # USE HASH MAP TO GROUP BY DATE
        date_groups = self.manager.group_by_date()
        
        if not date_groups:
            # Show empty state
            empty_label = ctk.CTkLabel(
                self.widgets["scrollable_frame"],
                text="No transactions yet\nAdd your first transaction above!",
                font=UIConstants.FONT_LABEL,
                text_color=UIConstants.TEXT_SECONDARY
            )
            empty_label.pack(pady=50)
            return
        
        # Sort dates (newest first)
        sorted_dates = sorted(date_groups.keys(), reverse=True)
        
        # Display grouped transactions
        for date_str in sorted_dates:
            # Date Header
            date_header = DateHelper.format_date_header(date_str)
            header_label = ctk.CTkLabel(
                self.widgets["scrollable_frame"],
                text=date_header,
                font=(UIConstants.FONT_FAMILY, 13, "bold"),
                text_color=UIConstants.TEXT_SECONDARY,
                anchor="w"
            )
            header_label.pack(fill="x", pady=(10, 5))
            
            # Transaction Cards for this date
            for node in date_groups[date_str]:
                TransactionCard(
                    self.widgets["scrollable_frame"],
                    node,
                    self.delete_transaction
                )
    
    # ==================== HELPER METHODS ====================
    
    def _clear_form(self):
        """Clear semua form input"""
        self.widgets["title_entry"].delete(0, "end")
        self.widgets["amount_entry"].delete(0, "end")
        self.widgets["category_entry"].delete(0, "end")
        self.widgets["date_entry"].delete(0, "end")
        self.widgets["date_entry"].insert(0, DateHelper.get_today())
    
    def _show_error(self, message: str):
        """
        Sekarang masih console print, bisa diganti popup nanti
        
        Args:
            message: Error message to display
        """
        print(f"Error: {message}")
