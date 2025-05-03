import pickle
import io
import os

def rle_encode(data):
    """Encode data using Run-Length Encoding"""
    if not data:
        return bytearray()
    
    encoded = bytearray()
    count = 1
    current = data[0]
    
    # Process all bytes
    for i in range(1, len(data)):
        if data[i] == current and count < 255:  # Limit runs to 255 for byte storage
            count += 1
        else:
            # Store the count and byte
            encoded.append(count)
            encoded.append(current)
            # Reset for next run
            current = data[i]
            count = 1
            
    # Add the last run
    encoded.append(count)
    encoded.append(current)
    
    return encoded

def rle_decode(encoded_data):
    """Decode RLE-encoded data"""
    if not encoded_data or len(encoded_data) % 2 != 0:
        return bytearray()
    
    decoded = bytearray()
    
    # Process pairs (count, byte)
    for i in range(0, len(encoded_data), 2):
        count = encoded_data[i]
        byte = encoded_data[i+1]
        decoded.extend([byte] * count)
        
    return decoded

def encode_file(input_path, output_path):
    """Encode a file using RLE"""
    with open(input_path, 'rb') as file:
        data = file.read()
    
    encoded_data = rle_encode(data)
    
    with open(output_path, 'wb') as file:
        metadata = {
            'original_size': len(data)
        }
        pickle.dump(metadata, file)
        file.write(encoded_data)
    
    original_size = len(data)
    compressed_size = len(encoded_data) + len(pickle.dumps(metadata))
    compression_ratio = (original_size - compressed_size) / original_size * 100 if original_size > 0 else 0
    
    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {compression_ratio:.2f}%")
    
    return output_path

def decode_file(input_path, output_path):
    """Decode an RLE-encoded file"""
    with open(input_path, 'rb') as file:
        metadata = pickle.load(file)
        encoded_data = file.read()
    
    decoded_data = rle_decode(encoded_data)
    
    with open(output_path, 'wb') as file:
        file.write(decoded_data)
    
    return output_path

def encode_data(data):
    """Encode data using RLE (in-memory version)"""
    encoded_data = rle_encode(data)
    
    memory_file = io.BytesIO()
    
    metadata = {
        'original_size': len(data)
    }
    pickle.dump(metadata, memory_file)
    memory_file.write(encoded_data)
    
    original_size = len(data)
    compressed_size = len(encoded_data) + len(pickle.dumps(metadata))
    compression_ratio = (original_size - compressed_size) / original_size * 100 if original_size > 0 else 0
    
    print(f"Original size: {original_size} bytes")
    print(f"Compressed size: {compressed_size} bytes")
    print(f"Compression ratio: {compression_ratio:.2f}%")
    
    memory_file.seek(0)
    return memory_file.read(), compression_ratio

def decode_data(encoded_data_bytes):
    """Decode data that was encoded using RLE"""
    memory_file = io.BytesIO(encoded_data_bytes)
    
    # Skip metadata
    pickle.load(memory_file)
    
    # Get the encoded data
    encoded_data = memory_file.read()
    
    # Decode the data
    return rle_decode(encoded_data)