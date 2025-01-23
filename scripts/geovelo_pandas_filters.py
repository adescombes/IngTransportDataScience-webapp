# q1

# Masque pour les routes à double sens avec accotement cyclable d'un côté
mask_double_sens = (
    (df['oneway'].isnull() | ~df['oneway'].isin(['yes', '-1'])) &
    (df['cycleway:right'] == 'shoulder') &
    (df['cycleway:left'].isnull() | ~df['cycleway:left'].isin(['shoulder']))
)

# Masque pour les routes à sens unique avec accotement cyclable
mask_sens_unique = (
    ((df['oneway'] == 'yes') | (df['junction'].isin(['roundabout', 'circular']))) &
    ((df['cycleway'] == 'shoulder') | (df['cycleway:right'] == 'shoulder'))
)

# Masque pour les routes à sens inverse avec accotement à gauche
mask_sens_inverse = (
    (df['oneway'] == '-1') & (df['cycleway:left'] == 'shoulder')
)

# Combinaison des masques
filtered_df_q1 = df[mask_double_sens | mask_sens_unique | mask_sens_inverse]

# q2

# Masque pour les routes à double sens avec accotement cyclable à gauche
mask_double_sens_left = (
    (df['oneway'].isnull() | ~df['oneway'].isin(['yes', '-1'])) &
    (df['cycleway:left'] == 'shoulder') &
    (df['cycleway:right'].isnull() | ~df['cycleway:right'].isin(['shoulder']))
)

# Masque pour les routes à sens unique avec accotement cyclable à gauche
mask_sens_unique_left = (
    ((df['oneway'] == 'yes') | (df['junction'].isin(['roundabout', 'circular']))) &
    (df['cycleway:left'] == 'shoulder')
)

# Masque pour les routes à sens inverse avec accotement cyclable à gauche
mask_sens_inverse_left = (
    (df['oneway'] == '-1') &
    ((df['cycleway:left'] == 'shoulder') | (df['cycleway'] == 'shoulder'))
)

# Combinaison des masques
filtered_df_q2 = df[mask_double_sens_left | mask_sens_unique_left | mask_sens_inverse_left]


# q3

mask_double_sens_both = (
    (df['oneway'].isnull() | (df['oneway'] == 'no')) &
    (
        (df['cycleway'] == 'shoulder') |
        ((df['cycleway:right'] == 'shoulder') & (df['cycleway:left'] == 'shoulder')) |
        (df['cycleway:both'] == 'shoulder')
    )
)

filtered_df_q3 = df[mask_double_sens_both]

# q4

mask_shared_path = (
    (df['highway'].isin(['footway', 'path'])) &
    (df['bicycle'] == 'designated') &
    (df['segregated'].isnull() | (df['segregated'] == 'no'))
)

filtered_df_q4 = df[mask_shared_path]
