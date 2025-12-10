import customtkinter as ctk
from utils.constants import UIConstants
from utils.helpers import CurrencyHelper
from models.transaction_node import TransactionNode
from typing import Callable, Optional

class UIComponents:
    
    @staticmethod
    def create_card_frame(parent, **kwargs) -> ctk.CTkFrame:
        """
        Args:
            parent: Parent widget
            **kwargs: Additional CTkFrame arguments
        
        Returns:
            Configured CTkFrame
        """
        default_kwargs = {
            "fg_color": UIConstants.CARD_BG,
            "corner_radius": 15
        }
        default_kwargs.update(kwargs)
        return ctk.CTkFrame(parent, **default_kwargs)
    
    @staticmethod
    def create_stat_display(parent, label_text: str, value_text: str, 
                           color: str) -> tuple:
        """
        (label + value)
        
        Args:
            parent: Parent widget
            label_text: Label text (e.g., "Income")
            value_text: Value text (e.g., "Rp 50,000")
            color: Text color for value
        
        Returns:
            Tuple of (label_widget, value_widget)
        """
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=UIConstants.FONT_SMALL,
            text_color=color
        )
        
        value = ctk.CTkLabel(
            parent,
            text=value_text,
            font=UIConstants.FONT_STAT,
            text_color=color
        )
        
        return label, value
    
    @staticmethod
    def create_input_field(parent, placeholder: str, **kwargs) -> ctk.CTkEntry:
        """
        Args:
            parent: Parent widget
            placeholder: Placeholder text
            **kwargs: Additional CTkEntry arguments
        
        Returns:
            Configured CTkEntry
        """
        default_kwargs = {
            "placeholder_text": placeholder,
            "font": (UIConstants.FONT_FAMILY, 13),
            "height": 40
        }
        default_kwargs.update(kwargs)
        return ctk.CTkEntry(parent, **default_kwargs)
    
    @staticmethod
    def create_button(parent, text: str, command, style: str = "primary", 
                     **kwargs) -> ctk.CTkButton:
        """
        Args:
            parent: Parent widget
            text: Button text
            command: Click callback
            style: "primary" or "danger"
            **kwargs: Additional CTkButton arguments
        
        Returns:
            Configured CTkButton
        """
        if style == "primary":
            fg_color = UIConstants.BUTTON_PRIMARY
            hover_color = UIConstants.BUTTON_PRIMARY_HOVER
        else:  # danger
            fg_color = UIConstants.BUTTON_DANGER
            hover_color = UIConstants.BUTTON_DANGER_HOVER
        
        default_kwargs = {
            "text": text,
            "command": command,
            "font": (UIConstants.FONT_FAMILY, 14, "bold"),
            "fg_color": fg_color,
            "hover_color": hover_color
        }
        default_kwargs.update(kwargs)
        return ctk.CTkButton(parent, **default_kwargs)
    
    @staticmethod
    def create_progress_bar(parent, value: float = 0.0, **kwargs) -> ctk.CTkProgressBar:
        """
        Create progress bar untuk budget tracker
        
        Args:
            parent: Parent widget
            value: Initial value (0.0-1.0)
            **kwargs: Additional CTkProgressBar arguments
        
        Returns:
            Configured CTkProgressBar
        """
        default_kwargs = {
            "height": 15,
            "corner_radius": 5
        }
        default_kwargs.update(kwargs)
        bar = ctk.CTkProgressBar(parent, **default_kwargs)
        bar.set(min(value, 1.0))  # Clamp ke 1.0
        return bar
    
    @staticmethod
    def create_checkbox(parent, text: str, variable=None, **kwargs) -> ctk.CTkCheckBox:
        """
        Create checkbox untuk recurring transaction
        
        Args:
            parent: Parent widget
            text: Label text
            variable: StringVar or IntVar
            **kwargs: Additional CTkCheckBox arguments
        
        Returns:
            Configured CTkCheckBox
        """
        default_kwargs = {
            "text": text,
            "font": (UIConstants.FONT_FAMILY, 13),
            "variable": variable
        }
        default_kwargs.update(kwargs)
        return ctk.CTkCheckBox(parent, **default_kwargs)
    
    @staticmethod
    def create_combobox(parent, values: list, **kwargs) -> ctk.CTkComboBox:
        """
        Create combobox untuk recurrence type selection
        
        Args:
            parent: Parent widget
            values: List of options
            **kwargs: Additional CTkComboBox arguments
        
        Returns:
            Configured CTkComboBox
        """
        default_kwargs = {
            "values": values,
            "font": (UIConstants.FONT_FAMILY, 13),
            "height": 40
        }
        default_kwargs.update(kwargs)
        return ctk.CTkComboBox(parent, **default_kwargs)


class TransactionCard:

    def __init__(self, parent, node: TransactionNode, delete_callback, edit_callback=None):
        """
        Membuat transaction card
        
        Args:
            parent: Parent widget (usually scrollable frame)
            node: TransactionNode to display
            delete_callback: Function to call when delete is clicked
            edit_callback: Function to call when edit is clicked
        """
        self.node = node
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        
        # Main card frame
        self.card = UIComponents.create_card_frame(
            parent,
            corner_radius=10
        )
        self.card.pack(fill="x", pady=3)
        
        # Content container
        content = ctk.CTkFrame(self.card, fg_color="transparent")
        content.pack(fill="x", padx=15, pady=12)
        
        # Left side: Title & Category
        self._create_left_section(content)
        
        # Right side: Amount & Delete button
        self._create_right_section(content)
    
    def _create_left_section(self, parent):
        """Title dan kategori"""
        left_frame = ctk.CTkFrame(parent, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True)
        
        # Title
        title_label = ctk.CTkLabel(
            left_frame,
            text=self.node.title,
            font=(UIConstants.FONT_FAMILY, 14, "bold"),
            text_color=UIConstants.TEXT_PRIMARY,
            anchor="w"
        )
        title_label.pack(anchor="w")
        
        # Category
        category_label = ctk.CTkLabel(
            left_frame,
            text=self.node.category,
            font=UIConstants.FONT_TINY,
            text_color=UIConstants.TEXT_SECONDARY,
            anchor="w"
        )
        category_label.pack(anchor="w")
    
    def _create_right_section(self, parent):
        """Jumlah, tombol edit dan delete"""
        right_frame = ctk.CTkFrame(parent, fg_color="transparent")
        right_frame.pack(side="right")
        
        # Determine color and prefix
        color = (UIConstants.INCOME_COLOR if self.node.trans_type == "Income" 
                else UIConstants.EXPENSE_COLOR)
        prefix = "+" if self.node.trans_type == "Income" else "-"
        
        # Amount label
        amount_text = CurrencyHelper.format_amount(self.node.amount, prefix)
        amount_label = ctk.CTkLabel(
            right_frame,
            text=amount_text,
            font=(UIConstants.FONT_FAMILY, 14, "bold"),
            text_color=color
        )
        amount_label.pack()
        
        # Button frame
        button_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        button_frame.pack(pady=(3, 0))
        
        # Recurring badge
        if self.node.is_recurring:
            recurring_badge = ctk.CTkLabel(
                button_frame,
                text=f"🔄 {self.node.recurrence_type}",
                font=(UIConstants.FONT_FAMILY, 9),
                text_color=UIConstants.TEXT_SECONDARY
            )
            recurring_badge.pack(side="left", padx=2)
        
        # Edit button
        edit_btn = ctk.CTkButton(
            button_frame,
            text="✎",
            width=30,
            height=25,
            font=(UIConstants.FONT_FAMILY, 12),
            fg_color=UIConstants.BUTTON_PRIMARY,
            hover_color=UIConstants.BUTTON_PRIMARY_HOVER,
            command=lambda: self.edit_callback(self.node) if hasattr(self, 'edit_callback') else None
        )
        edit_btn.pack(side="left", padx=2)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            button_frame,
            text="✕",
            width=30,
            height=25,
            font=(UIConstants.FONT_FAMILY, 12),
            fg_color=UIConstants.BUTTON_DANGER,
            hover_color=UIConstants.BUTTON_DANGER_HOVER,
            command=lambda: self.delete_callback(self.node.trans_id)
        )
        delete_btn.pack(side="left", padx=2)
    
    def set_edit_callback(self, callback: Callable):
        """Set edit callback after initialization"""
        self.edit_callback = callback