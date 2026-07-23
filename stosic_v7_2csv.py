from __future__ import annotations

"""
https://github.com/gajaka/luces-pvs-theories
"""

"""
stosic_v7_2csv.py — 7-node krug (K=7 / prilagodjenje 7/39) — Brenier / monotone 1D mapa (7/39)

Izvor (Stosić / LUCES):
  luces-pvs-theories-main/brenier_uniqueness.pvs
  — kvadratni cost na pravoj → optimalna mapa T monotona (Brenier–McCann)
  luces-pvs-theories-main/rank_orientation.pvs
  — očuvanje ranga pri monotonom poklapanju

Mapiranje na 7/39:
  μ = empirijska mera svih brojeva sa celog CSV (sortirani atomi)
  izvor = 7 rangova (poslednje izvlačenje ima 7 atomima jednake težine)
  T monotono: rang k ↦ order-statistika μ na kvantilu (k + ½) / 7
  next = 7 slika T; ako ima duplikata, dopuna sledećim atomima μ (deterministički)
  bez randoma
"""

from typing import List

import numpy as np

from stosic_v1_2csv import CSV_LOTO, CSV_PLUS, MAX_NUM, N_PICK, load_draws


def empirical_atoms(draws: np.ndarray) -> np.ndarray:
    return np.sort(draws.astype(int).ravel())


def monotone_quantile_images(atoms: np.ndarray, n_pick: int = N_PICK) -> List[int]:
    n = len(atoms)
    images: List[int] = []
    for k in range(n_pick):
        q = (k + 0.5) / n_pick
        idx = int(q * n)
        if idx >= n:
            idx = n - 1
        images.append(int(atoms[idx]))
    return images


def unique_top_fill(images: List[int], atoms: np.ndarray, n_pick: int = N_PICK) -> List[int]:
    out: List[int] = []
    seen = set()
    for x in images:
        if x not in seen and 1 <= x <= MAX_NUM:
            out.append(x)
            seen.add(x)
        if len(out) >= n_pick:
            return sorted(out)
    for x in atoms:
        xi = int(x)
        if xi not in seen and 1 <= xi <= MAX_NUM:
            out.append(xi)
            seen.add(xi)
        if len(out) >= n_pick:
            break
    return sorted(out[:n_pick])


def predict_next(draws: np.ndarray) -> List[int]:
    atoms = empirical_atoms(draws)
    images = monotone_quantile_images(atoms, N_PICK)
    return unique_top_fill(images, atoms, N_PICK)


def main():
    next_loto = predict_next(load_draws(CSV_LOTO))
    next_loto_plus = predict_next(load_draws(CSV_PLUS))
    print("next_loto:      ", next_loto)
    print("next_loto_plus: ", next_loto_plus)


if __name__ == "__main__":
    main()



"""
next_loto:       [3, 9, 15, 20, 26, 31, 37]
next_loto_plus:  [3, 9, 14, 20, 26, 31, 37]
"""



"""
Brenier 1D (brenier_uniqueness + rang). 
"""



"""
Stosić jezgro	Ocena

v1
fisher_voronoi (d_F, centroid, nearest_regime)
Da — najbliže strogo

v2
regime_sequence / prelaz iz istog PVS
Uglavnom da — operaciona frekvencija prelaza je naša mapa, ali ideja je njegova

v3
dual_observability (obe karte)
Delimično — A+B = remix v1+v2 signala, ne čitanje PVS formula

v4
blizina u prostoru mera / stabilnost
Slabo — 1/(ε+d_F) težine su moja konstrukcija, ne direktan teorem

v5
entropy_along_geodesic (H na mid)
Uglavnom da — filter po H(mid)≤max je blizu teoremima

v6
velocity_asymmetry / lie shape direction
Uglavnom da — √p razlike; suma max(u,0) je naša agregacija
Zaključak: strogo čist je uglavnom v1 (i solidno v5/v6/v2). v3 i naročito v4 su više moje operacione verzije „u duhu“ nego doslovan Stosić.
"""



"""
21 teorija

fisher_voronoi → v1, v2
dual_observability → v3
v4 se pozivao na W₂/stabilnost — slabo / nije strogo
entropy_along_geodesic → v5
velocity_asymmetry (+ delom lie_generator_structure) → v6
brenier_uniqueness (+ delom rank_orientation) → v7

kantorovich_duality
cyclical_monotonicity
displacement_interpolation
displacement_concavity
wasserstein_metric (strogo)
transport_structure
transport_structure_v2
transport_stability
stability_of_maps
monge_kantorovich_equivalence
lie_generator_structure (pun T10)
fisher_boundary
hybrid_observability
tangent_bundle
global_optimality
"""



"""
Kratko, o repou:

21 PVS teorija — sve su prošle kroz v1–v22 (neke ranije labavo: naročito v3/v4; rank_orientation je ušao uz Brenier u v7).
Repo je o spektralnom OT / LUCES (ESP32), ne o lotou — 7/39 je naša mapa, ne Stosićev domen.
Najčistije jezgro oko Fisher–Voronoi, Brenier/CM, W₂, T10 (lie_generator_structure). global_optimality je samo aksiomi + lema (bez teorema).
Empirija u PVS-u (bootovi, κ, Monge fraction) ne prenosi se automatski na CSV — samo struktura ideja.
"""
