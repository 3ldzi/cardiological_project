def count_beats(df):
    return len(df)

def parse_time_to_seconds(time_str):
    """
    Obsługuje formaty:
    - HH:MM:SS.mmm
    - HH:MM:SS:MMM
    - HH:MM:SS
    - z dodatkowymi spacjami
    """

    time_str = str(time_str).strip()

    # jeśli są milisekundy oddzielone kropką
    if "." in time_str:
        main, ms = time_str.split(".")
        ms = int(ms)
    # jeśli są milisekundy oddzielone dwukropkiem
    elif time_str.count(":") == 3:
        h, m, s, ms = time_str.split(":")
        return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
    else:
        main = time_str
        ms = 0

    parts = main.split(":")

    # zabezpieczenie: jeśli jest więcej niż 3 elementy, bierzemy pierwsze 3
    if len(parts) > 3:
        parts = parts[:3]

    h, m, s = parts

    return int(h)*3600 + int(m)*60 + int(s) + ms/1000

def calculate_duration(df):
    time_col = df.iloc[:, 1]

    start = parse_time_to_seconds(time_col.iloc[0])
    end = parse_time_to_seconds(time_col.iloc[-1])

    return end - start
