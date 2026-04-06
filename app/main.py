import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from app.file_loader import load_par_files
from app.data_description import count_beats, calculate_duration, parse_time_to_seconds
from app.filtering import filter_by_quality
from app.statistics import compute_statistics


def main():
    print("=== Program analizy danych kardiologicznych ===")

    # 1. Wczytanie plików
    data = load_par_files()

    print("\nZnalezione pliki:")
    for name in data:
        print(" -", name)

    # 2. Opis danych
    descriptions = {}

    for filename, df in data.items():
        N = count_beats(df)
        T = calculate_duration(df)

        descriptions[filename] = {"N": N, "T": T}

    print("\nOpis danych:")
    for f, d in descriptions.items():
        print(f"{f}: N={d['N']} uderzeń, T={d['T']} sekund")

    # 3. Wybór metody analizy
    print("\nWybierz metodę analizy:")
    print("1 – na podstawie czasu (T)")
    print("2 – na podstawie liczby uderzeń serca (N)")

    choice = input("Twój wybór: ")

    # 4. Pobranie długości okna
    if choice == "1":
        window_seconds = float(input("\nPodaj długość odcinka w sekundach: "))
        window_beats = None
    else:
        window_beats = int(input("\nPodaj liczbę uderzeń serca do analizy: "))
        window_seconds = None

    # 5. Punkt odcięcia jakości
    threshold = float(input("\nPodaj minimalną jakość QI-ICG (np. 85): "))

    results = []

    for filename, df in data.items():

        # --- FILTROWANIE JAKOŚCI ---
        df_filtered = filter_by_quality(df, threshold)

        # --- INFORMACJE O ANALIZOWANYM ODCINKU ---
        N_total = len(df)
        T_total = calculate_duration(df)

        N_filtered = len(df_filtered)
        T_filtered = calculate_duration(df_filtered)

        percent_kept = (N_filtered / N_total) * 100 if N_total > 0 else 0
        percent_removed = 100 - percent_kept

        print("\n--- Analizowany odcinek po filtracji jakości ---")
        print(f"Liczba wierszy po filtracji: {N_filtered} (z {N_total}, usunięto {percent_removed:.1f}%)")
        print(f"Czas trwania po filtracji: {T_filtered:.2f} s (z {T_total:.2f} s)")
        print("-----------------------------------------------\n")

        # --- WYBÓR FRAGMENTU DANYCH ---
        if choice == "1":
            # wybór na podstawie czasu
            time_seconds = df_filtered.iloc[:, 1].apply(parse_time_to_seconds)

            max_time = time_seconds.max()
            start_time = max_time - window_seconds
            if start_time < 0:
                start_time = 0

            df_selected = df_filtered[time_seconds >= start_time]

        else:
            # wybór na podstawie liczby uderzeń
            df_selected = df_filtered.tail(window_beats)

        # --- STATYSTYKI DLA WSZYSTKICH PARAMETRÓW ---
        stats = {
            "filename": filename,
            "N_total": N_total,
            "T_total": T_total,
            "N_filtered": N_filtered,
            "T_filtered": T_filtered,
            "percent_removed": percent_removed,
            "N_selected": len(df_selected),
            "window_seconds": window_seconds,
            "window_beats": window_beats
        }

        # czas wybranego fragmentu
        if len(df_selected) > 1:
            stats["T_selected"] = calculate_duration(df_selected)
        else:
            stats["T_selected"] = 0

        # statystyki dla każdej kolumny numerycznej
        for col in df_selected.columns:
            if col in ["sample", "time"]:
                continue

            mean, std, med = compute_statistics(df_selected, col)

            stats[f"{col}_MN"] = mean
            stats[f"{col}_STD"] = std
            stats[f"{col}_MED"] = med

        results.append(stats)

    # --- ZAPIS DO CSV ---
    results_df = pd.DataFrame(results)
    results_df.to_csv("output/results.csv", index=False)

    print("\nWyniki zapisano w output/results.csv")


if __name__ == "__main__":
    main()
