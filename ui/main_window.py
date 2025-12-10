import customtkinter as ctk
from models.finance_manager import FinanceManager
from utils.constants import UIConstants
from utils.helpers import DateHelper, CurrencyHelper
from ui.components import UIComponents, TransactionCard
from datetime import datetime
import os

class FinanceApp(ctk.CTk):
    """
    Main Application Window
    """

    def __init__(self):
        super().__init__()

        self.manager = FinanceManager()

        self.title("FlowTrack - Personal Finance Manager")
        self.geometry(f"{UIConstants.WINDOW_WIDTH}x{UIConstants.WINDOW_HEIGHT}")
        self.resizable(True, True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=UIConstants.DARK_BG)

        self.widgets = {}

        self._create_ui()
        self.refresh_display()

    # ==================== FORMAT ANGKA OTOMATIS ====================
    def _format_amount(self, event=None):
        entry = self.widgets["amount_entry"]
        value = entry.get().replace(".", "")

        if value == "":
            return
        
        if value.isdigit():
            formatted = "{:,}".format(int(value)).replace(",", ".")
            entry.delete(0, "end")
            entry.insert(0, formatted)

    def _toggle_recurrence_options(self):
        """Enable/disable recurrence type dropdown berdasarkan checkbox status"""
        is_recurring = self.widgets["recurring_var"].get() == 1
        if is_recurring:
            self.widgets["recurrence_type"].configure(state="normal")
        else:
            self.widgets["recurrence_type"].configure(state="disabled")

    # ==================== UI CREATION ====================

    def _create_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(self, width=350, corner_radius=0, fg_color=UIConstants.CARD_BG)
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        self.left_panel.pack_propagate(False)

        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self._create_app_title(self.left_panel)
        self._create_action_buttons(self.left_panel)
        self._create_input_form_section(self.left_panel)
        self._create_budget_section(self.left_panel)
        self._create_highest_expense_section(self.left_panel)

        self._create_header_section(self.right_panel)
        self._create_transaction_feed_section(self.right_panel)

    def _create_app_title(self, parent):
        ctk.CTkLabel(parent, text="FlowTrack (alpha)", font=("Roboto", 24, "bold"),
                     text_color=UIConstants.TEXT_PRIMARY).pack(pady=(30, 20))

    # ==================== ACTION BUTTONS ====================
    def _create_action_buttons(self, parent):
        """Tombol untuk Export dan action lainnya"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(padx=20, fill="x", pady=(0, 15))
        
        export_btn = UIComponents.create_button(
            button_frame, 
            "📊 Export CSV", 
            self.export_transactions,
            style="primary",
            height=35,
            font=(UIConstants.FONT_FAMILY, 12, "bold")
        )
        export_btn.pack(fill="x", pady=5)

    # ==================== HEADER SECTION ====================
    def _create_header_section(self, parent):
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        balance_container = UIComponents.create_card_frame(header_frame)
        balance_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(balance_container, text="Jumlah uang", font=UIConstants.FONT_LABEL,
                     text_color=UIConstants.TEXT_SECONDARY).pack(pady=(15, 0))
        self.widgets["balance_value"] = ctk.CTkLabel(balance_container, text="Rp 0",
                                                     font=UIConstants.FONT_BALANCE,
                                                     text_color=UIConstants.TEXT_PRIMARY)
        self.widgets["balance_value"].pack(pady=(5, 15))

        stats_container = UIComponents.create_card_frame(header_frame)
        stats_container.pack(side="right", fill="both", expand=True, padx=(10, 0))

        stats_inner = ctk.CTkFrame(stats_container, fg_color="transparent")
        stats_inner.pack(expand=True, pady=15)

        # Income
        inc_frame = ctk.CTkFrame(stats_inner, fg_color="transparent")
        inc_frame.pack(side="left", padx=20)
        inc_lbl, inc_val = UIComponents.create_stat_display(
            inc_frame, "↓ Pemasukan", "Rp 0", UIConstants.INCOME_COLOR)
        inc_lbl.pack(); inc_val.pack()
        self.widgets["income_value"] = inc_val

        # Expense
        exp_frame = ctk.CTkFrame(stats_inner, fg_color="transparent")
        exp_frame.pack(side="left", padx=20)
        exp_lbl, exp_val = UIComponents.create_stat_display(
            exp_frame, "↑ Pengeluaran", "Rp 0", UIConstants.EXPENSE_COLOR)
        exp_lbl.pack(); exp_val.pack()
        self.widgets["expense_value"] = exp_val

    # ==================== HIGHEST EXPENSE ====================
    def _create_highest_expense_section(self, parent):
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(padx=20, pady=(20, 10), fill="x", side="bottom")

        ctk.CTkLabel(container, text="🔥 Highest Expense (Max-Heap)",
                     font=(UIConstants.FONT_FAMILY, 12, "bold"),
                     text_color=UIConstants.TEXT_SECONDARY).pack(anchor="w")

        self.widgets["highest_expense"] = ctk.CTkLabel(
            container, text="No expenses yet", font=("Roboto", 16, "bold"),
            text_color=UIConstants.EXPENSE_COLOR)
        self.widgets["highest_expense"].pack(fill="x", pady=(5, 0))

    # ==================== BUDGET SECTION ====================
    def _create_budget_section(self, parent):
        """Monthly Budget Tracker dengan progress bar"""
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(padx=20, pady=(0, 20), fill="x")

        ctk.CTkLabel(container, text="💰 Anggaran Bulanan",
                     font=(UIConstants.FONT_FAMILY, 12, "bold"),
                     text_color=UIConstants.TEXT_PRIMARY).pack(anchor="w", pady=(0, 10))

        # Budget input frame
        input_frame = ctk.CTkFrame(container, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 10))

        self.widgets["budget_entry"] = UIComponents.create_input_field(
            input_frame, 
            "Jumlah Anggaran",
            width=150,
            height=35
        )
        self.widgets["budget_entry"].pack(side="left", padx=(0, 5), fill="x", expand=True)

        set_budget_btn = UIComponents.create_button(
            input_frame,
            "Atur",
            self.set_monthly_budget,
            style="primary",
            width=60,
            height=35,
            font=(UIConstants.FONT_FAMILY, 12)
        )
        set_budget_btn.pack(side="left")

        # Progress bar
        progress_label = ctk.CTkLabel(container, text="Pengeluaran vs Anggaran:",
                                     font=(UIConstants.FONT_FAMILY, 10),
                                     text_color=UIConstants.TEXT_SECONDARY)
        progress_label.pack(anchor="w", pady=(5, 2))
        
        self.widgets["budget_progress"] = UIComponents.create_progress_bar(
            container,
            value=0.0,
            width=310,
            height=20
        )
        self.widgets["budget_progress"].pack(fill="x", pady=(2, 5), padx=0)

        # Status label
        self.widgets["budget_status"] = ctk.CTkLabel(
            container,
            text="Anggaran belum diatur",
            font=(UIConstants.FONT_FAMILY, 11),
            text_color=UIConstants.TEXT_SECONDARY,
            justify="left"
        )
        self.widgets["budget_status"].pack(anchor="w", pady=(5, 0))

    # ==================== INPUT FORM ====================
    def _create_input_form_section(self, parent):
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(padx=20, fill="x")

        ctk.CTkLabel(form_frame, text="New Transaction",
                     font=UIConstants.FONT_TITLE,
                     text_color=UIConstants.TEXT_PRIMARY).pack(pady=(0, 15), anchor="w")

        self.widgets["date_entry"] = UIComponents.create_input_field(form_frame, "Tanggal")
        self.widgets["date_entry"].pack(pady=5, fill="x")
        self.widgets["date_entry"].insert(0, DateHelper.get_today())

        self.widgets["title_entry"] = UIComponents.create_input_field(form_frame, "Judul")
        self.widgets["title_entry"].pack(pady=5, fill="x")

        # Amount with auto-format
        self.widgets["amount_entry"] = UIComponents.create_input_field(form_frame, "Total")
        self.widgets["amount_entry"].pack(pady=5, fill="x")
        self.widgets["amount_entry"].bind("<KeyRelease>", self._format_amount)

        self.widgets["category_entry"] = UIComponents.create_input_field(form_frame, "Catatan")
        self.widgets["category_entry"].pack(pady=5, fill="x")

        self.widgets["type_var"] = ctk.StringVar(value="Expense")
        type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        type_frame.pack(pady=10, fill="x")

        ctk.CTkRadioButton(type_frame, text="Pemasukan",
                           variable=self.widgets["type_var"], value="Income",
                           fg_color=UIConstants.INCOME_COLOR).pack(side="left", padx=(0, 10))
        ctk.CTkRadioButton(type_frame, text="Pengeluaran",
                           variable=self.widgets["type_var"], value="Expense",
                           fg_color=UIConstants.EXPENSE_COLOR).pack(side="left")

        # Recurring checkbox
        self.widgets["recurring_var"] = ctk.IntVar(value=0)
        recurring_check = UIComponents.create_checkbox(
            form_frame,
            "🔄 Recurring Transaction",
            variable=self.widgets["recurring_var"],
            command=self._toggle_recurrence_options
        )
        recurring_check.pack(anchor="w", pady=5)

        # Recurrence type (hidden by default)
        self.widgets["recurrence_frame"] = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.widgets["recurrence_frame"].pack(fill="x", pady=5)
        
        ctk.CTkLabel(self.widgets["recurrence_frame"], text="Pilih Tipe:", font=(UIConstants.FONT_FAMILY, 12),
                    text_color=UIConstants.TEXT_SECONDARY).pack(side="left", padx=(0, 10))

        self.widgets["recurrence_type"] = UIComponents.create_combobox(
            self.widgets["recurrence_frame"],
            values=["weekly", "monthly"],
            state="disabled"
        )
        self.widgets["recurrence_type"].set("monthly")
        self.widgets["recurrence_type"].pack(side="left", fill="x", expand=True)

        UIComponents.create_button(form_frame, "Tambah Transaksi",
                                   self.add_transaction, "primary").pack(pady=20, fill="x")

    # ==================== TRANSACTION FEED ====================
    def _create_transaction_feed_section(self, parent):
        ctk.CTkLabel(parent, text="Riwayat Transaksi", font=UIConstants.FONT_TITLE,
                     text_color=UIConstants.TEXT_PRIMARY).pack(anchor="w", pady=(10, 10))

        self.widgets["scrollable_frame"] = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        self.widgets["scrollable_frame"].pack(fill="both", expand=True)

    # ==================== EVENT HANDLERS ====================
    def add_transaction(self):
        try:
            date = self.widgets["date_entry"].get().strip()
            title = self.widgets["title_entry"].get().strip()
            amount_str = self.widgets["amount_entry"].get().replace(".", "").strip()
            trans_type = self.widgets["type_var"].get()
            category = self.widgets["category_entry"].get().strip()
            is_recurring = self.widgets["recurring_var"].get() == 1
            recurrence_type = self.widgets["recurrence_type"].get() if is_recurring else None

            if not all([date, title, category, amount_str]):
                self._show_error("All fields are required")
                return

            amount = float(amount_str)
            if amount <= 0:
                self._show_error("Amount must be positive")
                return

            self.manager.insert_at_head(date, title, amount, trans_type, category,
                                       is_recurring, recurrence_type)
            self.manager.save_to_file()
            self._clear_form()
            self.refresh_display()

        except ValueError:
            self._show_error("Invalid amount. Please enter a number.")

    def delete_transaction(self, trans_id: int):
        """Delete transaction"""
        node = self.manager.find_node_by_id(trans_id)
        if node:
            self.manager.delete_node(node)
            self.manager.save_to_file()
            self.refresh_display()

    def edit_transaction(self, node):
        """Open edit modal for transaction"""
        self._open_edit_modal(node)

    def export_transactions(self):
        """Export transaksi ke CSV"""
        try:
            filename = f"flowtrack_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            if self.manager.export_to_csv(filename):
                self._show_error(f"✓ Exported to {filename}")
            else:
                self._show_error("Failed to export")
        except Exception as e:
            self._show_error(f"Export error: {str(e)}")

    def set_monthly_budget(self):
        """Set budget untuk bulan ini"""
        try:
            budget_str = self.widgets["budget_entry"].get().replace(".", "").strip()
            if not budget_str:
                self._show_error("Please enter budget amount")
                return
            
            budget = float(budget_str)
            if budget <= 0:
                self._show_error("Budget must be positive")
                return
            
            current_month = datetime.now().strftime("%Y-%m")
            self.manager.budget_bst.insert(current_month, budget)
            self.widgets["budget_entry"].delete(0, "end")
            self.refresh_display()
        except ValueError:
            self._show_error("Invalid budget amount")

    def _open_edit_modal(self, node):
        """Open modal window untuk edit transaction"""
        modal = ctk.CTkToplevel(self)
        modal.title(f"Edit Transaction - {node.title}")
        modal.geometry("400x400")
        modal.resizable(False, False)

        # Center modal
        modal.transient(self)
        modal.grab_set()

        # Form fields
        form_frame = ctk.CTkFrame(modal, fg_color="transparent")
        form_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="Edit Transaction",
                    font=UIConstants.FONT_TITLE,
                    text_color=UIConstants.TEXT_PRIMARY).pack(pady=(0, 20), anchor="w")

        # Date
        ctk.CTkLabel(form_frame, text="Date:", font=(UIConstants.FONT_FAMILY, 12)).pack(anchor="w")
        date_entry = UIComponents.create_input_field(form_frame, "Date")
        date_entry.pack(fill="x", pady=5)
        date_entry.insert(0, node.date)

        # Title
        ctk.CTkLabel(form_frame, text="Title:", font=(UIConstants.FONT_FAMILY, 12)).pack(anchor="w")
        title_entry = UIComponents.create_input_field(form_frame, "Title")
        title_entry.pack(fill="x", pady=5)
        title_entry.insert(0, node.title)

        # Amount
        ctk.CTkLabel(form_frame, text="Amount:", font=(UIConstants.FONT_FAMILY, 12)).pack(anchor="w")
        amount_entry = UIComponents.create_input_field(form_frame, "Amount")
        amount_entry.pack(fill="x", pady=5)
        amount_entry.insert(0, str(node.amount))

        # Category
        ctk.CTkLabel(form_frame, text="Category:", font=(UIConstants.FONT_FAMILY, 12)).pack(anchor="w")
        category_entry = UIComponents.create_input_field(form_frame, "Category")
        category_entry.pack(fill="x", pady=5)
        category_entry.insert(0, node.category)

        # Save button
        def save_changes():
            try:
                new_date = date_entry.get().strip()
                new_title = title_entry.get().strip()
                new_amount = float(amount_entry.get().replace(".", "").strip())
                new_category = category_entry.get().strip()

                self.manager.update_node(node, new_date, new_title, new_amount,
                                        category=new_category)
                self.manager.save_to_file()
                self.refresh_display()
                modal.destroy()
                self._show_error("✓ Transaction updated")
            except ValueError:
                self._show_error("Invalid input")

        save_btn = UIComponents.create_button(
            form_frame,
            "Save Changes",
            save_changes,
            style="primary"
        )
        save_btn.pack(pady=20, fill="x")

    # ==================== UI UPDATES ====================
    def refresh_display(self):
        stats = self.manager.get_stats()

        self.widgets["balance_value"].configure(text=CurrencyHelper.format_amount(stats["balance"]))
        self.widgets["income_value"].configure(text=CurrencyHelper.format_amount(stats["total_income"]))
        self.widgets["expense_value"].configure(text=CurrencyHelper.format_amount(stats["total_expense"]))

        highest = self.manager.get_highest_expense()
        if highest:
            self.widgets["highest_expense"].configure(
                text=f"{highest.title} - {CurrencyHelper.format_amount(highest.amount)}",
                text_color=UIConstants.EXPENSE_COLOR)
        else:
            self.widgets["highest_expense"].configure(
                text="No expenses yet",
                text_color=UIConstants.TEXT_SECONDARY)

        # Update budget display
        current_month = datetime.now().strftime("%Y-%m")
        budget_node = self.manager.budget_bst.search(current_month)
        if budget_node:
            remaining = budget_node.get_remaining()
            percentage = budget_node.get_percentage()
            
            # Update progress bar
            progress_value = min(percentage / 100, 1.0)
            self.widgets["budget_progress"].set(progress_value)
            
            # Update status label with color warning
            if budget_node.is_over_budget():
                status_color = UIConstants.EXPENSE_COLOR
                status_text = f"⚠️ Over budget by {CurrencyHelper.format_amount(budget_node.spent - budget_node.budget_limit)}"
            elif budget_node.is_near_limit():
                status_color = "#FFA500"  # Orange
                status_text = f"⚡ Near limit: {CurrencyHelper.format_amount(remaining)} remaining ({percentage:.0f}%)"
            else:
                status_color = UIConstants.INCOME_COLOR
                status_text = f"✓ {CurrencyHelper.format_amount(remaining)} remaining ({percentage:.0f}%)"
            
            self.widgets["budget_status"].configure(text=status_text, text_color=status_color)
        else:
            self.widgets["budget_progress"].set(0.0)
            self.widgets["budget_status"].configure(
                text="No budget set",
                text_color=UIConstants.TEXT_SECONDARY
            )

        for widget in self.widgets["scrollable_frame"].winfo_children():
            widget.destroy()

        date_groups = self.manager.group_by_date()

        if not date_groups:
            empty_label = ctk.CTkLabel(
                self.widgets["scrollable_frame"],
                text="No transactions yet\nAdd your first transaction above!",
                font=UIConstants.FONT_LABEL,
                text_color=UIConstants.TEXT_SECONDARY
            )
            empty_label.pack(pady=50)
            return

        sorted_dates = sorted(date_groups.keys(), reverse=True)

        for date_str in sorted_dates:
            date_header = DateHelper.format_date_header(date_str)
            header_label = ctk.CTkLabel(
                self.widgets["scrollable_frame"],
                text=date_header,
                font=(UIConstants.FONT_FAMILY, 13, "bold"),
                text_color=UIConstants.TEXT_SECONDARY,
                anchor="w"
            )
            header_label.pack(fill="x", pady=(10, 5))

            for node in date_groups[date_str]:
                card = TransactionCard(
                    self.widgets["scrollable_frame"],
                    node,
                    self.delete_transaction,
                    self.edit_transaction
                )

    # ==================== HELPER METHODS ====================
    def _clear_form(self):
        self.widgets["title_entry"].delete(0, "end")
        self.widgets["amount_entry"].delete(0, "end")
        self.widgets["category_entry"].delete(0, "end")
        self.widgets["date_entry"].delete(0, "end")
        self.widgets["date_entry"].insert(0, DateHelper.get_today())

    def _show_error(self, message: str):
        print(f"Error: {message}")
