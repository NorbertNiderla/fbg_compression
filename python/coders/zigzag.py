def zigzag_encode(data):
    output = []
    for x in data:
        if x >= 0:
            output.append(2 * x)
        else:
            output.append(-2 * x + 1)

    return output


def zigzag_decode(data):
    output = []
    for x in data:
        if x % 2 == 0:
            output.append(x // 2)
        else:
            output.append((x - 1) // -2)

    return output
