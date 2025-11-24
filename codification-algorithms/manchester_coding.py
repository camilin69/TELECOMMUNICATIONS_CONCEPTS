import numpy as np
import matplotlib.pyplot as plt

class ManchesterCoding:
    def __init__(self):
        pass
    
    def coding(self, message):
        """
        Codificación Manchester:
        - Bit 0: transición de 1 a 0 (alto a bajo)
        - Bit 1: transición de 0 a 1 (bajo a alto)
        Cada bit se representa con 2 niveles
        """
        if isinstance(message, str):
            binary_message = ''.join(format(ord(c), '08b') for c in message)
            bits = [int(bit) for bit in binary_message]
        else:
            bits = message
        
        encoded_bits = []
        
        for bit in bits:
            if bit == 0:
                # Transición 1->0 (alto a bajo)
                encoded_bits.extend([1, 0])
            else:  # bit == 1
                # Transición 0->1 (bajo a alto)
                encoded_bits.extend([0, 1])
        
        return encoded_bits
    
    def decoding(self, encoded_bits):
        """
        Decodificación Manchester:
        - [1,0]: bit 0
        - [0,1]: bit 1
        """
        if len(encoded_bits) % 2 != 0:
            raise ValueError("La longitud de bits codificados debe ser par")
        
        decoded_bits = []
        
        for i in range(0, len(encoded_bits), 2):
            first_half = encoded_bits[i]
            second_half = encoded_bits[i+1]
            
            if first_half == 1 and second_half == 0:
                decoded_bits.append(0)
            elif first_half == 0 and second_half == 1:
                decoded_bits.append(1)
            else:
                # Patrón inválido, manejar error
                decoded_bits.append(0)  # Valor por defecto
        
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
    
    def get_encoded_signal_for_plotting(self, message):
        """
        Retorna la señal codificada con más puntos para una mejor visualización
        de las transiciones en t/2
        """
        encoded_bits = self.coding(message)
        
        # Crear una señal con más puntos para mostrar transiciones suaves
        t_detailed = []
        signal_detailed = []
        
        for i, bit in enumerate(encoded_bits):
            # Cada bit codificado ocupa 0.5 unidades de tiempo
            start_time = i * 0.5
            end_time = (i + 1) * 0.5
            
            # Agregar puntos para transición suave
            t_detailed.extend([start_time, start_time + 0.25, end_time - 0.001])
            signal_detailed.extend([bit, bit, bit])
            
            # Si no es el último bit, preparar transición
            if i < len(encoded_bits) - 1:
                next_bit = encoded_bits[i + 1]
                if bit != next_bit:
                    t_detailed.append(end_time)
                    signal_detailed.append(next_bit)
        
        return t_detailed, signal_detailed, encoded_bits