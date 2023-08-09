"""
Created 05/07/19
Developed by Fraser Love
"""

B64_CHAR_SET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

class Encoder:
    
    def encode(self, text):
        encoded = []
        # Convert text to bytes
        bytes = text.encode('ascii')

        for i in range(0, len(bytes), 3):
            # Process 3 bytes (24-bits) at a time
            chunk = bytes[i:i+3]
            binary_chunk = ''.join(format(byte, '08b') for byte in chunk)

            # Group binary into 6-bit chunks and pad with zeros
            while len(binary_chunk) % 6 != 0:
                binary_chunk += '00'
            # Convert binary chunks to decimal and map to Base64 characters
            for j in range(0, len(binary_chunk), 6):
                decimal = int(binary_chunk[j:j+6], 2)
                encoded.append(B64_CHAR_SET[decimal])

        # Add extra padding if necessary
        padding = '=' * ((3 - len(bytes) % 3) % 3)
        encoded.append(padding)
        return ''.join(encoded)
    
    def decode(self, base64):
        output_bytes = bytearray()
        # Remove padding characters and convert Base64 characters to their decimal values
        decimal = [B64_CHAR_SET.index(char) for char in base64.replace('=', '')]

        for i in range(0, len(decimal), 4):
            # Process 4 decimal values at a time
            chunk = decimal[i:i+4]
            # Convert decimal values to 6-bit binary strings
            binary_chunk = ''.join(format(value, '06b') for value in chunk)

            # Convert binary to bytes and add to the output
            for j in range(0, len(binary_chunk), 8):
                byte = int(binary_chunk[j:j+8], 2)
                output_bytes.append(byte)

        return output_bytes.decode('ascii')


encoder = Encoder()
string = encoder.decode(encoder.encode('Hello World!'))
print(string)
