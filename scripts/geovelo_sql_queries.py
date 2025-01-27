
# line_gpd_clipped.loc[osmid_bike_type[47],"info"]="Zones_rencontre-2x"

# line_gpd_clipped.loc[osmid_bike_type[51],"info"]="escalier-2x"
q52 = """
-- Sont comptabilisés uniquement les escaliers ayant un aménagement pour les vélos

"highway" = 'steps' -- un escalier

AND

(
    "ramp:bicycle" = 'yes' --avec une goulotte pour les vélos sans précision de coté
    OR
    "ramp:bicycle:both" = 'yes'
    OR
    (  --avec une goulotte pour les vélos de chaque coté
        "ramp:bicycle:right" = 'yes'
        AND
        "ramp:bicycle:left" = 'yes'
    )
)
 """
# line_gpd_clipped.loc[osmid_bike_type[52],"info"]="footway_permissive-1x"
q53 = """(
	"oneway" IN ('yes','-1')
	OR
	"oneway:bicycle" IN ('yes','-1')
)
AND
(
	( --cas des footway tolérées aux vélo (permissive) on ne prend pas les trottoirs
		( "highway" = 'footway' AND ( "footway" IS NULL OR "footway" NOT IN ('sidewalk')))
		AND
		"bicycle" = 'permissive'
	)
	OR
	( --cas des path tolérées aux vélo (permissive)
		"highway" LIKE 'path'
		AND
		"bicycle" = 'permissive'
	)
)
AND
(   -- Elles ont un revetement circulable au VTC vélo de randonnée ou le revetement n'est pas connu
    (
        (
            "surface" IN ('paved','asphalt','concrete','concrete:plates','concrete:lanes','paving_stones','sett','unhewn_cobblestone','cobblestone','metal','wood','unpaved','compacted','fine_gravel','gravel','pebblestone','ground','tartan','clay','metal_grid' )
            OR
            "surface" IS NULL
        )
        AND
        (
            "smoothness" NOT IN ('bad','very_bad','horrible','very_horrible','impassable')
            OR
            "smoothness" IS NULL
        )
        AND
        (
            "tracktype" NOT iN ('grade3','grade4','grade5')
            OR
            "tracktype" IS NULL
        )
    )
)

 """
# line_gpd_clipped.loc[osmid_bike_type[53],"info"]="footway_permissive-2x"
q54 = """(
	( "oneway" IS NULL OR "oneway" NOT IN ('yes','-1'))
	AND
	( "oneway:bicycle" IS NULL OR "oneway" NOT IN ('yes','-1'))
)
AND
(
	( --cas des footway tolérées aux vélo (permissive) on ne prend pas les trottoirs
		( "highway" = 'footway' AND ( "footway" IS NULL OR "footway" NOT IN ('sidewalk')))
		AND
		"bicycle" = 'permissive'
	)
	OR
	( --cas des path tolérées aux vélo (permissive)
		"highway" = 'path'
		AND
		"bicycle" = 'permissive'
	)
)
AND
(   -- Elles ont un revetement circulable au VTC vélo de randonnée ou le revetement n'est pas connu
    (
        (
            "surface" IN ('paved','asphalt','concrete','concrete:plates','concrete:lanes','paving_stones','sett','unhewn_cobblestone','cobblestone','metal','wood','unpaved','compacted','fine_gravel','gravel','pebblestone','ground','tartan','clay','metal_grid' )
            OR
            "surface" IS NULL
        )
        AND
        (
            "smoothness" NOT IN ('bad','very_bad','horrible','very_horrible','impassable')
            OR
            "smoothness" IS NULL
        )
        AND
        (
            "tracktype" NOT iN ('grade3','grade4','grade5')
            OR
            "tracktype" IS NULL
        )
    )
)
 """
# line_gpd_clipped.loc[osmid_bike_type[54],"info"]="velorue-1x"
q55 = """(
    "cyclestreet" = 'yes'
    OR
    "bicycle_road" = 'yes'
)

AND "oneway" IN ('yes','-1')

AND
(
	"bicycle" IS NULL
	OR
	"bicycle" NOT IN ('no')
)
 """
# line_gpd_clipped.loc[osmid_bike_type[55],"info"]="velorue-2x"
q56 = """(
    "cyclestreet" = 'yes'
    OR
    "bicycle_road" = 'yes'
)
AND
(
	"oneway" IS NULL
	OR
	"oneway" LIKE 'no'
)
AND
(
	"bicycle" IS NULL
	OR
	"bicycle" NOT IN ('no')
)
"""

# all network 1x

q57 = """-- Seul le sens voiture est pris en compte

    "oneway" IS NULL

    OR

    "oneway" LIKE 'no'

 """

# all network 2x

q58 = """-- Seul le sens voiture est pris en compte

"oneway" IN ('yes','-1')

 """

# all in a array

queries = [
    q1,
    q2,
    q3,
    q4,
    q5,
    q6,
    q7,
    q8,
    q9,
    q10,
    q11,
    q12,
    q13,
    q14,
    q15,
    q16,
    q17,
    q18,
    q19,
    q20,
    q21,
    q22,
    q23,
    q24,
    q25,
    q26,
    q27,
    q28,
    q29,
    q30,
    q31,
    q32,
    q33,
    q34,
    q35,
    q36,
    q37,
    q38,
    q39,
    q40,
    q41,
    q42,
    q43,
    q44,
    q45,
    q46,
    q47,
    q48,
    q49,
    q50,
    q51,
    q52,
    q53,
    q54,
    q55,
    q56,
    q57,
    q58,
]
