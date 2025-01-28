def geovelo_pandas_filters(df):

    required_columns = [
        "oneway",
        "cycleway",
        "cycleway:right",
        "cycleway:left",
        "cycleway:both",
        "oneway:bicycle",
        "highway",
        "junction",
        "psv",
        "bus",
        "access",
        "motor_vehicle",
        "motorcar",
        "motorcycle",
        "bicycle",
        "cycleway:right:bicycle",
        "cycleway:left:bicycle",
        "cycleway:both:bicycle",
        "sidewalk",
        "sidewalk:right:bicycle",
        "sidewalk:left:bicycle",
        "sidewalk:both:bicycle",
        "sidewalk:segregated",
        "sidewalk:right:segregated",
        "sidewalk:left:segregated",
        "sidewalk:both:segregated",
        "footway",
        "segregated",
        "surface",
        "smoothness",
        "tracktype",
        "maxspeed",
        "maxspeed:type",
        "zone:maxspeed",
        "source:maxspeed",
        "length_line[m]",
        "busway",
        "busway:right",
        "busway:left",
        "ramp:bicycle",
        "ramp:bicycle:right",
        "ramp:bicycle:left",
        "ramp:bicycle:both",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Colonnes manquantes : {missing_columns}")

    # on check si toutes les colonnes requises pour les maskques sont présentes, sinon valeurs None par défaut
    for col in missing_columns:
        df[col] = None

    mask_q1 = (
        (
            (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
            & (df["cycleway:right"] == "shoulder")
            & (df["cycleway:left"].isnull() | ~df["cycleway:left"].isin(["shoulder"]))
        )
        | ((df["oneway"] == "yes") | (df["junction"].isin(["roundabout", "circular"])))
        & ((df["cycleway"] == "shoulder") | (df["cycleway:right"] == "shoulder"))
        | (df["oneway"] == "-1") & (df["cycleway:left"] == "shoulder")
    )

    mask_q2 = (
        (
            (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
            & (df["cycleway:left"] == "shoulder")
            & (df["cycleway:right"].isnull() | ~df["cycleway:right"].isin(["shoulder"]))
        )
        | ((df["oneway"] == "yes") | (df["junction"].isin(["roundabout", "circular"])))
        & (df["cycleway:left"] == "shoulder")
        | (df["oneway"] == "-1")
        & ((df["cycleway:left"] == "shoulder") | (df["cycleway"] == "shoulder"))
    )

    mask_q3 = (df["oneway"].isnull() | (df["oneway"] == "no")) & (
        (df["cycleway"] == "shoulder")
        | ((df["cycleway:right"] == "shoulder") & (df["cycleway:left"] == "shoulder"))
        | (df["cycleway:both"] == "shoulder")
    )

    mask_q4 = (
        (df["highway"].isin(["footway", "path"]))
        & (df["bicycle"] == "designated")
        & (df["segregated"].isnull() | (df["segregated"] == "no"))
    )

    mask_q5 = (
        (
            (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
            & (df["oneway:bicycle"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
        )
        & (
            (
                (df["highway"] == "footway")
                & (df["footway"].isnull() | ~df["footway"].isin(["sidewalk"]))
                & (df["bicycle"].isin(["yes", "destination"]))
            )
            | ((df["highway"] == "path") & (df["bicycle"].isin(["yes", "destination"])))
        )
        & (
            (
                (
                    df["surface"].isin(
                        [
                            "paved",
                            "asphalt",
                            "concrete",
                            "concrete:plates",
                            "concrete:lanes",
                            "paving_stones",
                            "sett",
                            "unhewn_cobblestone",
                            "cobblestone",
                            "metal",
                            "wood",
                            "unpaved",
                            "compacted",
                            "fine_gravel",
                            "gravel",
                            "pebblestone",
                            "ground",
                            "tartan",
                            "clay",
                            "metal_grid",
                        ]
                    )
                    | df["surface"].isnull()
                )
                & (
                    df["smoothness"].isnull()
                    | ~df["smoothness"].isin(
                        ["bad", "very_bad", "horrible", "very_horrible", "impassable"]
                    )
                )
                & (
                    df["tracktype"].isnull()
                    | ~df["tracktype"].isin(["grade3", "grade4", "grade5"])
                )
            )
        )
    )

    mask_q6 = (
        (
            (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
            & (
                (df["cycleway:right"] == "lane")
                & (df["cycleway:left"].isnull() | ~df["cycleway:left"].isin(["lane"]))
            )
        )
        | (
            (
                (df["oneway"] == "yes")
                | (df["junction"].isin(["roundabout", "circular"]))
            )
            & (((df["cycleway"] == "lane") | (df["cycleway:right"] == "lane")))
        )
        | (
            (df["oneway"] == "-1")
            & (
                (df["cycleway:right"] == "lane")
                & (df["oneway:bicycle"].isnull() | (df["oneway:bicycle"] != "no"))
            )
        )
    )

    mask_q7 = (
        (
            (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
            & (
                (df["cycleway:left"] == "lane")
                & (df["cycleway:right"].isnull() | ~df["cycleway:right"].isin(["lane"]))
            )
        )
        | (
            (
                (df["oneway"] == "yes")
                | (df["junction"].isin(["roundabout", "circular"]))
            )
            & (
                (df["cycleway:left"] == "lane")
                & (df["oneway:bicycle"].isnull() | (df["oneway:bicycle"] != "no"))
            )
        )
        | (
            (df["oneway"] == "-1")
            & ((df["cycleway:left"] == "lane") | (df["cycleway"] == "lane"))
        )
    )

    mask_q8 = (
        (
            (df["oneway"].isnull() | (df["oneway"] == "no"))
            & (
                df["junction"].isnull()
                | ~df["junction"].isin(["roundabout", "circular"])
            )
        )
        & (
            (df["cycleway"].isin(["lane", "opposite_lane"]))
            | (
                (df["cycleway:right"].isin(["lane", "opposite_lane"]))
                & (df["cycleway:left"].isin(["lane", "opposite_lane"]))
            )
            | (df["cycleway:both"].isin(["lane", "opposite_lane"]))
        )
        & ((df["lanes"].isnull() | ~df["lanes"].isin(["1"])))
    )

    mask_q9 = df["cycleway:right"].isin(["lane", "opposite_lane"])

    mask_q10 = df["cycleway:left"].isin(["lane", "opposite_lane"])

    mask_q11 = (
        (
            (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
            & (
                (df["cycleway:right"] == "shared_lane")
                & (
                    df["cycleway:left"].isnull()
                    | ~df["cycleway:left"].isin(["shared_lane"])
                )
            )
        )
        | (
            (
                (df["oneway"] == "yes")
                | (df["junction"].isin(["roundabout", "circular"]))
            )
            & (
                (df["cycleway"] == "shared_lane")
                | (df["cycleway:right"] == "shared_lane")
            )
        )
        | ((df["oneway"] == "-1") & (df["cycleway:left"] == "shared_lane"))
    )

    mask_q12 = (
        (
            (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
            & (
                (df["cycleway:left"] == "shared_lane")
                & (
                    df["cycleway:right"].isnull()
                    | ~df["cycleway:right"].isin(["shared_lane"])
                )
            )
        )
        | (
            (
                (df["oneway"] == "yes")
                | (df["junction"].isin(["roundabout", "circular"]))
            )
            & (
                (df["cycleway:left"] == "shared_lane")
                & (df["oneway:bicycle"].isnull() | (df["oneway:bicycle"] != "no"))
            )
        )
        | (
            (df["oneway"] == "-1")
            & (
                (df["cycleway:left"] == "shared_lane")
                | (df["cycleway"] == "shared_lane")
            )
        )
    )

    mask_q13 = (
        (df["oneway"].isnull() | (df["oneway"] == "no"))
        & (df["junction"].isnull() | ~df["junction"].isin(["roundabout", "circular"]))
    ) & (
        (df["cycleway"] == "shared_lane")
        | (
            (df["cycleway:right"] == "shared_lane")
            & (df["cycleway:left"] == "shared_lane")
        )
        | (df["cycleway:both"] == "shared_lane")
    )

    mask_q14 = (
        (
            (df["oneway"].isin(["yes", "-1"]))
            & (
                (df["cycleway"] == "opposite")
                | (df["cycleway:left"] == "opposite")
                | (df["cycleway:right"] == "opposite")
            )
        )
        | (
            (df["oneway"] == "yes")
            & (df["oneway:bicycle"] == "no")
            & (
                (df["cycleway"].isnull() | df["cycleway"].isin(["no", "shared_lane"]))
                & (
                    df["cycleway:left"].isnull()
                    | df["cycleway:left"].isin(["no", "shared_lane"])
                )
                & (
                    df["cycleway:both"].isnull()
                    | df["cycleway:both"].isin(["no", "shared_lane"])
                )
            )
        )
        | (
            (df["oneway"] == "-1")
            & (df["oneway:bicycle"] == "no")
            & (
                (df["cycleway"].isnull() | df["cycleway"].isin(["no", "shared_lane"]))
                & (
                    df["cycleway:right"].isnull()
                    | df["cycleway:right"].isin(["no", "shared_lane"])
                )
                & (
                    df["cycleway:both"].isnull()
                    | df["cycleway:both"].isin(["no", "shared_lane"])
                )
            )
        )
    )

    mask_q15 = (
        (df["oneway"].isin(["yes", "-1"])) & (df["cycleway:right"] == "opposite_lane")
    ) | (
        (df["oneway"] == "-1")
        & (
            (df["cycleway"] == "opposite_lane")
            | ((df["cycleway:right"] == "lane") & (df["oneway:bicycle"] == "no"))
            | ((df["cycleway:both"] == "lane") & (df["oneway:bicycle"] == "no"))
        )
    )

    mask_q16 = (
        (df["oneway"].isin(["yes", "-1"])) & (df["cycleway:left"] == "opposite_lane")
    ) | (
        (df["oneway"] == "yes")
        & (
            (df["cycleway"] == "opposite_lane")
            | ((df["cycleway:left"] == "lane") & (df["oneway:bicycle"] == "no"))
            | ((df["cycleway:both"] == "lane") & (df["oneway:bicycle"] == "no"))
        )
    )

    mask_q17 = (
        (df["oneway"].isin(["yes", "-1"])) & (df["cycleway:right"] == "opposite_track")
    ) | (
        (df["oneway"] == "-1")
        & (
            (df["cycleway"] == "opposite_track")
            | ((df["cycleway:right"] == "track") & (df["oneway:bicycle"] == "no"))
            | ((df["cycleway:both"] == "track") & (df["oneway:bicycle"] == "no"))
        )
    )

    mask_q18 = (
        (df["oneway"].isin(["yes", "-1"])) & (df["cycleway:left"] == "opposite_track")
    ) | (
        (df["oneway"] == "yes")
        & (
            (df["cycleway"] == "opposite_track")
            | ((df["cycleway:left"] == "track") & (df["oneway:bicycle"] == "no"))
            | ((df["cycleway:both"] == "track") & (df["oneway:bicycle"] == "no"))
        )
    )

    mask_q19 = (
        (df["oneway"].isin(["yes", "-1"]) | df["oneway:bicycle"].isin(["yes", "-1"]))
        & (
            (
                (df["highway"] == "footway")
                & (df["footway"].isnull() | ~df["footway"].isin(["sidewalk"]))
                & (df["bicycle"].isin(["designated", "official"]))
            )
            | (
                (df["highway"] == "path")
                & (df["bicycle"].isin(["designated", "official"]))
                & (df["foot"].isnull() | ~df["foot"].isin(["designated"]))
            )
        )
        & (
            (
                (
                    df["surface"].isin(
                        [
                            "paved",
                            "asphalt",
                            "concrete",
                            "concrete:plates",
                            "concrete:lanes",
                            "paving_stones",
                            "sett",
                            "unhewn_cobblestone",
                            "cobblestone",
                            "metal",
                            "wood",
                            "unpaved",
                            "compacted",
                            "fine_gravel",
                            "gravel",
                            "pebblestone",
                            "ground",
                            "tartan",
                            "clay",
                            "metal_grid",
                        ]
                    )
                    | df["surface"].isnull()
                )
                & (
                    df["smoothness"].isnull()
                    | ~df["smoothness"].isin(
                        ["bad", "very_bad", "horrible", "very_horrible", "impassable"]
                    )
                )
                & (
                    df["tracktype"].isnull()
                    | ~df["tracktype"].isin(["grade3", "grade4", "grade5"])
                )
            )
        )
    )

    mask_q20 = (
        (
            (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
            & (
                df["oneway:bicycle"].isnull()
                | ~df["oneway:bicycle"].isin(["yes", "-1"])
            )
        )
        & (
            (
                (df["highway"] == "footway")
                & (df["footway"].isnull() | ~df["footway"].isin(["sidewalk"]))
                & (df["bicycle"].isin(["designated", "official"]))
            )
            | (
                (df["highway"] == "path")
                & (df["bicycle"].isin(["designated", "official"]))
                & (df["foot"].isnull() | ~df["foot"].isin(["designated"]))
            )
        )
        & (
            (
                (
                    df["surface"].isin(
                        [
                            "paved",
                            "asphalt",
                            "concrete",
                            "concrete:plates",
                            "concrete:lanes",
                            "paving_stones",
                            "sett",
                            "unhewn_cobblestone",
                            "cobblestone",
                            "metal",
                            "wood",
                            "unpaved",
                            "compacted",
                            "fine_gravel",
                            "gravel",
                            "pebblestone",
                            "ground",
                            "tartan",
                            "clay",
                            "metal_grid",
                        ]
                    )
                    | df["surface"].isnull()
                )
                & (
                    df["smoothness"].isnull()
                    | ~df["smoothness"].isin(
                        ["bad", "very_bad", "horrible", "very_horrible", "impassable"]
                    )
                )
                & (
                    df["tracktype"].isnull()
                    | ~df["tracktype"].isin(["grade3", "grade4", "grade5"])
                )
            )
        )
    )

    mask_q21 = (
        (df["maxspeed"] == "30")
        & ((df["maxspeed:type"].isnull() | (df["maxspeed:type"] != "CH:zone30")))
        & (df["oneway"].isin(["yes", "-1"]))
    )

    mask_q22 = (
        (df["maxspeed"] == "30")
        & ((df["maxspeed:type"].isnull() | (df["maxspeed:type"] != "CH:zone30")))
        & (df["oneway"].isnull() | (df["oneway"] == "no"))
    )

    mask_q23 = (
        (df["highway"] == "pedestrian")
        & (df["oneway"].isin(["yes", "-1"]))
        & (df["bicycle"].isnull() | (df["bicycle"] != "no"))
    )

    mask_q24 = (
        (df["highway"] == "pedestrian")
        & (df["oneway"].isnull() | (df["oneway"] == "no"))
        & (df["bicycle"].isnull() | (df["bicycle"] != "no"))
    )

    mask_q25 = ((df["oneway"] == "yes") & (df["highway"] == "cycleway")) | (
        (
            (df["cycleway:right"] == "track")
            & (
                df["cycleway:left"].isnull()
                | ~df["cycleway:left"].isin(["track", "opposite_track"])
            )
        )
        | (
            (df["oneway"] == "yes")
            & ((df["cycleway"] == "track") | (df["cycleway:right"] == "track"))
        )
        | (
            (df["oneway"] == "-1")
            & (df["cycleway:right"] == "track")
            & (df["oneway:bicycle"].isnull() | (df["oneway:bicycle"] != "no"))
        )
    )

    mask_q26 = (
        ((df["cycleway"] == "track") & (df["oneway"] == "-1"))
        | (
            (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
            & (
                (df["cycleway:left"] == "track")
                & (df["cycleway:right"].isnull() | (df["cycleway:right"] != "track"))
            )
        )
        | (
            (df["oneway"] == "yes")
            & (
                (df["cycleway:left"] == "track")
                & (df["oneway:bicycle"].isnull() | (df["oneway:bicycle"] != "no"))
            )
        )
        | (
            (df["oneway"] == "-1")
            & ((df["cycleway:left"] == "track") | (df["cycleway"] == "track"))
        )
    )

    mask_q27 = (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"])) & (
        (df["highway"] == "cycleway")
        | (
            (df["cycleway"].isin(["track", "opposite_track"]))
            | (df["cycleway:both"].isin(["track", "opposite_track"]))
            | (
                (df["cycleway:left"].isin(["track", "opposite_track"]))
                & (df["cycleway:right"].isin(["track", "opposite_track"]))
            )
        )
    )

    mask_q28 = df["cycleway:right"].isin(["track", "opposite_track"])

    mask_q29 = df["cycleway:left"].isin(["track", "opposite_track"])

    mask_q30 = (
        (df["segregated"] == "yes")
        & (df["highway"] == "footway")
        & (df["footway"] == "sidewalk")
        & (df["bicycle"] != "no")
        & (
            (df["oneway"].isin(["yes", "-1"]))
            | (df["oneway:bicycle"].isin(["yes", "-1"]))
        )
    )

    mask_q31 = (
        (df["segregated"] == "yes")
        & (df["highway"] == "footway")
        & (df["footway"] == "sidewalk")
        & (df["bicycle"].isin(["yes", "designated", "official"]))
        & (df["oneway"] == "yes")
    ) | (
        (df["sidewalk"].isin(["right", "both"]))
        & (df["sidewalk:right:bicycle"].isin(["yes", "designated", "official"]))
        & (
            (df["sidewalk:left:bicycle"].isnull())
            | (df["sidewalk:left:bicycle"] == "no")
        )
    )

    mask_q32 = (
        (df["segregated"] == "yes")
        & (df["highway"] == "footway")
        & (df["footway"] == "sidewalk")
        & (df["bicycle"].isin(["yes", "designated", "official"]))
        & (df["oneway"] == "-1")
    ) | (
        (df["sidewalk"].isin(["left", "both"]))
        & (df["sidewalk:left:bicycle"].isin(["yes", "designated", "official"]))
        & (
            (df["sidewalk:right:bicycle"].isnull())
            | (df["sidewalk:right:bicycle"] == "no")
        )
    )

    mask_q33 = (
        (df["segregated"] == "yes")
        & (df["highway"] == "footway")
        & (df["footway"] == "sidewalk")
        & (df["bicycle"].isin(["yes", "designated", "official"]))
        & (
            (df["oneway"].isnull() | (df["oneway"] == "no"))
            & (df["oneway:bicycle"].isnull() | (df["oneway:bicycle"] == "no"))
        )
    ) | (
        (df["sidewalk"] == "both")
        & (
            (
                (df["sidewalk:right:bicycle"].isin(["yes", "designated", "official"]))
                & (df["sidewalk:left:bicycle"].isin(["yes", "designated", "official"]))
            )
        )
    )

    mask_q34 = (
        (
            df["highway"].isin(
                [
                    "track",
                    "service",
                    "unclasified",
                    "residential",
                    "tertiary",
                    "secondary",
                    "primary",
                ]
            )
        )
        & (
            (
                (
                    df["surface"].isin(
                        [
                            "paved",
                            "asphalt",
                            "concrete",
                            "concrete:plates",
                            "concrete:lanes",
                            "paving_stones",
                            "sett",
                            "unhewn_cobblestone",
                            "cobblestone",
                            "metal",
                            "wood",
                            "unpaved",
                            "compacted",
                            "fine_gravel",
                            "gravel",
                            "pebblestone",
                            "ground",
                            "tartan",
                            "clay",
                            "metal_grid",
                        ]
                    )
                )
                | df["surface"].isnull()
            )
            & (
                df["smoothness"].isnull()
                | ~df["smoothness"].isin(
                    ["bad", "very_bad", "horrible", "very_horrible", "impassable"]
                )
            )
            & (
                df["tracktype"].isnull()
                | ~df["tracktype"].isin(["grade3", "grade4", "grade5"])
            )
        )
        & (
            (df["highway"] != "track")
            | df[["surface", "smoothness", "tracktype"]].notnull().any(axis=1)
        )
        & (
            (df["psv"].isnull() | (df["psv"] == "no"))
            & (df["motorcycle"].isnull() | (df["motorcycle"] == "no"))
            & (df["bus"].isnull() | (df["bus"] == "no"))
        )
        & (
            (
                (
                    df["motor_vehicle"].isin(["no", "forestry", "agricultural"])
                    | df["motorcar"].isin(["no", "forestry", "agricultural"])
                )
                & (df["bicycle"].isnull() | (df["bicycle"] != "no"))
            )
            | (
                (df["access"].isin(["no", "forestry", "agricultural"]))
                & (df["bicycle"].isin(["yes", "designated"]))
                & (df["motor_vehicle"].isnull() | (df["motor_vehicle"] == "no"))
            )
        )
        & (
            df["oneway"].isin(["yes", "-1"])
            & (df["oneway:bicycle"].isnull() | df["oneway:bicycle"].isin(["yes", "-1"]))
        )
    )

    mask_q35 = (
        (
            df["highway"].isin(
                [
                    "track",
                    "service",
                    "unclasified",
                    "residential",
                    "tertiary",
                    "secondary",
                    "primary",
                ]
            )
        )
        & (
            (
                (
                    df["surface"].isin(
                        [
                            "paved",
                            "asphalt",
                            "concrete",
                            "concrete:plates",
                            "concrete:lanes",
                            "paving_stones",
                            "sett",
                            "unhewn_cobblestone",
                            "cobblestone",
                            "metal",
                            "wood",
                            "unpaved",
                            "compacted",
                            "fine_gravel",
                            "gravel",
                            "pebblestone",
                            "ground",
                            "tartan",
                            "clay",
                            "metal_grid",
                        ]
                    )
                )
                | df["surface"].isnull()
            )
            & (
                df["smoothness"].isnull()
                | ~df["smoothness"].isin(
                    ["bad", "very_bad", "horrible", "very_horrible", "impassable"]
                )
            )
            & (
                df["tracktype"].isnull()
                | ~df["tracktype"].isin(["grade3", "grade4", "grade5"])
            )
        )
        & (
            (df["highway"] != "track")
            | df[["surface", "smoothness", "tracktype"]].notnull().any(axis=1)
        )
        & (
            (df["psv"].isnull() | (df["psv"] == "no"))
            & (df["motorcycle"].isnull() | (df["motorcycle"] == "no"))
            & (df["bus"].isnull() | (df["bus"] == "no"))
        )
        & (
            (
                (
                    df["motor_vehicle"].isin(["no", "forestry", "agricultural"])
                    | df["motorcar"].isin(["no", "forestry", "agricultural"])
                )
                & (df["bicycle"].isnull() | (df["bicycle"] != "no"))
            )
            | (
                (
                    df["access"].isin(["no", "forestry", "agricultural"])
                    & (df["bicycle"].isin(["yes", "designated"]))
                )
                & (df["motor_vehicle"].isnull() | (df["motor_vehicle"] == "no"))
            )
        )
        & (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
        & (df["oneway:bicycle"].isnull() | ~df["oneway:bicycle"].isin(["yes", "-1"]))
    )

    mask_q36 = (
        (df["segregated"].isnull() | (df["segregated"] != "yes"))
        & (df["highway"] == "footway")
        & (df["footway"] == "sidewalk")
        & (df["bicycle"] != "no")
        & (
            (df["oneway"].isin(["yes", "-1"]))
            | (df["oneway:bicycle"].isin(["yes", "-1"]))
        )
    )

    mask_q37 = (
        (df["segregated"].isnull() | (df["segregated"] != "yes"))
        & (df["highway"] == "footway")
        & (df["footway"] == "sidewalk")
        & (df["bicycle"].isin(["yes", "designated", "official"]))
        & (df["oneway"] == "yes")
    ) | (
        (df["sidewalk"].isin(["right", "both"]))
        & (df["sidewalk:right:bicycle"].isin(["yes", "designated", "official"]))
        & (
            (df["sidewalk:left:bicycle"].isnull())
            | (df["sidewalk:left:bicycle"] == "no")
        )
    )

    mask_q38 = (
        (df["segregated"].isnull() | (df["segregated"] != "yes"))
        & (df["highway"] == "footway")
        & (df["footway"] == "sidewalk")
        & (df["bicycle"].isin(["yes", "designated", "official"]))
        & (df["oneway"] == "-1")
    ) | (
        (df["sidewalk"].isin(["left", "both"]))
        & (df["sidewalk:left:bicycle"].isin(["yes", "designated", "official"]))
        & (
            (df["sidewalk:right:bicycle"].isnull())
            | (df["sidewalk:right:bicycle"] == "no")
        )
    )

    mask_q39 = (
        (df["segregated"].isnull() | (df["segregated"] != "yes"))
        & (df["highway"] == "footway")
        & (df["footway"] == "sidewalk")
        & (df["bicycle"].isin(["yes", "designated", "official"]))
        & (
            (df["oneway"].isnull() | (df["oneway"] == "no"))
            & (df["oneway:bicycle"].isnull() | (df["oneway:bicycle"] == "no"))
        )
    ) | (
        (df["sidewalk"] == "both")
        & (
            (
                (df["sidewalk:right:bicycle"].isin(["yes", "designated", "official"]))
                & (df["sidewalk:left:bicycle"].isin(["yes", "designated", "official"]))
            )
        )
    )

    mask_q40 = (
        (
            (df["oneway"] == "yes")
            & (
                (
                    (df["highway"] == "service")
                    & (df["psv"].isin(["yes"]))
                    & (df["access"] == "no")
                    & (df["bicycle"].notnull() & (df["bicycle"] != "no"))
                )
                | (
                    (df["cycleway"] == "share_busway")
                    & (
                        df["busway"].notnull()
                        & (df["busway"] != "no")
                        & (df["busway"] != "opposite_lane")
                    )
                )
                | (
                    (df["highway"] == "bus_guideway")
                    & (
                        (df["bicycle"].notnull() & (df["bicycle"] != "no"))
                        | (df["cycleway"] == "share_busway")
                    )
                )
            )
        )
        | (
            (df["oneway"] == "-1")
            & (
                (df["cycleway"].isin(["share_busway", "opposite_share_busway"]))
                & (df["busway"] == "opposite_lane")
            )
        )
        | (
            (df["cycleway"] == "share_busway")
            & (
                (df["busway:right"].notnull() & (df["busway:right"] != "no"))
                & (df["busway:left"].isnull() | (df["busway:left"] == "no"))
            )
        )
        | (
            (df["cycleway:right"].isin(["share_busway", "opposite_share_busway"]))
            & (
                df["cycleway:left"].isnull()
                | ~df["cycleway:left"].isin(["share_busway", "opposite_share_busway"])
            )
        )
    )

    mask_q41 = (
        (
            # A - Les cas où la voie est à sens unique
            (df["oneway"] == "-1")
            & (
                (
                    # A1 - Soit il s'agit de voies de bus indépendantes
                    (df["highway"] == "service")
                    & (df["psv"].isin(["yes"]) | df["bus"].isin(["yes"]))
                    & ((df["access"] == "no") | (df["motor_vehicle"] == "no"))
                    & (
                        (df["bicycle"].notnull() & (df["bicycle"] != "no"))
                        | (df["cycleway"] == "share_busway")
                    )
                )
                | (
                    # A2 - Soit des voies de bus rattachées à une route en sens unique
                    (df["cycleway"] == "share_busway")
                    & (df["busway"].notnull() & (df["busway"] != "no"))
                )
            )
        )
        | (
            # Soit il s'agit de voies de bus guidée ouverte aux vélos
            (df["highway"] == "bus_guideway")
            & (
                (df["bicycle"].notnull() & (df["bicycle"] != "no"))
                | (df["cycleway"] == "share_busway")
                | (df["cycleway:left"] == "share_busway")
            )
        )
        | (
            # Une voie à sens unique
            (df["oneway"] == "yes")
            & (
                (df["cycleway"].isin(["share_busway", "opposite_share_busway"]))
                & (df["busway"] == "opposite_lane")
            )
        )
        | (
            # B1 - Le côté est signalé uniquement sur le tag busway
            (df["cycleway"] == "share_busway")
            & (
                (df["busway:left"].notnull() & (df["busway:left"] != "no"))
                & ((df["busway:right"].isnull()) | (df["busway:right"] == "no"))
            )
        )
        | (
            # B2 - Le côté est signalé sur le tag cycleway
            (df["cycleway:left"].isin(["share_busway", "opposite_share_busway"]))
            & (
                (df["cycleway:right"].isnull())
                | ~df["cycleway:right"].isin(["share_busway", "opposite_share_busway"])
            )
        )
    )

    mask_q42 = (
        # Cas 1 : Rue à sens unique avec voies vélo spécifiées
        df["oneway"].isin(["yes", "-1"])
        & (
            (
                (df["cycleway:right"].isin(["share_busway", "opposite_share_busway"]))
                & (df["cycleway:left"].isin(["share_busway", "opposite_share_busway"]))
            )
            | (df["cycleway"].isin(["share_busway", "opposite_share_busway"]))
        )
        & (df["busway:right"].notnull() & (df["busway:right"] != "no"))
        & (df["busway:left"].notnull() & (df["busway:left"] != "no"))
    ) | (
        # Cas 2 : Route non à sens unique
        (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
        & (
            # A1 : Vélos ont accès à la voie bus
            (
                df["cycleway"].isin(["share_busway"])
                & (
                    (df["busway"] != "no")
                    | ((df["busway:right"] != "no") & (df["busway:left"] != "no"))
                )
            )  # A2 : Les deux voies vélo sont spécifiées
            | (
                (df["cycleway:right"].isin(["share_busway"]))
                & (df["cycleway:left"].isin(["share_busway"]))
                & (df["busway:right"].notnull() & (df["busway:right"] != "no"))
                & (df["busway:left"].notnull() & (df["busway:left"] != "no"))
            )  # B : Bus empruntent des voies indépendantes accessibles aux vélos
            | (
                (df["highway"] == "service")
                & (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
                & (
                    (df["psv"].notnull() & (df["psv"] != "no"))
                    | (df["bus"].notnull() & (df["bus"] != "no"))
                )
                & ((df["access"] == "no") | (df["motor_vehicle"] == "no"))
                & (
                    (df["bicycle"].notnull() & (df["bicycle"] != "no"))
                    | (df["cycleway"] == "share_busway")
                    | (
                        (df["cycleway:right"] == "share_busway")
                        & (df["cycleway:left"] == "share_busway")
                    )
                )
            )  # Cas des bus guideway
            | (
                (df["highway"] == "bus_guideway")
                & (
                    (df["bicycle"].notnull() & (df["bicycle"] != "no"))
                    | (df["cycleway"] == "share_busway")
                    | (
                        (df["cycleway:right"] == "share_busway")
                        & (df["cycleway:left"] == "share_busway")
                    )
                )
            )
        )
    )

    mask_q43 = (
        df["oneway"].isin(["yes", "-1"]) | df["oneway:bicycle"].isin(["yes", "-1"])
    ) & (
        (df["highway"] == "path")
        & (df["bicycle"] == "designated")
        & (df["foot"] == "designated")
    )

    mask_q44 = (
        (df["oneway"].isnull() | (df["oneway"] == "no"))
        & (df["oneway:bicycle"].isnull() | (df["oneway:bicycle"] == "no"))
    ) & (
        (df["highway"] == "path")
        & (df["bicycle"] == "designated")
        & (df["foot"] == "designated")
    )

    mask_q45 = (
        (df["maxspeed"] == "30")
        & ((df["maxspeed:type"] != "CH:zone30"))
        & (df["oneway"].isin(["yes", "-1"]))
        & (df["bicycle"].isnull() | (df["bicycle"] != "no"))
    )

    mask_q46 = (
        (df["maxspeed"] == "30")
        & ((df["maxspeed:type"] != "CH:zone30"))
        &
        # Condition 3 : "oneway" est NULL ou 'no'
        (df["oneway"].isnull() | (df["oneway"] == "no"))
        &
        # Condition 4 : "bicycle" est NULL ou n'est pas 'no'
        (df["bicycle"].isnull() | (df["bicycle"] != "no"))
    )

    mask_q47 = (
        # Condition 1 : "oneway" est 'yes' ou '-1'
        (df["oneway"].isin(["yes", "-1"]))
        &
        # Condition 2 : soit "highway" est 'living_street', soit des tags spécifiques sont définis
        (
            (df["highway"] == "living_street")
            | (
                # "maxspeed" est '20' et "zone:maxspeed" ou "source:maxspeed" contient 'FR:20' ou 'FR:zone20'
                (df["maxspeed"] == "20")
                & ((df["maxspeed:type"] == "CH:zone20"))
            )
        )
    )

    mask_q48 = (
        # Condition 1 : La voie est à double sens
        (df["oneway"].isnull() | (df["oneway"] == "no"))
        &
        # Condition 2 : Soit la voie est de type 'living_street', soit certaines conditions sont remplies
        (
            (df["highway"] == "living_street")
            | (
                # "maxspeed" est '20' et "zone:maxspeed" ou "source:maxspeed" contient 'FR:20' ou 'FR:zone20'
                (df["maxspeed"] == "20")
                & (df["maxspeed:type"] == "CH:zone20")
            )
        )
    )

    mask_q49 = (
        # Condition 1 : Une route explicitement à double sens
        (
            (df["oneway"].isnull() | (df["oneway"] == "no"))
            & (
                df["junction"].isnull()
                | ~df["junction"].isin(["roundabout", "circular"])
            )
        )
        &
        # Condition 2 : Soit une bande cyclable classique ou des bandes cyclables des deux côtés
        (
            (df["cycleway"] == "lane")
            | ((df["cycleway:right"] == "lane") & (df["cycleway:left"] == "lane"))
            | (df["cycleway:both"] == "lane")
        )
        &
        # Condition 3 : La route ne comporte qu'une seule voie
        (df["lanes"] == "1")
    )

    mask_q50 = (
        # Condition 1 : La voie est un escalier
        (df["highway"] == "steps")
        &
        # Condition 2 : Avec une goulotte pour vélos à droite
        (df["ramp:bicycle"] == "yes")
    )

    mask_q51 = (
        # Condition 1 : La voie est à sens unique pour les voitures ou les vélos
        (df["oneway"].isin(["yes", "-1"]) | df["oneway:bicycle"].isin(["yes", "-1"]))
        &
        # Condition 2 : Cas des footways ou paths tolérés aux vélos
        (
            (
                (df["highway"] == "footway")
                & (df["footway"].isnull() | ~df["footway"].isin(["sidewalk"]))
                & (df["bicycle"] == "permissive")
            )
            | ((df["highway"] == "path") & (df["bicycle"] == "permissive"))
        )
        &
        # Condition 3 : Revêtement circulable ou inconnu
        (
            (
                (
                    df["surface"].isin(
                        [
                            "paved",
                            "asphalt",
                            "concrete",
                            "concrete:plates",
                            "concrete:lanes",
                            "paving_stones",
                            "sett",
                            "unhewn_cobblestone",
                            "cobblestone",
                            "metal",
                            "wood",
                            "unpaved",
                            "compacted",
                            "fine_gravel",
                            "gravel",
                            "pebblestone",
                            "ground",
                            "tartan",
                            "clay",
                            "metal_grid",
                        ]
                    )
                    | df["surface"].isnull()
                )
                & (
                    df["smoothness"].isnull()
                    | ~df["smoothness"].isin(
                        ["bad", "very_bad", "horrible", "very_horrible", "impassable"]
                    )
                )
                & (
                    df["tracktype"].isnull()
                    | ~df["tracktype"].isin(["grade3", "grade4", "grade5"])
                )
            )
        )
    )

    mask_q52 = (
        # Condition 1 : La voie n'est pas à sens unique pour les voitures ou les vélos
        (df["oneway"].isnull() | ~df["oneway"].isin(["yes", "-1"]))
        & (df["oneway:bicycle"].isnull() | ~df["oneway:bicycle"].isin(["yes", "-1"]))
        &
        # Condition 2 : Cas des footways ou paths tolérés aux vélos
        (
            (
                (df["highway"] == "footway")
                & (df["footway"].isnull() | ~df["footway"].isin(["sidewalk"]))
                & (df["bicycle"] == "permissive")
            )
            | ((df["highway"] == "path") & (df["bicycle"] == "permissive"))
        )
        &
        # Condition 3 : Revêtement circulable ou inconnu
        (
            (
                (
                    df["surface"].isin(
                        [
                            "paved",
                            "asphalt",
                            "concrete",
                            "concrete:plates",
                            "concrete:lanes",
                            "paving_stones",
                            "sett",
                            "unhewn_cobblestone",
                            "cobblestone",
                            "metal",
                            "wood",
                            "unpaved",
                            "compacted",
                            "fine_gravel",
                            "gravel",
                            "pebblestone",
                            "ground",
                            "tartan",
                            "clay",
                            "metal_grid",
                        ]
                    )
                    | df["surface"].isnull()
                )
                & (
                    df["smoothness"].isnull()
                    | ~df["smoothness"].isin(
                        ["bad", "very_bad", "horrible", "very_horrible", "impassable"]
                    )
                )
                & (
                    df["tracktype"].isnull()
                    | ~df["tracktype"].isin(["grade3", "grade4", "grade5"])
                )
            )
        )
    )

    df["info"] = "autres routes"
    df["info_regrouped"] = "autres routes"

    df.loc[mask_q1, "info"] = "Accotement cyclable à droite"
    df.loc[mask_q1, "info_regrouped"] = "Accotement cyclable"

    df.loc[mask_q2, "info"] = "Accotement cyclable à gauche"
    df.loc[mask_q2, "info_regrouped"] = "Accotement cyclable"

    df.loc[mask_q3, "info"] = "Accotement cyclables des 2 côtés"
    df.loc[mask_q3, "info_regrouped"] = "Accotement cyclable"

    df.loc[mask_q4, "info"] = "Autre chemin piéton autorisé aux vélos 1x"
    df.loc[mask_q4, "info_regrouped"] = "Autre chemin piéton autorisé aux vélos"

    df.loc[mask_q5, "info"] = "Autre chemin piéton autorisé aux vélos 2x"
    df.loc[mask_q5, "info_regrouped"] = "Autre chemin piéton autorisé aux vélos"

    df.loc[mask_q6, "info"] = "Bande cyclable à droite"
    df.loc[mask_q6, "info_regrouped"] = "Bande cyclable"

    df.loc[mask_q7, "info"] = "Bande cyclable à gauche"
    df.loc[mask_q7, "info_regrouped"] = "Bande cyclable"

    df.loc[mask_q8, "info"] = "Bande cyclable des 2 côtés"
    df.loc[mask_q8, "info_regrouped"] = "Bande cyclable"

    df.loc[mask_q9, "info"] = "Bande cyclable à droite"
    df.loc[mask_q9, "info_regrouped"] = "Bande cyclable"

    df.loc[mask_q10, "info"] = "Bande cyclable à gauche"
    df.loc[mask_q10, "info_regrouped"] = "Bande cyclable"

    df.loc[mask_q11, "info"] = "Cheminement cyclable à droite"
    df.loc[mask_q11, "info_regrouped"] = "Cheminement cyclable"

    df.loc[mask_q12, "info"] = "Cheminement cyclable à gauche"
    df.loc[mask_q12, "info_regrouped"] = "Cheminement cyclable"

    df.loc[mask_q13, "info"] = "Cheminement cyclable des 2 côtés"
    df.loc[mask_q13, "info_regrouped"] = "Cheminement cyclable"

    df.loc[mask_q14, "info"] = "Double-sens cyclable sans bande"
    df.loc[mask_q14, "info_regrouped"] = "Double-sens cyclable"

    df.loc[mask_q15, "info"] = "Double-sens cyclable_en_bande à droite"
    df.loc[mask_q15, "info_regrouped"] = "Double-sens cyclable"

    df.loc[mask_q16, "info"] = "Double-sens cyclable en bande à gauche"
    df.loc[mask_q16, "info_regrouped"] = "Double-sens cyclable"

    df.loc[mask_q17, "info"] = "Double-sens cyclable piste à droite"
    df.loc[mask_q17, "info_regrouped"] = "Double-sens cyclable"

    df.loc[mask_q18, "info"] = "Double-sens cyclable piste à gauche"
    df.loc[mask_q18, "info_regrouped"] = "Double-sens cyclable"

    df.loc[mask_q18, "info"] = "Double-sens cyclable piste à gauche"
    df.loc[mask_q18, "info_regrouped"] = "Double-sens cyclable"

    df.loc[mask_q19, "info"] = "Chemin piéton"
    df.loc[mask_q19, "info_regrouped"] = "Chemin piéton"

    df.loc[mask_q20, "info"] = "Chemin piéton des 2 côtés"
    df.loc[mask_q20, "info_regrouped"] = "Chemin piéton"

    df.loc[mask_q21, "info"] = "Limite à 30"
    df.loc[mask_q21, "info_regrouped"] = "Limite à 30"

    df.loc[mask_q22, "info"] = "Limite à 30 des 2 côtés"
    df.loc[mask_q22, "info_regrouped"] = "Limite à 30"

    df.loc[mask_q23, "info"] = "Chemin piéton"
    df.loc[mask_q23, "info_regrouped"] = "Chemin piéton"

    df.loc[mask_q24, "info"] = "Chemin piéton des 2 côtés"
    df.loc[mask_q24, "info_regrouped"] = "Chemin piéton"

    df.loc[mask_q25, "info"] = "Piste cyclable à droite"
    df.loc[mask_q25, "info_regrouped"] = "Piste cyclable"

    df.loc[mask_q26, "info"] = "Piste cyclable à gauche"
    df.loc[mask_q26, "info_regrouped"] = "Piste cyclable"

    df.loc[mask_q27, "info"] = "Piste cyclable des 2 côtés"
    df.loc[mask_q27, "info_regrouped"] = "Piste cyclable"

    df.loc[mask_q28, "info"] = "Piste cyclable à droite (2 voies)"
    df.loc[mask_q28, "info_regrouped"] = "Piste cyclable"

    df.loc[mask_q29, "info"] = "Piste cyclable à gauche (2 voies)"
    df.loc[mask_q29, "info_regrouped"] = "Piste cyclable"

    df.loc[mask_q30, "info"] = "Piste sur trottoir"
    df.loc[mask_q30, "info_regrouped"] = "Piste sur trottoir"

    df.loc[mask_q31, "info"] = "Piste sur trottoir à droite"
    df.loc[mask_q31, "info_regrouped"] = "Piste sur trottoir"

    df.loc[mask_q32, "info"] = "Piste sur trottoir à gauche"
    df.loc[mask_q32, "info_regrouped"] = "Piste sur trottoir"

    df.loc[mask_q33, "info"] = "Piste sur trottoir des 2 côtés"
    df.loc[mask_q33, "info_regrouped"] = "Piste sur trottoir"

    df.loc[mask_q34, "info"] = "Route de service / chemin agricole"
    df.loc[mask_q34, "info_regrouped"] = "Route de service / chemin agricole"

    df.loc[mask_q35, "info"] = "Route de service / chemin agricole des 2 côtés"
    df.loc[mask_q35, "info_regrouped"] = "Route de service / chemin agricole"

    df.loc[mask_q36, "info"] = "Trottoir cyclable"
    df.loc[mask_q36, "info_regrouped"] = "Trottoir cyclable"

    df.loc[mask_q37, "info"] = "Trottoir cyclable à droite"
    df.loc[mask_q37, "info_regrouped"] = "Trottoir cyclable"

    df.loc[mask_q38, "info"] = "Trottoir cyclable à gauche"
    df.loc[mask_q38, "info_regrouped"] = "Trottoir cyclable"

    df.loc[mask_q39, "info"] = "Piste sur trottoir"
    df.loc[mask_q39, "info_regrouped"] = "Piste sur trottoir"

    df.loc[mask_q40, "info"] = "Voie bus à droite"
    df.loc[mask_q40, "info_regrouped"] = "Voie bus"

    df.loc[mask_q41, "info"] = "Voie bus à gauche"
    df.loc[mask_q41, "info_regrouped"] = "Voie bus"

    df.loc[mask_q42, "info"] = "Voie bus des 2 côtés"
    df.loc[mask_q42, "info_regrouped"] = "Voie bus"

    df.loc[mask_q43, "info"] = "Voie verte"
    df.loc[mask_q43, "info_regrouped"] = "Voie verte"

    df.loc[mask_q44, "info"] = "Voie verte des 2 côtés"
    df.loc[mask_q44, "info_regrouped"] = "Voie verte"

    df.loc[mask_q45, "info"] = "Zone 30"
    df.loc[mask_q45, "info_regrouped"] = "Zone 30"

    df.loc[mask_q46, "info"] = "Zone 30"
    df.loc[mask_q46, "info_regrouped"] = "Zone 30"

    df.loc[mask_q47, "info"] = "Zone de rencontre"
    df.loc[mask_q47, "info_regrouped"] = "Zone de rencontre"

    df.loc[mask_q48, "info"] = "Zone de rencontre"
    df.loc[mask_q48, "info_regrouped"] = "Zone de rencontre"

    df.loc[mask_q49, "info"] = "chaucidou"
    df.loc[mask_q49, "info_regrouped"] = "chaucidou"

    df.loc[mask_q50, "info"] = "escalier"
    df.loc[mask_q50, "info_regrouped"] = "escalier"

    df.loc[mask_q51, "info"] = "Chemin piéton"
    df.loc[mask_q51, "info_regrouped"] = "Chemin piéton"

    df.loc[mask_q52, "info"] = "Chemin piéton"
    df.loc[mask_q52, "info_regrouped"] = "Chemin piéton"

    return df
