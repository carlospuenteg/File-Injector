# Store bits in a channel value
def store_bits(channel_val:int, to_store:int, mask:int) -> int:    
    return (channel_val & mask) | to_store

# Retrieve bits from a channel value
def retrieve_bits(channel_val:int, base:int) -> int:
    return channel_val % base