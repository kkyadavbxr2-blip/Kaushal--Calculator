
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.core.window import Window
import ast
import operator

Window.clearcolor = (0.04, 0.03, 0.12, 1)

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

def solve(node):
    if isinstance(node, ast.Expression):
        return solve(node.body)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](solve(node.left), solve(node.right))
    raise ValueError("Invalid")

class Calculator(App):
    def build(self):
        self.expr = ""

        root = BoxLayout(
            orientation="vertical",
            padding=dp(14),
            spacing=dp(12)
        )

        # GREEN BOLD HEADING
        heading = Label(
            text="CREATE BY KAUSHAL",
            font_size=dp(22),
            bold=True,
            color=(0, 1, 0, 1),
            size_hint_y=None,
            height=dp(55)
        )
        root.add_widget(heading)

        # DISPLAY
        display_box = BoxLayout(
            padding=dp(12),
            size_hint_y=0.28
        )

        with display_box.canvas.before:
            Color(0.13, 0.09, 0.28, 1)
            display_box.bg = RoundedRectangle(
                pos=display_box.pos,
                size=display_box.size,
                radius=[dp(24)]
            )

        display_box.bind(
            pos=lambda w, p: setattr(w.bg, "pos", p),
            size=lambda w, s: setattr(w.bg, "size", s)
        )

        self.display = Label(
            text="0",
            font_size=dp(40),
            color=(0.4, 0.9, 1, 1),
            halign="right",
            valign="middle"
        )
        self.display.bind(
            size=lambda w, s: setattr(w, "text_size", s)
        )
        display_box.add_widget(self.display)
        root.add_widget(display_box)

        # BUTTONS
        grid = GridLayout(
            cols=4,
            spacing=dp(9),
            size_hint_y=0.72
        )

        keys = [
            ("AC", (0.85, 0.12, 0.30, 1)),
            ("DEL", (0.48, 0.18, 0.75, 1)),
            ("%", (0.48, 0.18, 0.75, 1)),
            ("÷", (0.08, 0.35, 0.85, 1)),

            ("7", (0.13, 0.11, 0.25, 1)),
            ("8", (0.13, 0.11, 0.25, 1)),
            ("9", (0.13, 0.11, 0.25, 1)),
            ("×", (0.08, 0.35, 0.85, 1)),

            ("4", (0.13, 0.11, 0.25, 1)),
            ("5", (0.13, 0.11, 0.25, 1)),
            ("6", (0.13, 0.11, 0.25, 1)),
            ("-", (0.08, 0.35, 0.85, 1)),

            ("1", (0.13, 0.11, 0.25, 1)),
            ("2", (0.13, 0.11, 0.25, 1)),
            ("3", (0.13, 0.11, 0.25, 1)),
            ("+", (0.08, 0.35, 0.85, 1)),

            ("±", (0.48, 0.18, 0.75, 1)),
            ("0", (0.13, 0.11, 0.25, 1)),
            (".", (0.13, 0.11, 0.25, 1)),
            ("=", (0.02, 0.65, 0.40, 1)),
        ]

        for text, color in keys:
            btn = Button(
                text=text,
                font_size=dp(23),
                bold=True,
                color=(1, 1, 1, 1),
                background_normal="",
                background_color=color
            )
            btn.bind(on_press=self.press)
            grid.add_widget(btn)

        root.add_widget(grid)
        return root

    def press(self, btn):
        key = btn.text

        if key == "AC":
            self.expr = ""
            self.display.text = "0"
            return

        if key == "DEL":
            self.expr = self.expr[:-1]
            self.display.text = self.expr or "0"
            return

        if key == "±":
            if self.expr:
                if self.expr.startswith("-"):
                    self.expr = self.expr[1:]
                else:
                    self.expr = "-" + self.expr
                self.display.text = self.expr
            return

        if key == "=":
            try:
                exp = self.expr.replace("×", "*").replace("÷", "/")
                result = solve(ast.parse(exp, mode="eval"))
                self.expr = str(result)
                self.display.text = self.expr
            except Exception:
                self.display.text = "Error"
                self.expr = ""
            return

        if key == "%":
            try:
                exp = self.expr.replace("×", "*").replace("÷", "/")
                result = solve(ast.parse(exp, mode="eval"))
                self.expr = str(result / 100)
                self.display.text = self.expr
            except Exception:
                self.display.text = "Error"
                self.expr = ""
            return

        if key in ("+", "-", "×", "÷"):
            if not self.expr and key != "-":
                return

        if key == ".":
            last = self.expr
            for op in ("+", "-", "×", "÷"):
                last = last.split(op)[-1]
            if "." in last:
                return

        self.expr += key
        self.display.text = self.expr

if __name__ == "__main__":
    Calculator().run()
