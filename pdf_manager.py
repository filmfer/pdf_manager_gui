import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import sys
from pathlib import Path

from pypdf import PdfWriter, PdfReader
from PIL import Image, ImageOps
import fitz  # PyMuPDF

# --- UI palette -------------------------------------------------------------
BG_COLOR = "#f0f0f0"
ACCENT = "#0078d4"
ACCENT_HOVER = "#005a9e"
FOOTER_COLOR = "#8a8a8a"

# Widely available, license-free raster image formats (lowercase extension).
# These are the formats Pillow (PIL) can open without extra dependencies.
IMAGE_EXTENSIONS = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".jpe": "JPEG",
    ".jfif": "JPEG",
    ".gif": "GIF",
    ".bmp": "BMP",
    ".dib": "BMP",
    ".tif": "TIFF",
    ".tiff": "TIFF",
    ".webp": "WEBP",
    ".ico": "ICO",
    ".ppm": "PPM",
    ".pgm": "PGM",
    ".pbm": "PBM",
    ".pcx": "PCX",
    ".tga": "TGA",
    ".sgi": "SGI",
    ".xbm": "XBM",
    ".xpm": "XPM",
    ".qoi": "QOI",
}

# Output raster formats supported by Pillow/PyMuPDF when exporting PDF pages.
EXPORT_IMAGE_EXTENSIONS = {
    ".png": "PNG",
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".webp": "WEBP",
    ".tif": "TIFF",
    ".tiff": "TIFF",
    ".bmp": "BMP",
    ".ppm": "PPM",
    ".pgm": "PGM",
    ".pbm": "PBM",
}

IMAGE_FILE_TYPES = [
    (
        "All supported image files",
        "*.png *.jpg *.jpeg *.jpe *.jfif *.gif *.bmp *.dib *.tif *.tiff "
        "*.webp *.ico *.ppm *.pgm *.pbm *.pcx *.tga *.sgi *.xbm *.xpm *.qoi",
    ),
    ("All files", "*.*"),
]

EXPORT_FILE_TYPES = [
    ("PNG image", "*.png"),
    ("JPEG image", "*.jpg *.jpeg"),
    ("WEBP image", "*.webp"),
    ("TIFF image", "*.tif *.tiff"),
    ("BMP image", "*.bmp"),
    ("PPM/PGM/PBM image", "*.ppm *.pgm *.pbm"),
    ("All files", "*.*"),
]

# --- Application metadata ---
APP_NAME = "simple PDF Manager"
AUTHOR = "Filipe Fernandes"
AUTHOR_EMAIL = "filmfer@gmail.com"

class PDFManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("560x520")
        self.root.minsize(460, 400)
        self.root.configure(bg=BG_COLOR)

        # --- Set window icon ---
        def get_resource_path(relative_path):
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        icon_path = get_resource_path("simple_pdf_manager.ico")
        if os.path.exists(icon_path) and sys.platform != "darwin":
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass

        style = ttk.Style()
        style.theme_use("clam")

        # --- Header (centered title, no buttons) ---
        header = tk.Frame(root, bg=ACCENT)
        header.pack(fill=tk.X)
        tk.Label(
            header, text=APP_NAME, font=("Arial", 16, "bold"),
            bg=ACCENT, fg="white",
        ).pack(fill=tk.X, pady=(12, 0))
        tk.Label(
            header, text="Merge  Extract  Remove  Split  Images <-> PDF",
            font=("Arial", 9), bg=ACCENT, fg="white",
        ).pack(fill=tk.X, padx=16, pady=(0, 8))

        # --- Content (no scrollbar needed) ---
        self.content = ttk.Frame(root)
        self.content.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 4))

        buttons = [
            ("Merge PDFs", self.merge_pdfs),
            ("Extract Pages", self.extract_pages),
            ("Remove Pages", self.remove_pages),
            ("Split PDF 1 page per file", self.split_pdf),
            ("Create PDF from Images", self.images_to_pdf),
            ("Export Pages to Images", self.pdf_to_images),
        ]
        for text, command in buttons:
            self._create_button(self.content, text, command)

        # --- Footer ---
        tk.Label(
            root,
            text=f"© 2026 {AUTHOR}  |  {AUTHOR_EMAIL}  |  Python 3 + Tkinter",
            font=("Arial", 8), fg=FOOTER_COLOR, bg=BG_COLOR,
        ).pack(side=tk.BOTTOM, fill=tk.X, pady=2)

    @staticmethod
    def _create_button(parent, text, command):
        btn = tk.Button(
            parent, text=text, command=command,
            font=("Arial", 11, "bold"), bg=ACCENT, fg="white",
            height=2, cursor="hand2", relief=tk.RAISED, bd=2,
            activebackground=ACCENT_HOVER, activeforeground="white",
        )
        btn.pack(fill=tk.X, pady=8)

        def on_enter(_event):
            btn.config(bg=ACCENT_HOVER)

        def on_leave(_event):
            btn.config(bg=ACCENT)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    @staticmethod
    def _centre(dialog):
        """Center a dialog on the screen, sized to fit its content."""
        dialog.update_idletasks()
        w = max(dialog.winfo_reqwidth(), 320)
        h = dialog.winfo_reqheight()
        sw = dialog.winfo_screenwidth()
        sh = dialog.winfo_screenheight()
        x = max((sw - w) // 2, 0)
        y = max((sh - h) // 3, 0)
        dialog.geometry(f"{w}x{h}+{x}+{y}")

    def merge_pdfs(self):
        """Merge two or more PDFs into a single document."""
        files = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
        )
        if not files:
            return
        if len(files) < 2:
            messagebox.showwarning(
                "Not enough files",
                "Please select at least 2 PDF files.",
                parent=self.root,
            )
            return

        output_file = filedialog.asksaveasfilename(
            title="Save merged PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not output_file:
            return
        if not output_file.lower().endswith(".pdf"):
            output_file += ".pdf"

        try:
            pdf_writer = PdfWriter()
            for file_path in files:
                pdf_reader = PdfReader(file_path)
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)
            with open(output_file, "wb") as f:
                pdf_writer.write(f)
            messagebox.showinfo(
                "Success",
                f"PDFs merged successfully!\nSaved to: {output_file}",
                parent=self.root,
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}", parent=self.root)

    def extract_pages(self):
        """Extract a page range from a PDF into a new document."""
        input_file = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not input_file:
            return

        try:
            reader = PdfReader(input_file)
            num_pages = len(reader.pages)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read PDF:\n{e}", parent=self.root)
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Extract Pages")
        dialog.configure(bg=BG_COLOR)
        dialog.transient(self.root)
        dialog.resizable(False, False)

        start_var = tk.IntVar(value=1)
        end_var = tk.IntVar(value=num_pages)

        body = tk.Frame(dialog, bg=BG_COLOR)
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        tk.Label(body, text="Start page:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", pady=4)
        tk.Spinbox(body, from_=1, to=num_pages, textvariable=start_var, width=8).grid(
            row=0, column=1, sticky="w", pady=4
        )
        tk.Label(body, text="End page:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", pady=4)
        tk.Spinbox(body, from_=1, to=num_pages, textvariable=end_var, width=8).grid(
            row=1, column=1, sticky="w", pady=4
        )
        tk.Label(
            body, text=f"PDF has {num_pages} page(s).", bg=BG_COLOR, fg=FOOTER_COLOR
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

        def extract():
            start = start_var.get()
            end = end_var.get()
            if not (1 <= start <= end <= num_pages):
                messagebox.showerror(
                    "Error",
                    f"Invalid range. Choose between 1 and {num_pages}.",
                    parent=dialog,
                )
                return

            output_file = filedialog.asksaveasfilename(
                title="Save extracted pages as",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
            )
            if not output_file:
                return
            if not output_file.lower().endswith(".pdf"):
                output_file += ".pdf"

            try:
                pdf_writer = PdfWriter()
                for i in range(start - 1, end):
                    pdf_writer.add_page(reader.pages[i])
                with open(output_file, "wb") as f:
                    pdf_writer.write(f)
                messagebox.showinfo(
                    "Success",
                    f"Pages extracted successfully!\nSaved to: {output_file}",
                    parent=dialog,
                )
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to extract pages:\n{e}", parent=dialog)

        tk.Button(
            body, text="Extract", command=extract, bg=ACCENT, fg="white",
            relief=tk.RAISED, bd=2, activebackground=ACCENT_HOVER,
        ).grid(row=3, column=0, columnspan=2, pady=(12, 0), sticky="we")

        self._centre(dialog)
        dialog.grab_set()

    def remove_pages(self):
        """Remove pages from a PDF and save the result."""
        input_file = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not input_file:
            return

        try:
            reader = PdfReader(input_file)
            total_pages = len(reader.pages)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read PDF:\n{e}", parent=self.root)
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Remove Pages")
        dialog.configure(bg=BG_COLOR)
        dialog.transient(self.root)
        dialog.resizable(False, False)

        tk.Label(
            dialog, bg=BG_COLOR,
            text="Pages to remove (comma-separated, e.g., 1,3,5):",
            wraplength=320, justify="left",
        ).pack(pady=(8, 4))
        pages_entry = tk.Entry(dialog, width=20)
        pages_entry.pack(pady=4)
        tk.Label(
            dialog, bg=BG_COLOR, fg=FOOTER_COLOR,
            text=f"PDF has {total_pages} page(s).",
        ).pack(pady=2)

        def remove():
            pages_str = pages_entry.get().strip()
            if not pages_str:
                messagebox.showerror("Error", "Please enter page numbers.", parent=dialog)
                return

            try:
                pages_to_remove = [int(p.strip()) for p in pages_str.split(",")]
            except ValueError:
                messagebox.showerror(
                    "Error", "Invalid page numbers. Use comma-separated integers.", parent=dialog
                )
                return

            for page_num in pages_to_remove:
                if page_num < 1 or page_num > total_pages:
                    messagebox.showerror(
                        "Error",
                        f"Page {page_num} is out of range (PDF has {total_pages} pages).",
                        parent=dialog,
                    )
                    return

            output_file = filedialog.asksaveasfilename(
                title="Save modified PDF as",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
            )
            if not output_file:
                return
            if not output_file.lower().endswith(".pdf"):
                output_file += ".pdf"

            try:
                pdf_writer = PdfWriter()
                for i, page in enumerate(reader.pages, 1):
                    if i not in pages_to_remove:
                        pdf_writer.add_page(page)
                with open(output_file, "wb") as f:
                    pdf_writer.write(f)

                messagebox.showinfo(
                    "Success",
                    f"Pages removed successfully!\nSaved to: {output_file}",
                    parent=dialog,
                )
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove pages:\n{e}", parent=dialog)

        tk.Button(
            dialog, text="Remove", command=remove,
            bg=ACCENT, fg="white", relief=tk.RAISED, bd=2, activebackground=ACCENT_HOVER,
        ).pack(pady=10)

        self._centre(dialog)
        dialog.grab_set()

    def split_pdf(self):
        """Split a PDF into single-page files."""
        input_file = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not input_file:
            return

        output_dir = filedialog.askdirectory(title="Select output directory")
        if not output_dir:
            return

        try:
            pdf_reader = PdfReader(input_file)
            base_name = Path(input_file).stem

            for i, page in enumerate(pdf_reader.pages, 1):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page)
                output_path = os.path.join(output_dir, f"{base_name}_page_{i}.pdf")
                with open(output_path, "wb") as f:
                    pdf_writer.write(f)

            messagebox.showinfo(
                "Success",
                f"PDF split successfully!\n{len(pdf_reader.pages)} files created in:\n{output_dir}",
                parent=self.root,
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to split PDF:\n{e}", parent=self.root)

    def images_to_pdf(self):
        """Create a PDF from selected images or from all images in a folder."""
        use_folder = messagebox.askyesno(
            "Create PDF from Images",
            "Use all images in a folder?\n\n"
            "Yes = select a folder and use every supported image inside it\n"
            "No  = pick the image files individually",
            parent=self.root,
        )

        if use_folder:
            folder = filedialog.askdirectory(title="Select folder with images")
            if not folder:
                return
            images = []
            for name in sorted(os.listdir(folder)):
                ext = os.path.splitext(name)[1].lower()
                if ext in IMAGE_EXTENSIONS:
                    images.append(os.path.join(folder, name))
            if not images:
                messagebox.showwarning(
                    "No images found",
                    "No supported images were found in the selected folder.",
                    parent=self.root,
                )
                return
        else:
            files = filedialog.askopenfilenames(
                title="Select images (Ctrl+click for multiple)",
                filetypes=IMAGE_FILE_TYPES,
            )
            if not files:
                return
            images = list(files)

        output_file = filedialog.asksaveasfilename(
            title="Save PDF as",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not output_file:
            return
        if not output_file.lower().endswith(".pdf"):
            output_file += ".pdf"

        # Open every image, apply EXIF orientation and normalize the color mode.
        prepared = []
        failures = []
        for path in images:
            try:
                with Image.open(path) as img:
                    img = ImageOps.exif_transpose(img)
                    # Keep an independent in-memory copy so the file can be closed.
                    if img.mode not in ("RGB", "L"):
                        img = img.convert("RGB")
                    prepared.append(img.copy())
            except Exception:
                failures.append(os.path.basename(path))

        if not prepared:
            messagebox.showerror(
                "Error",
                "None of the selected images could be read.",
                parent=self.root,
            )
            return

        try:
            first, rest = prepared[0], prepared[1:]
            first.save(output_file, "PDF", save_all=True, append_images=rest, resolution=96.0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create PDF:\n{e}", parent=self.root)
            return

        msg = (
            f"Created PDF successfully!\n"
            f"{len(prepared)} image(s) saved to:\n{output_file}"
        )
        if failures:
            msg += f"\n\nSkipped {len(failures)} unreadable file(s):\n" + ", ".join(failures[:10])
        messagebox.showinfo("Success", msg, parent=self.root)

    def pdf_to_images(self):
        """Export one or more PDF pages to raster images."""
        input_file = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF Files", "*.pdf")],
        )
        if not input_file:
            return

        try:
            doc = fitz.open(input_file)
            num_pages = doc.page_count
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read PDF:\n{e}", parent=self.root)
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Export Pages to Images")
        dialog.configure(bg=BG_COLOR)
        dialog.transient(self.root)
        dialog.resizable(False, False)

        start_var = tk.IntVar(value=1)
        end_var = tk.IntVar(value=num_pages)
        dpi_var = tk.IntVar(value=150)
        format_var = tk.StringVar(value=".png")

        body = tk.Frame(dialog, bg=BG_COLOR)
        body.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
        body.grid_columnconfigure(1, weight=1)

        tk.Label(body, text="Start page:", bg=BG_COLOR).grid(row=0, column=0, sticky="w", pady=4)
        tk.Spinbox(body, from_=1, to=num_pages, textvariable=start_var, width=8).grid(
            row=0, column=1, sticky="w", pady=4
        )
        tk.Label(body, text="End page:", bg=BG_COLOR).grid(row=1, column=0, sticky="w", pady=4)
        tk.Spinbox(body, from_=1, to=num_pages, textvariable=end_var, width=8).grid(
            row=1, column=1, sticky="w", pady=4
        )
        tk.Label(body, text="Resolution (DPI):", bg=BG_COLOR).grid(row=2, column=0, sticky="w", pady=4)
        tk.Spinbox(body, from_=50, to=600, increment=50, textvariable=dpi_var, width=8).grid(
            row=2, column=1, sticky="w", pady=4
        )
        tk.Label(body, text="Image format:", bg=BG_COLOR).grid(row=3, column=0, sticky="w", pady=4)
        ttk.Combobox(
            body, textvariable=format_var, state="readonly",
            values=list(EXPORT_IMAGE_EXTENSIONS.keys()),
        ).grid(row=3, column=1, sticky="we", pady=4)
        tk.Label(
            body, text=f"PDF has {num_pages} page(s).", bg=BG_COLOR, fg=FOOTER_COLOR
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 0))

        def export():
            start = start_var.get()
            end = end_var.get()
            if not (1 <= start <= end <= num_pages):
                messagebox.showerror(
                    "Error",
                    f"Invalid range. Choose between 1 and {num_pages}.",
                    parent=dialog,
                )
                return
            dpi = min(max(dpi_var.get(), 50), 600)
            fmt = format_var.get().strip().lower()

            output_dir = filedialog.askdirectory(title="Select output folder")
            if not output_dir:
                return

            base = Path(input_file).stem
            width = len(str(end))
            count = 0
            try:
                for page_num in range(start, end + 1):
                    page = doc[page_num - 1]
                    pix = page.get_pixmap(dpi=dpi, alpha=False)
                    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                    name = f"{base}_page_{str(page_num).zfill(max(width, 2))}{fmt}"
                    img.save(os.path.join(output_dir, name), format=EXPORT_IMAGE_EXTENSIONS[fmt])
                    count += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export pages:\n{e}", parent=dialog)
                return

            messagebox.showinfo(
                "Success",
                f"Exported {count} page(s) to:\n{output_dir}",
                parent=dialog,
            )
            dialog.destroy()

        tk.Button(
            body, text="Export", command=export, bg=ACCENT, fg="white",
            relief=tk.RAISED, bd=2, activebackground=ACCENT_HOVER,
        ).grid(row=5, column=0, columnspan=2, pady=(12, 0), sticky="we")

        self._centre(dialog)
        dialog.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFManagerApp(root)
    root.mainloop()

