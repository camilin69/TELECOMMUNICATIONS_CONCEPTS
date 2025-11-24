import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Importar las clases de codificación
from differential_coding import DifferentialCoding
from manchester_coding import ManchesterCoding
from manchester_differential_coding import DifferentialManchesterCoding

class CodingInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Codificación Digital")
        self.root.geometry("1200x1000")
        
        # Instanciar codificadores
        self.differential_coder = DifferentialCoding()
        self.manchester_coder = ManchesterCoding()
        self.diff_manchester_coder = DifferentialManchesterCoding()
        
        self.current_canvas = None
        
        self.setup_ui()

    def __del__(self):
        # Limpiar figuras de matplotlib para evitar memory leaks
        if hasattr(self, 'figures'):
            for fig in self.figures:
                plt.close(fig)

    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Sistema de Codificación Digital", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Entrada de texto
        ttk.Label(main_frame, text="Mensaje:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.text_entry = ttk.Entry(main_frame, width=50, font=('Arial', 10))
        self.text_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.text_entry.insert(0, "Hola")
        
        # Combobox de técnicas de codificación
        ttk.Label(main_frame, text="Técnica de Codificación:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.technique_combo = ttk.Combobox(main_frame, values=[
            "Codificación Diferencial",
            "Codificación Manchester", 
            "Codificación Manchester Diferencial"
        ], state="readonly", font=('Arial', 10))
        self.technique_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.technique_combo.set("Codificación Diferencial")
        
        # Combobox de códigos banda base
        ttk.Label(main_frame, text="Código Banda Base:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.base_code_combo = ttk.Combobox(main_frame, values=[
            "Unipolar",
            "Polar", 
            "Bipolar"
        ], state="readonly", font=('Arial', 10))
        self.base_code_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.base_code_combo.set("Unipolar")
        
        # Botón de codificación
        self.encode_button = ttk.Button(main_frame, text="Codificar", command=self.encode_message)
        self.encode_button.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Frame para la gráfica
        self.plot_frame = ttk.Frame(main_frame)
        self.plot_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Configurar expansión
        main_frame.rowconfigure(5, weight=1)
        main_frame.columnconfigure(1, weight=1)
    
    def encode_message(self):
        message = self.text_entry.get()
        technique = self.technique_combo.get()
        base_code = self.base_code_combo.get()
        
        if not message:
            messagebox.showwarning("Advertencia", "Por favor ingrese un mensaje")
            return
        
        try:
            # Convertir mensaje a bits
            binary_message = ''.join(format(ord(c), '08b') for c in message)
            original_bits = [int(bit) for bit in binary_message]
            
            # Seleccionar codificador según la técnica
            if technique == "Codificación Diferencial":
                coder = self.differential_coder
                technique_name = "Diferencial"
            elif technique == "Codificación Manchester":
                coder = self.manchester_coder
                technique_name = "Manchester"
            else:  # Manchester Diferencial
                coder = self.diff_manchester_coder
                technique_name = "Manchester Diferencial"
            
            # Codificar
            encoded_bits = coder.coding(message)
            
            # Decodificar
            decoded_bits = coder.decoding(encoded_bits)
            
            # Verificar que la decodificación sea correcta
            if original_bits != decoded_bits:
                print("Advertencia: La decodificación podría tener errores")
            
            # Mostrar información en consola
            print(f"\n=== {technique_name} - {base_code} ===")
            print(f"Mensaje original: {message}")
            print(f"Bits originales: {''.join(map(str, original_bits))}")
            print(f"Bits codificados: {''.join(map(str, encoded_bits))}")
            print(f"Bits decodificados: {''.join(map(str, decoded_bits))}")
            print(f"Decodificación correcta: {original_bits == decoded_bits}")
            
            # Generar gráficas específicas según el código banda base seleccionado
            self.display_plots(original_bits, encoded_bits, decoded_bits, technique_name, base_code)
            
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def display_plots(self, original_bits, encoded_bits, decoded_bits, technique_name, base_code):
        # Limpiar frame anterior
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Crear una sola figura con 4 subplots verticales
        fig, axes = plt.subplots(4, 1, figsize=(12, 8))  # Altura reducida
        fig.suptitle(f'Codificación {technique_name} - Código {base_code}', 
                    fontsize=14, fontweight='bold', y=0.98)
        
        # Gráfica 1: Señal Original
        if base_code == "Unipolar":
            self._plot_unipolar_signal(axes[0], original_bits, f"Señal Original - {base_code}")
        elif base_code == "Polar":
            self._plot_polar_signal(axes[0], original_bits, f"Señal Original - {base_code}")
        else:  # Bipolar
            self._plot_bipolar_signal(axes[0], original_bits, f"Señal Original - {base_code}")
        
        # Gráfica 2: Muestreo
        self._plot_sampling(axes[1], original_bits, "Muestreo (t/2)")
        
        # Gráfica 3: Señal Codificada
        self._plot_encoded_signal(axes[2], encoded_bits, f"Señal Codificada - {technique_name}", technique_name)
        
        # Gráfica 4: Señal Decodificada
        if base_code == "Unipolar":
            self._plot_unipolar_signal(axes[3], decoded_bits, f"Señal Decodificada - {base_code}")
        elif base_code == "Polar":
            self._plot_polar_signal(axes[3], decoded_bits, f"Señal Decodificada - {base_code}")
        else:  # Bipolar
            self._plot_bipolar_signal(axes[3], decoded_bits, f"Señal Decodificada - {base_code}")
        
        # Ajustar espaciado entre subplots
        plt.tight_layout(pad=2.0, h_pad=1.5, w_pad=1.0, rect=[0, 0, 1, 0.96])
        
        # Integrar matplotlib con tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Guardar referencia
        self.current_canvas = canvas
        self.current_figure = fig
    
    def _plot_unipolar_signal(self, ax, bits, title):
        """Gráfica unipolar (0V, 5V)"""
        t = np.arange(len(bits))
        signal = np.array(bits) * 5
        
        ax.step(t, signal, where='post', linewidth=2, color='blue')
        ax.set_title(title, fontweight='bold', fontsize=12, pad=10)
        ax.set_xlabel('Tiempo (bits)', fontsize=10)
        ax.set_ylabel('Voltaje (V)', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-1, 6)
        ax.set_xlim(0, len(bits))
        
        ax.set_yticks([0, 5])
        ax.set_yticklabels(['0V', '5V'], fontsize=9)
        ax.tick_params(axis='x', labelsize=9)
        
        for i, bit in enumerate(bits):
            ax.text(i + 0.5, 2.5, str(bit), ha='center', va='center', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                fontsize=9)

    def _plot_polar_signal(self, ax, bits, title):
        """Gráfica polar (-5V, +5V)"""
        t = np.arange(len(bits))
        signal = np.array(bits) * 10 - 5
        
        ax.step(t, signal, where='post', linewidth=2, color='red')
        ax.set_title(title, fontweight='bold', fontsize=12, pad=10)
        ax.set_xlabel('Tiempo (bits)', fontsize=10)
        ax.set_ylabel('Voltaje (V)', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-6, 6)
        ax.set_xlim(0, len(bits))
        
        ax.set_yticks([-5, 5])
        ax.set_yticklabels(['-5V', '+5V'], fontsize=9)
        ax.tick_params(axis='x', labelsize=9)
        
        for i, bit in enumerate(bits):
            ax.text(i + 0.5, 0, str(bit), ha='center', va='center', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                fontsize=9)

    def _plot_bipolar_signal(self, ax, bits, title):
        """Gráfica bipolar (-5V, 0V, +5V)"""
        t = np.arange(len(bits))
        signal = []
        last_positive = True
        
        for bit in bits:
            if bit == 0:
                signal.append(0)
            else:
                if last_positive:
                    signal.append(-5)
                else:
                    signal.append(5)
                last_positive = not last_positive
        
        ax.step(t, signal, where='post', linewidth=2, color='green')
        ax.set_title(title, fontweight='bold', fontsize=12, pad=10)
        ax.set_xlabel('Tiempo (bits)', fontsize=10)
        ax.set_ylabel('Voltaje (V)', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-6, 6)
        ax.set_xlim(0, len(bits))
        
        ax.set_yticks([-5, 0, 5])
        ax.set_yticklabels(['-5V', '0V', '+5V'], fontsize=9)
        ax.tick_params(axis='x', labelsize=9)
        
        for i, bit in enumerate(bits):
            ax.text(i + 0.5, 0, str(bit), ha='center', va='center', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8),
                fontsize=9)

    def _plot_sampling(self, ax, bits, title):
        """Gráfica de muestreo con flechas en t/2"""
        t = np.arange(len(bits))
        signal = np.array(bits) * 5
        
        t_detailed = np.linspace(0, len(bits), len(bits) * 10)
        signal_detailed = np.repeat(signal, 10)
        
        ax.plot(t_detailed, signal_detailed, 'b-', alpha=0.7, linewidth=1)
        ax.step(t, signal, where='post', linewidth=2, color='blue')
        
        for i in range(len(bits)):
            sample_time = i + 0.5
            sample_value = signal[i]
            
            ax.annotate('', xy=(sample_time, sample_value), 
                    xytext=(sample_time, sample_value + 2),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
            
            ax.plot(sample_time, sample_value, 'ro', markersize=6)
            ax.text(sample_time, sample_value + 2.5, f'Bit: {bits[i]}', 
                ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        ax.set_title(title, fontweight='bold', fontsize=12, pad=10)
        ax.set_xlabel('Tiempo (bits)', fontsize=10)
        ax.set_ylabel('Voltaje (V)', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-1, 8)
        ax.set_xlim(0, len(bits))
        ax.tick_params(axis='both', labelsize=9)
    
    def _plot_encoded_signal(self, ax, encoded_bits, title, technique_name):
        """Gráfica del mensaje codificado"""
        
        if "Diferencial" in technique_name and "Manchester" not in technique_name:
            # Para codificación diferencial - mostrar transiciones en t/2
            t_detailed = []
            signal_detailed = []
            
            for i in range(len(encoded_bits)):
                # Cada bit ocupa 1 unidad de tiempo
                t_start = i
                t_mid = i + 0.5  # Punto de transición en t/2
                t_end = i + 1
                
                if i == 0:
                    # Primer bit - empezar desde el nivel
                    t_detailed.extend([t_start, t_mid - 0.001])
                    signal_detailed.extend([encoded_bits[i] * 5] * 2)
                else:
                    # Verificar si hay transición con el bit anterior
                    if encoded_bits[i] != encoded_bits[i-1]:
                        # Hay transición - mostrar cambio abrupto en t/2
                        t_detailed.extend([t_start, t_mid - 0.001])
                        signal_detailed.extend([encoded_bits[i-1] * 5] * 2)
                        t_detailed.extend([t_mid, t_mid])
                        signal_detailed.extend([encoded_bits[i-1] * 5, encoded_bits[i] * 5])
                    else:
                        # Sin transición - continuar nivel
                        t_detailed.extend([t_start, t_mid - 0.001])
                        signal_detailed.extend([encoded_bits[i] * 5] * 2)
                
                # Segunda mitad del bit (después de t/2)
                t_detailed.extend([t_mid + 0.001, t_end - 0.001])
                signal_detailed.extend([encoded_bits[i] * 5] * 2)
            
            ax.plot(t_detailed, signal_detailed, 'purple', linewidth=2)
            
            # Marcar puntos de muestreo en t/2
            for i in range(len(encoded_bits)):
                t_sample = i + 0.5
                sample_value = encoded_bits[i] * 5
                ax.plot(t_sample, sample_value, 'ro', markersize=6, label='Muestreo' if i == 0 else "")
                
                # Flecha indicando muestreo
                ax.annotate('', xy=(t_sample, sample_value), 
                        xytext=(t_sample, sample_value + 1.5),
                        arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
                
                # Mostrar el valor del bit codificado
                ax.text(t_sample, sample_value - 0.8, str(encoded_bits[i]), 
                    ha='center', va='top', fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
            
            if len(encoded_bits) > 0:
                ax.legend()
            ax.set_xlim(0, len(encoded_bits))
            
        elif "Manchester Diferencial" in technique_name:
            # Para Manchester Diferencial - mostrar transiciones correctas
            t_detailed = []
            signal_detailed = []
            
            # Cada bit original se convierte en 2 bits codificados
            for i in range(0, len(encoded_bits), 2):
                bit_index = i // 2
                t_start = bit_index
                t_mid = bit_index + 0.5  # Transición en t/2
                t_end = bit_index + 1
                
                if i < len(encoded_bits) - 1:
                    first_half = encoded_bits[i] * 5
                    second_half = encoded_bits[i+1] * 5
                    
                    # Primera mitad del bit (antes de t/2)
                    t_detailed.extend([t_start, t_mid - 0.001])
                    signal_detailed.extend([first_half, first_half])
                    
                    # Transición en t/2
                    t_detailed.extend([t_mid, t_mid])
                    signal_detailed.extend([first_half, second_half])
                    
                    # Segunda mitad del bit (después de t/2)
                    t_detailed.extend([t_mid + 0.001, t_end - 0.001])
                    signal_detailed.extend([second_half, second_half])
            
            ax.plot(t_detailed, signal_detailed, 'purple', linewidth=2)
            
            # Marcar puntos de muestreo y transiciones
            for i in range(0, len(encoded_bits), 2):
                bit_index = i // 2
                t_sample = bit_index + 0.5
                sample_value = encoded_bits[i+1] * 5  # Muestreo en segunda mitad
                
                ax.plot(t_sample, sample_value, 'ro', markersize=6, label='Muestreo' if i == 0 else "")
                
                # Mostrar el bit decodificado
                if i < len(encoded_bits) - 1:
                    decoded_bit = 0 if encoded_bits[i] != encoded_bits[i+1] else 1
                    ax.text(t_sample, sample_value - 0.8, f'Bit: {decoded_bit}', 
                        ha='center', va='top', fontweight='bold',
                        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))
            
            if len(encoded_bits) > 0:
                ax.legend()
            ax.set_xlim(0, len(encoded_bits) // 2)
            
        elif "Manchester" in technique_name:
            # Para Manchester normal
            t_detailed = []
            signal_detailed = []
            
            for i in range(len(encoded_bits)):
                t_start = i * 0.5
                t_mid = i * 0.5 + 0.25
                t_end = (i + 1) * 0.5
                
                t_detailed.extend([t_start, t_mid, t_end - 0.001])
                signal_detailed.extend([encoded_bits[i] * 5] * 3)
                
                if i < len(encoded_bits) - 1 and encoded_bits[i] != encoded_bits[i + 1]:
                    t_detailed.append(t_end)
                    signal_detailed.append(encoded_bits[i + 1] * 5)
            
            ax.plot(t_detailed, signal_detailed, 'purple', linewidth=2)
            ax.set_xlim(0, len(encoded_bits) * 0.5)
            
        else:
            # Para otras codificaciones
            t = np.arange(len(encoded_bits))
            signal = np.array(encoded_bits) * 5
            ax.step(t, signal, where='post', linewidth=2, color='purple')
            ax.set_xlim(0, len(encoded_bits))
        
        ax.set_title(title, fontweight='bold', fontsize=12, pad=10)
        ax.set_xlabel('Tiempo (períodos de bit)', fontsize=10)
        ax.set_ylabel('Voltaje (V)', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(-1, 6)
        ax.tick_params(axis='both', labelsize=9)


def main():
    root = tk.Tk()
    app = CodingInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()