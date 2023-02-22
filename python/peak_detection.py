from numpy import average


def peak_detection_max(data, threshold):
    av = average(data)
    if av * (1 + threshold) > max(data):
        return None

    index = data.index(max(data))
    return index / len(data)


def peak_detection_band(data) -> list:
    av = average(data)
    if av * (1 + 0.3) > max(data):
        return [None]

    peaks = []
    threshold = min(data) + ((max(data) - min(data)) / 2)
    on_peak = False
    left = 0
    right = 0

    move_right = 0
    move_right_step = round(len(data) * 0.05)

    if data[0] > threshold:
        on_peak = True
        move_right = move_right_step

    for idx, val in enumerate(data):
        if move_right > 0:
            move_right -= 1
            continue

        if on_peak is False and val >= threshold:
            left = idx
            on_peak = True
            move_right = move_right_step
        elif on_peak is True and val < threshold:
            right = idx
            on_peak = False
            move_right = move_right_step
            peaks.append(0.5 * (left + right) / len(data))

    if on_peak is True:
        right = len(data) - 1
        peaks.append((right - left) / len(data))

    return peaks
