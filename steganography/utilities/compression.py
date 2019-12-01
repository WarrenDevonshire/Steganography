import zlib


def compress_data(data):
    compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)

    # compress_ratio = (float(len(data)) - float(len(compressed_data))) / float(len(data))

    # print('Compressed: %d%%' % (100.0 * compress_ratio))

    return compressed_data


def decompress_data(data):
    decompressed_data = zlib.decompress(data)
    return decompressed_data
