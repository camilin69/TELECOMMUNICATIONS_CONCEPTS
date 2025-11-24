import numpy as np
import matplotlib.pyplot as plt

class DifferentialCoding:
    def __init__(self):
        self.initial_state = 0  # Estado inicial conocido
    
    def coding(self, message):
        """
        Codificación diferencial: 
        - Bit 1: cambio en t=0 (inicio del bit)
        - Bit 0: sin cambio
        """
        if isinstance(message, str):
            # Convertir string a lista de bits
            binary_message = ''.join(format(ord(c), '08b') for c in message)
            bits = [int(bit) for bit in binary_message]
        else:
            bits = message
        
        encoded_bits = []
        current_level = self.initial_state
        
        for bit in bits:
            if bit == 1:
                # Cambio de nivel al inicio del bit
                current_level = 1 - current_level
            # El nivel se mantiene durante todo el bit
            encoded_bits.append(current_level)
        
        return encoded_bits
    
    def decoding(self, encoded_bits):
        """
        Decodificación diferencial:
        - Se compara el nivel actual con el nivel anterior
        - Cambio de nivel: bit 1
        - Mismo nivel: bit 0
        """
        decoded_bits = []
        previous_level = self.initial_state  # Usar el mismo estado inicial
        
        for current_level in encoded_bits:
            # Comparar nivel actual con nivel anterior (muestreo en t/2)
            if current_level != previous_level:
                decoded_bits.append(1)  # Hubo cambio - bit 1
            else:
                decoded_bits.append(0)  # No hubo cambio - bit 0
            previous_level = current_level
        
        return decoded_bits
    
    def get_detailed_signal(self, message):
        """
        Retorna la señal detallada para visualización
        Muestra transiciones al inicio de cada bit
        """
        encoded_bits = self.coding(message)
        
        t_detailed = []
        signal_detailed = []
        
        for i, level in enumerate(encoded_bits):
            # Cada bit ocupa 1 unidad de tiempo
            t_start = i
            t_mid = i + 0.5  # Punto de muestreo
            t_end = i + 1
            
            # Puntos para la señal detallada
            t_detailed.extend([t_start, t_mid - 0.001, t_mid, t_end - 0.001])
            signal_detailed.extend([level * 5] * 4)
        
        return t_detailed, signal_detailed, encoded_bits
    
    def explain_coding(self, message):
        """Explica el proceso de codificación paso a paso"""
        if isinstance(message, str):
            binary_message = ''.join(format(ord(c), '08b') for c in message)
            bits = [int(bit) for bit in binary_message]
        else:
            bits = message
        
        print("=== EXPLICACIÓN CODIFICACIÓN DIFERENCIAL ===")
        print(f"Bits originales: {''.join(map(str, bits))}")
        print(f"Estado inicial: {self.initial_state}")
        
        encoded_bits = []
        current_level = self.initial_state
        
        for i, bit in enumerate(bits):
            previous_level = current_level
            if bit == 1:
                current_level = 1 - current_level
                change = "CAMBIO"
            else:
                change = "MANTIENE"
            encoded_bits.append(current_level)
            print(f"Bit {i}: {bit} -> {change} -> Nivel: {current_level} (Anterior: {previous_level})")
        
        print(f"Bits codificados: {''.join(map(str, encoded_bits))}")
        return encoded_bits
    
    def explain_decoding(self, encoded_bits):
        """Explica el proceso de decodificación paso a paso"""
        print("=== EXPLICACIÓN DECODIFICACIÓN DIFERENCIAL ===")
        print(f"Bits codificados: {''.join(map(str, encoded_bits))}")
        print(f"Estado inicial: {self.initial_state}")
        
        decoded_bits = []
        previous_level = self.initial_state
        
        for i, current_level in enumerate(encoded_bits):
            if current_level != previous_level:
                decoded_bit = 1
                change = "CAMBIO DETECTADO"
            else:
                decoded_bit = 0
                change = "SIN CAMBIO"
            decoded_bits.append(decoded_bit)
            print(f"Muestra {i}: Nivel {current_level} vs Anterior {previous_level} -> {change} -> Bit: {decoded_bit}")
            previous_level = current_level
        
        print(f"Bits decodificados: {''.join(map(str, decoded_bits))}")
        return decoded_bits
    
    def bits_to_string(self, bits):
        """Convierte lista de bits a string"""
        bytes_list = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) == 8:
                char_code = int(''.join(map(str, byte)), 2)
                bytes_list.append(char_code)
        
        return ''.join(chr(byte) for byte in bytes_list)