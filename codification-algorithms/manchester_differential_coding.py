import numpy as np
import matplotlib.pyplot as plt

class DifferentialManchesterCoding:
    def __init__(self):
        self.initial_state = 0  # Siempre empezar desde 0V
    
    def coding(self, message):
        """
        Codificación Manchester Diferencial CORREGIDA:
        - Bit 0: transición AL INICIO del bit
        - Bit 1: SIN transición al inicio del bit
        - SIEMPRE transición a la MITAD del bit
        """
        if isinstance(message, str):
            binary_message = ''.join(format(ord(c), '08b') for c in message)
            bits = [int(bit) for bit in binary_message]
        else:
            bits = message
        
        encoded_bits = []
        current_level = self.initial_state  # Siempre empezar desde 0
        
        for bit in bits:
            if bit == 0:
                # BIT 0: Transición AL INICIO del bit
                current_level = 1 - current_level
            
            # Primera mitad del bit (antes de t/2)
            encoded_bits.append(current_level)
            
            # SIEMPRE transición a la MITAD del bit (para ambos bits 0 y 1)
            current_level = 1 - current_level
            
            # Segunda mitad del bit (después de t/2)
            encoded_bits.append(current_level)
        
        return encoded_bits
    
    def decoding(self, encoded_bits):
        """
        Decodificación Manchester Diferencial CORREGIDA:
        - Se compara el nivel de la primera mitad con el nivel anterior
        - Si son diferentes: Bit 0 (hubo transición al inicio)
        - Si son iguales: Bit 1 (no hubo transición al inicio)
        """
        if len(encoded_bits) % 2 != 0:
            raise ValueError("La longitud de bits codificados debe ser par")
        
        decoded_bits = []
        previous_second_half = self.initial_state  # Mismo estado inicial que la codificación
        
        for i in range(0, len(encoded_bits), 2):
            first_half = encoded_bits[i]      # Nivel en primera mitad del bit actual
            second_half = encoded_bits[i+1]   # Nivel en segunda mitad del bit actual
            
            # Comparar primera mitad del bit actual con segunda mitad del bit anterior
            if first_half != previous_second_half:
                # Hubo transición al inicio: Bit 0
                decoded_bits.append(0)
            else:
                # No hubo transición al inicio: Bit 1
                decoded_bits.append(1)
            
            previous_second_half = second_half
        
        return decoded_bits
    
    def debug_coding_decoding(self, message):
        """Método para debuggear el proceso completo"""
        if isinstance(message, str):
            binary_message = ''.join(format(ord(c), '08b') for c in message)
            bits = [int(bit) for bit in binary_message]
        else:
            bits = message
        
        print("=== DEBUG MANCHESTER DIFERENCIAL ===")
        print(f"Bits originales: {''.join(map(str, bits))}")
        print(f"Estado inicial: {self.initial_state}")
        
        # Codificación
        encoded_bits = self.coding(message)
        print(f"Bits codificados: {''.join(map(str, encoded_bits))}")
        
        # Mostrar proceso de codificación
        current_level = self.initial_state
        print("\nProceso de codificación:")
        for i, bit in enumerate(bits):
            first_half = encoded_bits[i*2]
            second_half = encoded_bits[i*2 + 1]
            
            if bit == 0:
                print(f"Bit {i}: 0 -> Transición AL INICIO: Nivel {current_level} -> {first_half}, Transición MITAD: {second_half}")
            else:
                print(f"Bit {i}: 1 -> SIN transición inicio: Nivel {current_level} -> {first_half}, Transición MITAD: {second_half}")
            
            # Actualizar para el siguiente bit
            current_level = second_half
        
        # Decodificación
        decoded_bits = self.decoding(encoded_bits)
        print(f"Bits decodificados: {''.join(map(str, decoded_bits))}")
        print(f"Decodificación correcta: {bits == decoded_bits}")
        
        return encoded_bits, decoded_bits
    
    def reset_state(self):
        """Resetear el estado inicial (útil para pruebas consecutivas)"""
        self.initial_state = 0
    
    def bits_to_string(self, bits):
        """Convierte lista de bits a string"""
        bytes_list = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) == 8:
                char_code = int(''.join(map(str, byte)), 2)
                bytes_list.append(char_code)
        
        return ''.join(chr(byte) for byte in bytes_list)