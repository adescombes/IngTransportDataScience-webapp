## All SQL queries from geovel

# Attention syntaxe :
# line_gpd_clipped.loc[osmid_bike_type[ N ] ...
# q_N+1


# line_gpd_clipped.loc[osmid_bike_type[0],"info"]="Accotements_cyclables-1xD"
q0 = """
-- Les accotements cyclables comptées une fois sont :
(	-- Soit qui ne sont que d'un coté d'une route à double sens et sont à sens uniques
	(	-- voies à double sens
		"oneway" IS NULL
		OR
		"oneway" NOT IN ('yes','-1')
	)
	AND
	(	--bande cyclable d'un seul côté
		(	-- seulement à droite
			"cycleway:right"='shoulder'
			AND
			(	-- pas à gauche
				"cycleway:left" IS NULL
				OR
				"cycleway:left" NOT IN ('shoulder')
			)
		)
	)
)

OR
(	-- Soit qui ne sont que du coté de circulation des routes à sens unique 
	(	-- route à sens unique (avec yes)
		(
			"oneway"='yes'
			OR
			"junction" IN ('roundabout','circular')
		)
		AND
		(
			(--avec un accotement cyclable
				"cycleway"='shoulder'
					OR
				"cycleway:right"='shoulder'
			)
				
		)
	)
	OR
	(	-- route à sens unique (avec -1)
		"oneway"='-1'
		AND
		(
			"cycleway:left"='shoulder' --avec une bande cyclable (obligatoirement left sinon il s'agit d'un double-sens cyclable)

		)
	)
)
"""
# line_gpd_clipped.loc[osmid_bike_type[1],"info"]="Accotements_cyclables-1xG"
q1 = """-- Les accotements cyclables comptées une fois sont :

(	-- Soit qui ne sont que d'un coté d'une route à double sens et sont à sens uniques
	(	-- voies à double sens
		"oneway" IS NULL
		OR
		"oneway" NOT IN ('yes','-1')
	)
	AND
	(	--bande cyclable d'un seul côté
		(	-- seulement à gauche
			"cycleway:left"='shoulder'
			AND
			(	--pas à droite
				"cycleway:right" IS NULL
				OR
				"cycleway:right" NOT IN ('shoulder')
			)
		)
	)
)

OR
(	-- Soit qui ne sont que du coté de circulation des routes à sens unique (obligatoirement left sinon il s'agit d'un double-sens cyclable)
	(	-- route à sens unique (avec yes)
		(
			"oneway"='yes'
			OR
			"junction" IN ('roundabout','circular')
		)
		AND
		( --cas d'une bande a gauche du sens de circulation mais dans le sens de circulation
			(
				"cycleway:left" LIKE 'shoulder'
			)
		)
	)
	OR
	(	-- route à sens unique (avec -1)
		"oneway"='-1'
		AND
		(
			 --cas d'une bande a gauche du sens de circulation mais dans le sens de circulation
			(
				"cycleway:left" LIKE 'shoulder'
				OR
				"cycleway"='shoulder'
			)
		)
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[2],"info"]="Accotements_cyclables-2x"
q2 = """(	-- Soit
	(	-- une route à double sens
		(
			"oneway" IS NULL
			OR
			"oneway" LIKE 'no'
		)
		AND
		(
			"junction" IS NULL
			OR
			"junction" NOT IN ('roundabout','circular')
		)
	)
	AND --et qui a
	(	-- soit une bande cyclable classique
		"cycleway" = 'shoulder'
		OR
		(	-- soit une bande cyclable à droite et à gauche quelque soit le sens
			"cycleway:right" = 'shoulder'
			AND "cycleway:left" = 'shoulder'
		)
		OR	-- soit une bande cyclable à droite et à gauche quelque soit le sens
		"cycleway:both" = 'shoulder'
	)
)

 """
# line_gpd_clipped.loc[osmid_bike_type[3],"info"]="Autres_chemins_piéton_autorisé_aux_vélos-1x"
q3 = """(
	"oneway" IN ('yes','-1')
	OR
	"oneway:bicycle" IN ('yes','-1')
)
AND
(
	( --cas des footway autorisé aux vélo mais pas (designated) on ne prend pas les trottoirs
		( "highway" LIKE 'footway' AND ( "footway" IS NULL OR "footway" NOT IN ('sidewalk')))
		AND
		"bicycle" IN ('yes','destination')
	)
	OR
	( --cas des path qui ne sont ni des voies verte et ou le vélo n'est pas (designated) ou interdit
		"highway" LIKE 'path'
		AND
		"bicycle" IN ('yes','destination')
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
# line_gpd_clipped.loc[osmid_bike_type[4],"info"]="Autres_chemins_piéton_autorisé_aux_vélos-2x"
q4 = """(
	( "oneway" IS NULL OR "oneway" NOT IN ('yes','-1'))
	AND
	( "oneway:bicycle" IS NULL OR "oneway" NOT IN ('yes','-1'))
)
AND
(
	( --cas des footway autorisé aux vélo mais pas (designated) on ne prend pas les trottoirs
		( "highway" = 'footway' AND ( "footway" IS NULL OR "footway" NOT IN ('sidewalk')))
		AND
		"bicycle" IN ('yes','destination')
	)
	OR
	( --cas des path qui ne sont ni des voies verte et ou le vélo n'est pas (designated) ou interdit
		"highway" = 'path'
		AND
		"bicycle" IN ('yes','destination')
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
# line_gpd_clipped.loc[osmid_bike_type[5],"info"]="Bandes_cyclables-1xD"
q5 = """-- Les bandes cyclables comptées une fois (et qui ne sont pas des doubles-sens cyclables) sont :

(	-- Soit qui ne sont que d'un coté d'une route à double sens et sont à sens uniques
	(	-- voies à double sens
		"oneway" IS NULL
		OR
		"oneway" NOT IN ('yes','-1')
	)
	AND
	(	--bande cyclable d'un seul côté
		(	-- seulement à droite
			"cycleway:right"='lane'
			AND
			(	-- pas à gauche
				"cycleway:left" IS NULL
				OR
				"cycleway:left" NOT IN ('lane')
			)
			AND
			(	-- et pas à double sens
				"cycleway:right:oneway" IS NULL
				OR
				"cycleway:right:oneway" NOT LIKE 'no'
			)
		)
	)
)

OR
(	-- Soit qui ne sont que du coté de circulation des routes à sens unique 
	(	-- route à sens unique (avec yes)
		(
			"oneway"='yes'
			OR
			"junction" IN ('roundabout','circular')
		)
		AND
		(
			(--avec une bande cyclable
				"cycleway"='lane'
					OR
				"cycleway:right"='lane'
			)
			AND
			( --et pas a double sens 
				"cycleway:right:oneway" NOT LIKE 'no'
				OR
				"cycleway:right:oneway" IS NULL
			)
				
		)
	)
	OR
	(	-- route à sens unique (avec -1)
		"oneway"='-1'
		AND
		(
			"cycleway:right"='lane' --avec une bande cyclable (obligatoirement left sinon il s'agit d'un double-sens cyclable)
			AND
			(	-- et pas à double sens
				"cycleway:right:oneway" IS NULL
				OR
				"cycleway:right:oneway" NOT LIKE 'no'
			)
			AND
			(	--et pas en en DSC
				"oneway:bicycle" NOT LIKE 'no'
				OR
				"oneway:bicycle" IS NULL
			)
		)
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[6],"info"]="Bandes_cyclables-1xG"
q6 = """ -- Les bandes cyclables comptées une fois (et qui ne sont pas des doubles-sens cyclables) sont :

(	-- Soit qui ne sont que d'un coté d'une route à double sens et sont à sens uniques
	(	-- voies à double sens
		"oneway" IS NULL
		OR
		"oneway" NOT IN ('yes','-1')
	)
	AND
	(	--bande cyclable d'un seul côté
		(	-- seulement à gauche
			"cycleway:left"='lane'
			AND
			(	--pas à droite
				"cycleway:right" IS NULL
				OR
				"cycleway:right" NOT IN ('lane')
			)
			AND
			(	-- et pas à double sens
				"cycleway:left:oneway" IS NULL
				OR
				"cycleway:left:oneway" NOT LIKE 'no'
			)
		)
	)
)

OR
(	-- Soit qui ne sont que du coté de circulation des routes à sens unique (obligatoirement left sinon il s'agit d'un double-sens cyclable)
	(	-- route à sens unique (avec yes)
		(
			"oneway"='yes'
			OR
			"junction" IN ('roundabout','circular')
		)
		AND
		( --cas d'une bande a gauche du sens de circulation mais dans le sens de circulation
			(
				"cycleway:left" LIKE 'lane'
				AND
				(   --et pas en DSC
					"oneway:bicycle" NOT LIKE 'no'
					OR
					"oneway:bicycle" IS NULL
				)
				AND
				( --et pas a double sens 
					"cycleway:left:oneway" NOT LIKE 'no'
					OR
					"cycleway:left:oneway" IS NULL
				)
			)
		)
	)
	OR
	(	-- route à sens unique (avec -1)
		"oneway"='-1'
		AND
		(
			 --cas d'une bande a gauche du sens de circulation mais dans le sens de circulation
			(
				"cycleway:left" LIKE 'lane'
				OR
				"cycleway"='lane'
			)
			AND
			( --et pas a double sens 
				"cycleway:left:oneway" NOT LIKE 'no'
				OR
				"cycleway:left:oneway" IS NULL
			)
		)
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[7],"info"]="Bandes_cyclables-2x"
q7 = """(	-- Soit
	(	-- une route à double sens
		(
			"oneway" IS NULL
			OR
			"oneway" LIKE 'no'
		)
		AND
		(
			"junction" IS NULL
			OR
			"junction" NOT IN ('roundabout','circular')
		)
	)
	AND --et qui a
	(	-- soit une bande cyclable classique
		"cycleway" IN ('lane' , 'opposite_lane')
		OR
		(	-- soit une bande cyclable à droite et à gauche quelque soit le sens
			"cycleway:right" IN ('lane','opposite_lane')
			AND "cycleway:left" IN ('lane','opposite_lane')
		)
		OR	-- soit une bande cyclable à droite et à gauche quelque soit le sens
		"cycleway:both" IN ('lane','opposite_lane')
	)
)

"""
# line_gpd_clipped.loc[osmid_bike_type[8],"info"]="Bandes_cyclables-2xD"
q8 = """ --Soit
	(	-- une route à sens unique ou non, quand la bande de droite est à double sens
		"cycleway:right" IN ('lane','opposite_lane')
		AND
		"cycleway:right:oneway" LIKE 'no'
	)
"""
# line_gpd_clipped.loc[osmid_bike_type[9],"info"]="Bandes_cyclables-2xG"
q9 = """--Soit
	(	-- une route à sens unique ou non, quand la bande de gauche est à double sens
		"cycleway:left" IN ('lane','opposite_lane')
		AND
		"cycleway:left:oneway" LIKE 'no'
	)
"""
# line_gpd_clipped.loc[osmid_bike_type[10],"info"]="Cheminements_cyclables-1xD" -> Chaussée partagée
q10 = """ -- Les cheminements cyclables comptées une fois sont :

(	-- Soit qui ne sont que d'un coté d'une route à double sens et sont à sens uniques
	(	-- voies à double sens
		"oneway" IS NULL
		OR
		"oneway" NOT IN ('yes','-1')
	)
	AND
	(	--cheminement cyclable d'un seul côté
		(	-- seulement à droite
			"cycleway:right"='shared_lane'
			AND
			(	-- pas à gauche
				"cycleway:left" IS NULL
				OR
				"cycleway:left" NOT IN ('shared_lane')
			)
		)
	)
)

OR
(	-- Soit qui ne sont que du coté de circulation des routes à sens unique
	(	-- route à sens unique (avec yes)
		(
			"oneway"='yes'
			OR
			"junction" IN ('roundabout','circular')
		)
		AND
		(
			(--avec un cheminement cyclable
				"cycleway"='shared_lane'
					OR
				"cycleway:right"='shared_lane'
			)

		)
	)
	OR
	(	-- route à sens unique (avec -1)
		"oneway"='-1'
		AND
		(
			"cycleway:left"='shared_lane' --avec une bande cyclable (obligatoirement left sinon il s'agit d'un double-sens cyclable)

		)
	)
)
"""
# line_gpd_clipped.loc[osmid_bike_type[11],"info"]="Cheminements_cyclables-1xG" -> Chaussée partagée
q11 = """ -- Les cheminements cyclables comptées une fois sont :

(	-- Soit qui ne sont que d'un coté d'une route à double sens et sont à sens uniques
	(	-- voies à double sens
		"oneway" IS NULL
		OR
		"oneway" NOT IN ('yes','-1')
	)
	AND
	(	--cheminement cyclable d'un seul côté
		(	-- seulement à gauche
			"cycleway:left"='shared_lane'
			AND
			(	--pas à droite
				"cycleway:right" IS NULL
				OR
				"cycleway:right" NOT IN ('shared_lane')
			)
		)
	)
)

OR
(	-- Soit qui ne sont que du coté de circulation des routes à sens unique (obligatoirement left sinon il s'agit d'un double-sens cyclable)
	(	-- route à sens unique (avec yes)
		(
			"oneway"='yes'
			OR
			"junction" IN ('roundabout','circular')
		)
		AND
		( --cas d'une bande a gauche du sens de circulation mais dans le sens de circulation

            "cycleway:left" LIKE 'shared_lane'
			AND
			(
			    "oneway:bicycle" IS NULL
			    OR
			    "oneway:bicycle" != 'no'
			)
		)
	)
	OR
	(	-- route à sens unique (avec -1)
		"oneway"='-1'
		AND
		(
			 --cas d'une bande a gauche du way mais dans le sens de circulation
			(
				"cycleway:left" LIKE 'shared_lane'
				OR
				"cycleway"='shared_lane'
			)
		)
	)
)
"""
# line_gpd_clipped.loc[osmid_bike_type[12],"info"]="Cheminements_cyclables-2x" -> Chaussée partagée
q12 = """(	-- Soit
	(	-- une route à double sens
		(
			"oneway" IS NULL
			OR
			"oneway" LIKE 'no'
		)
		AND
		(
			"junction" IS NULL
			OR
			"junction" NOT IN ('roundabout','circular')
		)
	)
	AND --et qui a
	(	-- soit une bande cyclable classique
		"cycleway" = 'shared_lane'
		OR
		(	-- soit une bande cyclable à droite et à gauche quelque soit le sens
			"cycleway:right" = 'shared_lane'
			AND "cycleway:left" = 'shared_lane'
		)
		OR	-- soit une bande cyclable à droite et à gauche quelque soit le sens
		"cycleway:both" = 'shared_lane'
	)
)

"""
# line_gpd_clipped.loc[osmid_bike_type[13],"info"]="Double-sens_cyclables_sans_bande"
q13 = """-- Soit tagué avec le schema opposite

(	-- une route à sens unique
	"oneway" IN ('yes','-1')
	AND
	(	-- qui a un contre-sens à gauche
		"cycleway" = 'opposite'
		OR	-- ou qui a un contre-sens à gauche explicite
		"cycleway:left" = 'opposite'
		OR	-- qui a un contre-sens à droite explicite
		"cycleway:right" = 'opposite'
	)
)

-- Soit tagué avec oneway:bicycle=no en distinguant oneway=yes et oneway=-1

OR
(	-- Une route à sense unique taguée avec oneway=yes
	"oneway" = 'yes'
	AND -- qui n'est pas à sens unique pour les vélo
	"oneway:bicycle" = 'no'
	AND 
	(	-- qui n'a pas d'autres informations concernant des aménagements cyclables
		(	-- qui n'a pas de bande cyclable ou de piste cyclable à contre-sens
			"cycleway" IS NULL
			OR 
			"cycleway" IN ('no','shared_lane')
		)
		AND
		(	-- qui n'a pas de bande cyclable à contre sens
			"cycleway:left" IS NULL
			OR
			"cycleway:left" IN ('no','shared_lane')
		)
		AND
		(	-- qui n'a pas de banse cyclable de chaque côté explicitement
			"cycleway:both" IS NULL
			OR
			"cycleway:both" IN ('no','shared_lane')
		)
		AND
		(  -- qui n'a pas de piste a droite à double sens
		    "cycleway:right:oneway" IS NULL
		    OR
		    "cycleway:right:oneway" != 'no'
		)
	)
)
OR
(
	"oneway" IN ('-1')
	AND
	"oneway:bicycle" = 'no'
	AND 
	(
		(
			"cycleway" IS NULL
			OR 
			"cycleway" IN ('no','shared_lane')
		)
		AND
		(
			"cycleway:right" IS NULL
			OR
			"cycleway:right" IN ('no','shared_lane')
		)
		AND
		(
			"cycleway:both" IS NULL
			OR
			"cycleway:both" IN ('no','shared_lane')
		)
		AND
		(  -- qui n'a pas de piste a droite à double sens
		    "cycleway:left:oneway" IS NULL
		    OR
		    "cycleway:left:oneway" != 'no'
		)
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[14],"info"]="Doubles-sens_cyclables_en_bande-D"
q14 = """ -- Double-sens cyclables avec bandes (compter une fois)

-- Cas pour les opposite_lane

(	-- Une route à sens unique
	"oneway" IN ('yes','-1')
	AND
	(	-- qui a un DSC expicitement à droite
		"cycleway:right" LIKE 'opposite_lane'
	)		
)
OR
(	-- Une route à sens unique taguée avec oneway=-1
	"oneway" LIKE '-1'
	AND
	(
		"cycleway" = 'opposite_lane'
		OR
		(	-- qui a une bande cyclable à droite implicitement à contre sens du fait du -1
			"cycleway:right" LIKE 'lane'
			AND
			"oneway:bicycle" LIKE 'no'
			AND
			(	--et qui n'est pas à double sens 
				"cycleway:right:oneway" IS NULL
				OR
				"cycleway:right:oneway" NOT LIKE 'no'
			)	
		)
		OR
		(	-- qui a une bande cyclable à droite et à gauche et donc implicitement à contre sens
			"cycleway:both" LIKE 'lane'
			AND
			"oneway:bicycle" LIKE 'no'
		)
	)
)
"""
# line_gpd_clipped.loc[osmid_bike_type[15],"info"]="Doubles-sens_cyclables_en_bande-G"
q15 = """ -- Double-sens cyclables avec bandes (compter une fois)

-- Cas pour les opposite_lane

(	-- Une route à sens unique
	"oneway" IN ('yes','-1')
	AND
	(	-- qui a une bande cyclable expicitement à contre sens
		"cycleway:left" LIKE 'opposite_lane'
	)		
)
		

OR
(	-- Une route à sens unique taguée avec oneway=yes
	"oneway" LIKE 'yes'
	AND
	(
		"cycleway" = 'opposite_lane'
		OR
		(		-- qui a une bande cyclable à gauche implicitement à contre sens
			"cycleway:left" LIKE 'lane'
			AND
			"oneway:bicycle" LIKE 'no'
			AND
			(	--et pas en double sens
				"cycleway:left:oneway" IS NULL
				OR
				"cycleway:left:oneway" NOT LIKE 'no'
			)
		)
		OR
		(	-- qui a une bande cyclable à droite et à gauche et donc implicitement à contre sens
			"cycleway:both" LIKE 'lane'
			AND
			"oneway:bicycle" LIKE 'no'
		)
		
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[16],"info"]="Doubles-sens_cyclables_piste-D"
q16 = """ -- Double-sens cyclables avec bandes (compter une fois)

-- Cas pour les opposite_lane

(	-- Une route à sens unique
	"oneway" IN ('yes', '-1')
	AND
	(	-- qui a un DSC expicitement à droite
		"cycleway:right" LIKE 'opposite_track'
	)		
)
OR
(	-- Une route à sens unique taguée avec oneway=-1
	"oneway" LIKE '-1'
	AND
	(
		"cycleway" = 'opposite_track'
		OR
		(	-- qui a une bande cyclable à droite implicitement à contre sens du fait du -1
			"cycleway:right" LIKE 'track'
			AND
			"oneway:bicycle" LIKE 'no'
			AND
			(	--et qui n'est pas à double sens 
				"cycleway:right:oneway" IS NULL
				OR
				"cycleway:right:oneway" NOT LIKE 'no'
			)	
		)
		OR
		(	-- qui a une bande cyclable à droite et à gauche et donc implicitement à contre sens
			"cycleway:both" LIKE 'track'
			AND
			"oneway:bicycle" LIKE 'no'
		)
	)
)
"""
# line_gpd_clipped.loc[osmid_bike_type[17],"info"]="Doubles-sens_cyclables_piste-G"
q17 = """-- Double-sens cyclables piste (compter une fois)

-- Cas pour les opposite_track

(	-- Une route à sens unique
	"oneway" IN ('yes','-1')
	AND
	(	-- qui a une bande cyclable expicitement à contre sens
		"cycleway:left" LIKE 'opposite_track'
	)		
)
		

OR
(	-- Une route à sens unique taguée avec oneway=yes
	"oneway" LIKE 'yes'
	AND
	(
		"cycleway" = 'opposite_track'
		OR
		(		-- qui a une bande cyclable à gauche implicitement à contre sens
			"cycleway:left" LIKE 'track'
			AND
			"oneway:bicycle" LIKE 'no'
			AND
			(	--et pas en double sens
				"cycleway:left:oneway" IS NULL
				OR
				"cycleway:left:oneway" NOT LIKE 'no'
			)
		)
		OR
		(	-- qui a une bande cyclable à droite et à gauche et donc implicitement à contre sens
			"cycleway:both" LIKE 'track'
			AND
			"oneway:bicycle" LIKE 'no'
		)
		
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[18],"info"]="Footway_path_designated-1x"
q18 = """(
	"oneway" IN ('yes','-1')
	OR
	"oneway:bicycle" IN ('yes','-1')
)
AND
(
	(	--cas des footway
		"highway" LIKE 'footway' AND ( "footway" IS NULL OR "footway" NOT IN ('sidewalk'))
		AND
		"bicycle" IN ('designated','official')
	)
	OR
	(	--cas des path, on ne compte pas les voies vertes
		"highway" LIKE 'path'
		AND
		"bicycle" IN ('designated','official')
		AND
		(
			"foot" IS NULL
			OR
			"foot" NOT IN ('designated')
		)
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
# line_gpd_clipped.loc[osmid_bike_type[19],"info"]="Footway_path_designated-2x "
q19 = """ (
	( "oneway" IS NULL OR "oneway" NOT IN ('yes','-1'))
	AND
	( "oneway:bicycle" IS NULL OR "oneway:bicycle" NOT IN ('yes','-1'))
)
AND
(
	(	--cas des footway on ne compte pas les trottoirs
		( "highway" LIKE 'footway' AND ( "footway" IS NULL OR "footway" NOT IN ('sidewalk')))
		AND
		"bicycle" IN ('designated','official')

	)
	OR
	(	--cas des path, on ne compte pas les voies vertes
		"highway" LIKE 'path'
		AND
		"bicycle" IN ('designated','official')
		AND
		(
			"foot" IS NULL
			OR
			"foot" NOT IN ('designated')
		)
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
# line_gpd_clipped.loc[osmid_bike_type[20],"info"]="Limite_a_30"
q20 = """ -- Sont comptabilisés uniquement les voies limitees à 30 et pas les zones 30
-- Seul le sens voiture est pris en compte

"maxspeed" LIKE '30'
AND
(
	( "zone:maxspeed" IS NULL OR "zone:maxspeed" NOT LIKE 'FR:30')
	AND
	( "source:maxspeed" IS NULL OR "source:maxspeed" NOT LIKE 'FR:zone30')
)

"""
# line_gpd_clipped.loc[osmid_bike_type[23],"info"]="Pedestrian"
q21 = """-- Seul le sens voiture est pris en compte

"highway" LIKE 'pedestrian'

AND
(
	"bicycle" IS NULL
	OR
	"bicycle" NOT IN ('no')
)
 """

# line_gpd_clipped.loc[osmid_bike_type[24],"info"]="Pistes_cyclables-1xD."
q22 = """ (-- A - Soit la piste cyclable est séparée et à sens unique
	"oneway" IN ('yes')
	AND
	"highway" LIKE 'cycleway'
)

OR
(
	(	-- soit la piste cyclable est à droite de manière explicite sur une voie a double sens )
		"cycleway:right" IN ('track')
		AND
		(	-- et il n'y a pas de piste à gauche
			"cycleway:left" IS NULL
			OR
			"cycleway:left" NOT IN ('track','opposite_track')
		)
		AND
		(	-- et la piste de droite est bien à sens unique
			"cycleway:right:oneway" IS NULL
			OR
			"cycleway:right:oneway" NOT LIKE 'no'
		)
	)
	OR
	(	-- Soit qui ne sont que du coté de circulation des routes à sens unique
		(  -- route à sens unique (avec yes)
			"oneway"='yes'
		)
		AND
		(
			(--avec une bande cyclable
				"cycleway"='track'
					OR
				"cycleway:right"='track'
			)
			AND
			( --et pas a double sens 
				"cycleway:right:oneway" NOT LIKE 'no'
				OR
				"cycleway:right:oneway" IS NULL
			)
				
		)
	)
	OR
	(	-- route à sens unique (avec -1)
		"oneway"='-1'
		AND
		(
			"cycleway:right"='track' --avec une bande cyclable (obligatoirement left sinon il s'agit d'un double-sens cyclable)
			AND
			(	-- et pas à double sens
				"cycleway:right:oneway" IS NULL
				OR
				"cycleway:right:oneway" NOT LIKE 'no'
			)
			AND
			(	--et pas en en DSC
				"oneway:bicycle" NOT LIKE 'no'
				OR
				"oneway:bicycle" IS NULL
			)
		)
	)
)
"""
# line_gpd_clipped.loc[osmid_bike_type[25],"info"]="Pistes_cyclables-1xG"
q23 = """(	-- soit la piste cyclable est à gauche de manière implicie
		"cycleway" IN ('track')
		AND
		"oneway" IN ('-1')
)
OR
(-- Soit la piste cyclable est attachée à la route (track)
	(	-- voies à double sens
		"oneway" IS NULL
		OR
		"oneway" NOT IN ('yes','-1')
	)
	AND
	(	--bande cyclable d'un seul côté
		(	-- seulement à gauche
			"cycleway:left"='track'
			AND
			(	--pas à droite
				"cycleway:right" IS NULL
				OR
				"cycleway:right" NOT IN ('track')
			)
			AND
			(	-- et pas à double sens
				"cycleway:left:oneway" IS NULL
				OR
				"cycleway:left:oneway" NOT LIKE 'no'
			)
		)
	)
)

OR
(	-- Soit qui ne sont que du coté de circulation des routes à sens unique (obligatoirement left sinon il s'agit d'un double-sens cyclable)
	(	-- route à sens unique (avec yes)
		(
			"oneway"='yes'
		)
		AND
		( --cas d'une bande a gauche du sens de circulation mais dans le sens de circulation
			(
				"cycleway:left" LIKE 'track'
				AND
				(   --et pas en DSC
					"oneway:bicycle" NOT LIKE 'no'
					OR
					"oneway:bicycle" IS NULL
				)
				AND
				( --et pas a double sens 
					"cycleway:left:oneway" NOT LIKE 'no'
					OR
					"cycleway:left:oneway" IS NULL
				)
			)
		)
	)
	OR
	(	-- route à sens unique (avec -1)
		"oneway"='-1'
		AND
		(
			 --cas d'une bande a gauche du sens de circulation mais dans le sens de circulation
			(
				"cycleway:left" LIKE 'track'
				OR
				"cycleway"='track'
			)
			AND
			( --et pas a double sens 
				"cycleway:left:oneway" NOT LIKE 'no'
				OR
				"cycleway:left:oneway" IS NULL
			)
		)
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[26],"info"]="Pistes_cyclables-2x"
q24 = """(	-- A - Soit la route est à double sens avec des pistes cyclables ratachées de part et d'autre, soit il s'agit d'une piste cyclable indépendante à double sens :
	(	-- la route ou la piste cyclable est à double sens
		"oneway" IS NULL
		OR "oneway" NOT IN ('yes','-1')
	)
	AND	-- et elle est
	(	-- soit une piste cyclable indépendante
		"highway" LIKE 'cycleway'
		OR
		(	-- soit une piste cyclable rattachée à la route (track) de part et d'autre de la route
			"cycleway" IN ('track','opposite_track')
			OR
			"cycleway:both" IN ('track','opposite_track')
			OR
			(
				"cycleway:left" IN ('track','opposite_track')
				AND
				"cycleway:right" IN ('track','opposite_track')
			)
		)
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[27],"info"]="Pistes_cyclables-2xD"
q25 = """-- Une piste cyclable à double sens d'un seul côté de la route (:left/right), rattachée à une route (track) qui peut être à sens unique ou pas :
	(	-- ou la piste peut être à droite
		"cycleway:right" IN ('track','opposite_track')
		AND
		"cycleway:right:oneway" LIKE 'no'
	)
 """
# line_gpd_clipped.loc[osmid_bike_type[28],"info"]="Pistes_cyclables-2xG"
q26 = """ -- Une piste cyclable à double sens d'un seul côté de la route (:left/right), rattachée à une route (track) qui peut être à sens unique ou pas :
	(	-- la piste peut être à gauche
		"cycleway:left" IN ('track','opposite_track')
		AND
		"cycleway:left:oneway" LIKE 'no'
	)

"""
# line_gpd_clipped.loc[osmid_bike_type[29],"info"]="Pistes_sur_Trottoirs-1x"
q27 = """ "segregated" LIKE 'yes'
AND
"highway" LIKE 'footway'
AND
"footway" LIKE 'sidewalk'
AND
"bicycle" NOT LIKE 'no'
AND
(
	"oneway" IN ('yes','-1')
	OR
	"oneway:bicycle" IN ('yes','-1')
)
"""
# line_gpd_clipped.loc[osmid_bike_type[30],"info"]="Pistes_sur_Trottoirs-1xD"
q28 = """( --modélisation avec un way séparé
    "segregated" LIKE 'yes'
    AND
    "highway" LIKE 'footway'
    AND
    "footway" LIKE 'sidewalk'
    AND
    "bicycle" IN ('yes', 'designated', 'official')
    AND
    (
        "oneway" = 'yes'
        OR
        "oneway:bicycle" = 'yes'
    )
)
OR
(  --modélisation sur la voirie
    (
        "sidewalk" = 'right'
        OR
        "sidewalk" = 'both'
    )
    AND
    (
        "sidewalk:right:bicycle" IN ('yes', 'designated', 'official')
        AND
        (
           "sidewalk:left:bicycle" IS NULL
           OR
           "sidewalk:left:bicycle" = 'no'
        )
    )
    AND
    (
        "sidewalk:segregated" = 'yes'
        OR
        "sidewalk:right:segregated" = 'yes'
    )
)
 """
# line_gpd_clipped.loc[osmid_bike_type[31],"info"]="Pistes_sur_Trottoirs-1xG"
q29 = """( --modélisation avec un way séparé
    "segregated" LIKE 'yes'
    AND
    "highway" LIKE 'footway'
    AND
    "footway" LIKE 'sidewalk'
    AND
    "bicycle" IN ('yes', 'designated', 'official')
    AND
    (
        "oneway" = '-1'
        OR
        "oneway:bicycle" = '-1'
    )
)
OR
(  --modélisation sur la voirie
    (
        "sidewalk" = 'left'
        OR
        "sidewalk" = 'both'
    )
    AND
    (
        "sidewalk:left:bicycle" IN ('yes', 'designated', 'official')
        AND
        (
           "sidewalk:right:bicycle" IS NULL
           OR
           "sidewalk:right:bicycle" = 'no'
        )
    )
    AND
    (
        "sidewalk:segregated" = 'yes'
        OR
        "sidewalk:left:segregated" = 'yes'
    )
)
 """
# line_gpd_clipped.loc[osmid_bike_type[32],"info"]="Pistes_sur_Trottoirs-2x"
q30 = """( --modélisation avec un way séparé
    "segregated" LIKE 'yes'
    AND
    "highway" LIKE 'footway'
    AND
    "footway" LIKE 'sidewalk'
    AND
    "bicycle" IN ('yes', 'designated', 'official')
    AND
    (
        (
            "oneway" IS NULL
            OR
            "oneway" LIKE 'no'
        )
        AND
        (
            "oneway:bicycle" IS NULL
            OR
            "oneway:bicycle" LIKE 'no'
        )
    )
)
OR
(  --modélisation sur la voirie

    "sidewalk" = 'both'
    AND
    (
        "sidewalk:both:bicycle" IN ('yes', 'designated', 'official')
        OR
        (
           "sidewalk:right:bicycle" IN ('yes', 'designated', 'official')
           AND
           "sidewalk:left:bicycle" IN ('yes', 'designated', 'official')
        )
    )
    AND
    (
        "sidewalk:segregated" = 'yes'
        OR
        "sidewalk:both:segregated" = 'yes'
    )
)
 """
# line_gpd_clipped.loc[osmid_bike_type[33],"info"]="Routes_services_chemins_agricoles-1x"
q31 = """-- Les voies particulières de type track et service

"highway" IN ('track','service','unclasified','residential','tertiary','secondary','primary')
AND
(   -- Elles ont un revetement circulable au VTC vélo de randonnée
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
    AND
    (  -- on veux au moins que l'un des trois tags (surface, smoothness ou tracktype) soit renseigné
        "highway" != 'track'
        OR
        "surface" IS NOT NULL
        OR
        "smoothness" IS NOT NULL
        OR
        "tracktype" IS NOT NULL
    )
)


AND
(	-- et dont l’accès n’est pas autorisé à certains types de véhicules, motorisés
	(
		"psv" IS NULL
		OR
		"psv"='no'
	)
	AND
	(
		"motorcycle" IS NULL
		OR
		"motorcycle"='no'
	)
	AND
	(
		"bus" IS NULL
		OR
		"bus"='no'
	)
)
AND
(	-- et dont
	(	-- soit, l'accès est interdits aux voitures
		(
			"motor_vehicle" IN ('no','forestry','agricultural')
			OR
			"motorcar" IN ('no','forestry','agricultural')
		)
		AND
		(	-- mais n’est pas interdit aux vélos,
			(
				"bicycle" IS NULL
				OR
				"bicycle" NOT LIKE 'no'
			)
			AND
			(
				"access:bicycle" IS NULL
				OR
				"access:bicycle" NOT LIKE 'no'
			)
		)
	)
	OR
	(	-- soit, l'accès est interdits à tous
		"access" IN ('no','forestry','agricultural')
		AND
        ( -- mais est permis aux vélos
            "bicycle" IN ('yes','designated')
            OR
            "access:bicycle" IN ('yes','designated')
        )
        AND
        ( -- et n'est pas explicitement autorisée aux voitures
            "motor_vehicle" IS NULL
            OR
            "motor_vehicle" = 'no'
        )
	)
)
AND
(	-- Et qui sont à sens unique pour les vélos
	"oneway" IN ('yes','-1')
	AND
	(
		"oneway:bicycle" IS NULL
		OR
		"oneway:bicycle" IN ('yes','-1')
	)
	-- il ne peut pas s'agir de double-sens cyclables car il n'y a pas de véhicules à moteur "oneway:bicycle"='no'
)
 """
# line_gpd_clipped.loc[osmid_bike_type[34],"info"]="Routes_services_chemins_agricoles-2x"
q32 = """ -- Les voies particulières de type track et service
"highway" IN ('track','service','unclasified','residential','tertiary','secondary','primary')
AND
(   -- Elles ont un revetement circulable au VTC vélo de randonnée
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
    AND
    (  -- on veux au moins que l'un des trois tags (surface, smoothness ou tracktype) soit renseigné pour les highway = track
        "highway" != 'track'
        OR
        "surface" IS NOT NULL
        OR
        "smoothness" IS NOT NULL
        OR
        "tracktype" IS NOT NULL
    )
)
AND
(	-- et dont l’accès n’est pas autorisé à certains types de véhicules motorisés
	(
		"psv" IS NULL
		OR
		"psv"='no'
	)
	AND
	(
		"motorcycle" IS NULL
		OR
		"motorcycle"='no'
	)
	AND
	(
		"bus" IS NULL
		OR
		"bus"='no'
	)
)
AND
(	-- et dont
	(	-- soit, l'accès est interdits aux voitures
		(
			"motor_vehicle" IN ('no','forestry','agricultural')
			OR
			"motorcar" IN ('no','forestry','agricultural')
		)
		AND
		(	-- mais n’est pas interdit aux vélos,
			(
				"bicycle" IS NULL
				OR
				"bicycle" NOT LIKE 'no'
			)
			AND
			(
				"access:bicycle" IS NULL
				OR
				"access:bicycle" NOT LIKE 'no'
			)
		)
	)
	OR
	(	-- soit, l'accès est interdits à tous
		"access" IN ('no','forestry','agricultural')
		AND
        ( -- mais est permis aux vélos
            "bicycle" IN ('yes','designated')
            OR
            "access:bicycle" IN ('yes','designated')
        )
        AND
        ( -- et n'est pas explicitement autorisée aux voitures
            "motor_vehicle" IS NULL
            OR
            "motor_vehicle" = 'no'
        )
	)
)
AND
(	-- Et qui ne sont pas à sens unique pour les vélos
	(
		"oneway" IS NULL
		OR
		"oneway" NOT IN ('yes','-1')
	)
	AND
	(
		"oneway:bicycle" IS NULL
		OR
		"oneway:bicycle" NOT IN ('yes','-1')
	)
)
"""
# line_gpd_clipped.loc[osmid_bike_type[35],"info"]="Trottoirs_cyclables-1x"
q33 = """("segregated" IS NULL OR "segregated" NOT IN  ('yes'))
AND
"highway" LIKE 'footway'
AND
"footway" LIKE 'sidewalk'
AND
"bicycle" NOT LIKE 'no'
AND
(
	"oneway" IN ('yes','-1')
	OR
	"oneway:bicycle" IN ('yes','-1')
)

 """
# line_gpd_clipped.loc[osmid_bike_type[36],"info"]="Trottoirs_cyclables-1xD"
q34 = """ ( --modélisation avec un way séparé
    ( "segregated" IS NULL OR "segregated" NOT IN  ('yes'))
    AND
    "highway" LIKE 'footway'
    AND
    "footway" LIKE 'sidewalk'
    AND
    "bicycle" IN ('yes', 'designated', 'official')
    AND
    (
        "oneway" = 'yes'
        OR
        "oneway:bicycle" = 'yes'
    )
)
OR
(  --modélisation sur la voirie
    (
        "sidewalk" = 'right'
        OR
        "sidewalk" = 'both'
    )
    AND
    (
        "sidewalk:right:bicycle" IN ('yes', 'designated', 'official')
        AND
        (
           "sidewalk:left:bicycle" IS NULL
           OR
           "sidewalk:left:bicycle" = 'no'
        )
    )
    AND
    (
        (
            "sidewalk:segregated" = 'no'
            OR
            "sidewalk:segregated" IS NULL
        )
        AND
        (
            "sidewalk:right:segregated" = 'yes'
            OR
            "sidewalk:right:segregated" IS NULL
        )
    )
)
"""
# line_gpd_clipped.loc[osmid_bike_type[37],"info"]="Trottoirs_cyclables-1xG"
q35 = """( --modélisation avec un way séparé
    ( "segregated" IS NULL OR "segregated" NOT IN  ('yes'))
    AND
    "highway" LIKE 'footway'
    AND
    "footway" LIKE 'sidewalk'
    AND
    "bicycle" IN ('yes', 'designated', 'official')
    AND
    (
        "oneway" = '-1'
        OR
        "oneway:bicycle" = '-1'
    )
)
OR
(  --modélisation sur la voirie
    (
        "sidewalk" = 'left'
        OR
        "sidewalk" = 'both'
    )
    AND
    (
        "sidewalk:left:bicycle" IN ('yes', 'designated', 'official')
        AND
        (
           "sidewalk:right:bicycle" IS NULL
           OR
           "sidewalk:right:bicycle" = 'no'
        )
    )
    AND
    (
        (
            "sidewalk:segregated" = 'no'
            OR
            "sidewalk:segregated" IS NULL
        )
        AND
        (
            "sidewalk:left:segregated" = 'yes'
            OR
            "sidewalk:left:segregated" IS NULL
        )
    )
)
 """
# line_gpd_clipped.loc[osmid_bike_type[38],"info"]="Trottoirs_cyclables-2x"
q36 = """ ( --modélisation avec un way séparé
    ( "segregated" IS NULL OR "segregated" NOT IN  ('yes'))
    AND
    "highway" LIKE 'footway'
    AND
    "footway" LIKE 'sidewalk'
    AND
    "bicycle" IN ('yes', 'designated', 'official')
    AND
    (
        (
            "oneway" IS NULL
            OR
            "oneway" LIKE 'no'
        )
        AND
        (
            "oneway:bicycle" IS NULL
            OR
            "oneway:bicycle" LIKE 'no'
        )
    )
)
OR
(  --modélisation sur la voirie

    "sidewalk" = 'both'
    AND
    (
        "sidewalk:both:bicycle" IN ('yes', 'designated', 'official')
        OR
        (
           "sidewalk:right:bicycle" IN ('yes', 'designated', 'official')
           AND
           "sidewalk:left:bicycle" IN ('yes', 'designated', 'official')
        )
    )
    AND
    (
        (
            "sidewalk:segregated" = 'no'
            OR
            "sidewalk:segregated" IS NULL
        )
        AND
        (
            "sidewalk:both:segregated" = 'no'
            OR
            "sidewalk:both:segregated" IS NULL
        )
    )
)
"""
# line_gpd_clipped.loc[osmid_bike_type[39],"info"]="Voies_bus-1xD"
q37 = """(	-- A - Les cas où la voie est à sens unique
	"oneway" IN ('yes')
	AND
	(
		(
			(	-- A1 - Soit il s'agit de voies de bus indépendantes :
				"highway" IN ('service') -- des routes de service,
				AND
				(	-- accessibles aux bus,
					"psv" IN ('yes')
					OR
					"bus" IN ('yes')
				)
				AND
				(	-- interdites à tous les autres véhicules,
					"access" LIKE 'no' OR "motor_vehicle" LIKE 'no'
				)
				AND
				(	-- mais authorisées aux vélos.
					(
					"bicycle" IS NOT NULL
					AND
					"bicycle" NOT IN ('no')
					)
					OR
					"cycleway" IN ('share_busway')
				)
			)
		)
		OR
		(	-- A2 - Soit des voies de bus rattachées à une route en sens unique :
			"cycleway" IN ('share_busway') -- un accès pour les vélos à la voie bus
			AND
			(	-- et l'existance d'une voie bus
				"busway" IS NOT NULL
				AND
				"busway" NOT IN ('no','opposite_lane')
			)
		)
        OR
        ( --Soit il s'agit de voies de bus guidée ouverte aux vélo
            "highway" = 'bus_guideway'
            AND
            (	-- mais authorisées aux vélos.
                (
                "bicycle" IS NOT NULL
                AND
                "bicycle" NOT IN ('no')
                )
                OR
                "cycleway" IN ('share_busway')
                OR
                "cycleway:right" IN ('share_busway')
            )
        )
	)
)
OR
( 
	"oneway" = '-1'
	AND
	(
			"cycleway" IN ('share_busway','opposite_share_busway') -- un accès pour les vélos à la voie bus
			AND
			(	-- et l'existance d'une voie bus a contre sens 
				"busway" IN ('opposite_lane')
			)
	)
)	
	
-- B - Les cas où le coté est mentionné par le tag

OR
(	-- B1 - Le coté est signalé uniquement sur sur le tag busway :
	"cycleway" IN ('share_busway') -- un accès pour les vélos à la voie bus et,
	AND
	(
		( 	-- pour la voie de bus à droite :
			(	-- une voie de bus à droite
				"busway:right" IS NOT NULL
				AND
				"busway:right" NOT IN ('no')
			)
			AND
			(	-- et pas de voie de bus à gauche
				"busway:left" IS NULL
				OR
				"busway:left" = 'no'
			)
		)
	)
)


OR
(	-- B2 - Le coté est signalé sur le tag cycleway :
	(
		"cycleway:right" IN ('share_busway','opposite_share_busway')
		AND
		(
			"cycleway:left" IS NULL
			OR
			"cycleway:left" NOT IN ('share_busway','opposite_share_busway')
		)
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[40],"info"]="Voies_bus-1xG"
q38 = """(	-- A - Les cas où la voie est à sens unique
	"oneway" IN ('-1')
	AND
	(
		(
			(	-- A1 - Soit il s'agit de voies de bus indépendantes :
				"highway" IN ('service') -- des routes de service,
				AND
				(	-- accessibles aux bus,
					"psv" IN ('yes')
					OR
					"bus" IN ('yes')
				)
				AND
				(	-- interdites à tous les autres véhicules,
					"access" LIKE 'no' OR "motor_vehicle" LIKE 'no'
				)
				AND
				(	-- mais authorisées aux vélos.
					(
					"bicycle" IS NOT NULL
					AND
					"bicycle" NOT IN ('no')
					)
					OR
					"cycleway" IN ('share_busway')	
				)
			)
            OR
            (	-- A2 - Soit des voies de bus rattachées à une route en sens unique :
                "cycleway" IN ('share_busway') -- un accès pour les vélos à la voie bus
                AND
                (	-- et l'existance d'une voie bus
                    "busway" IS NOT NULL
                    AND
                    "busway" NOT IN ('no')
                )
            )
       	)

	)
	OR
    ( --Soit il s'agit de voies de bus guidée ouverte aux vélo
        "highway" = 'bus_guideway'
        AND
        (	-- mais authorisées aux vélos.
            (
            "bicycle" IS NOT NULL
            AND
            "bicycle" NOT IN ('no')
            )
            OR
            "cycleway" IN ('share_busway')
            OR
            "cycleway:left" IN ('share_busway')
        )
    )
)
OR
(
	"oneway" IN ('yes')
	AND
		(
			"cycleway" IN ('share_busway','opposite_share_busway')
			AND
			"busway" IN ('opposite_lane')
		)
)

-- B - Les cas où le coté est mentionné par le tag

OR
(	-- B1 - Le coté est signalé uniquement sur sur le tag busway :
	"cycleway" IN ('share_busway') -- un accès pour les vélos à la voie bus et,
	AND
	( -- ou,
		(	-- pour la voie de bus à gauche :
			(	-- une voie de bus à gauche
				"busway:left" IS NOT NULL
				AND
				"busway:left" NOT LIKE 'no'
			)
			AND
			(	-- et pas de voie de bus à droite
				"busway:right" IS NULL
				OR
				"busway:left" LIKE 'no'
			)
		)
	)
)
OR
(	-- B2 - Le coté est signalé sur le tag cycleway :
	(
		"cycleway:left" IN ('share_busway','opposite_share_busway')
		AND
		(
			"cycleway:right" IS NULL
			OR
			"cycleway:right" NOT IN ('share_busway','opposite_share_busway')
		)
	)
)
 """
# line_gpd_clipped.loc[osmid_bike_type[41],"info"]="Voies_bus-2x"
q39 = """-- On part du postula qu'une voie de bus en opposite_lane n'est pas un contre sens cyclable
-- Seules les voies de bus accessibles aux vélos sont comptabilisées

(
    ("oneway" IN ('yes','-1')) -- Soit une rue a sens unique
    AND
    (	--  les deux voies vélo sont spécifiées
        (
            (
                "cycleway:right" IN ('share_busway','opposite_share_busway')
                AND
                "cycleway:left" IN ('share_busway','opposite_share_busway')
            )
            OR
            "cycleway" IN ('share_busway','opposite_share_busway')
        )
        AND
        (
            "busway:right" IS NOT NULL
            AND
            "busway:right" NOT IN ('no')
        )
        AND
        (
            "busway:left" IS NOT NULL
            AND
            "busway:left" NOT IN ('no')
        )
    )
)
OR
(
    (	-- Dans tous les cas la route n'est pas à sens unique
        "oneway" IS NULL
        OR
        "oneway" NOT IN ('yes','-1')
    )
    AND
    (	-- et...
            -- Soit les voies de bus rattachées à une route (A)
        (	-- A1 - Soit les vélos ont accès à la voie bus
            "cycleway" IN ('share_busway')
            AND
            (	-- et il y a un voie bus des deux cotés
                "busway" NOT IN ('no')
                OR
                (
                    "busway:right" NOT IN ('no')
                    AND
                    "busway:left" NOT IN ('no')
                )
            )
        )
        OR
        (	-- A2 - Soit les deux voies vélo sont spécifiées
            "cycleway:right" IN ('share_busway')
            AND
            "cycleway:left" IN ('share_busway')
            AND
            (
                "busway:right" IS NOT NULL
                AND
                "busway:right" NOT IN ('no')
            )
            AND
            (
                "busway:left" IS NOT NULL
                AND
                "busway:left" NOT IN ('no')
            )
        )
        OR
        (	-- Soit les bus empruntent des voies indépendantes accessibles seulement aux vélos (B)
            "highway" IN ('service')
            AND
                ( -- a double sens
                    "oneway" IS NULL
                    OR
                    "oneway" NOT IN ('yes','-1')
                )
            AND
            (
                ("psv" IS NOT NULL OR "psv" NOT IN ('no'))
                OR
                ("bus" IS NOT NULL OR "psv" NOT IN ('no'))
            )
            AND
            ("access" IN ('no') OR "motor_vehicle" IN ('no'))
            AND
            (
                (
                "bicycle" IS NOT NULL
                AND
                "bicycle" NOT IN ('no')
                )
                OR
                (
                "cycleway" IN ('share_busway')
                OR
                (
                    "cycleway:right" IN ('share_busway')
                    AND
                    "cycleway:left" IN ('share_busway')
                )
                )
            )
        )
        OR
        (
            "highway" IN ('bus_guideway')
            AND
            (
                (
                "bicycle" IS NOT NULL
                AND
                "bicycle" NOT IN ('no')
                )
                OR
                (
                    "cycleway" IN ('share_busway')
                    OR
                    (
                        "cycleway:right" IN ('share_busway')
                        AND
                        "cycleway:left" IN ('share_busway')
                    )
                )
            )
        )
    )
)
 """
# line_gpd_clipped.loc[osmid_bike_type[42],"info"]="Voies_vertes"
q40 = """
"highway" = 'path'
AND
"bicycle" = 'designated'
AND
"foot" = 'designated'
 """
# line_gpd_clipped.loc[osmid_bike_type[44],"info"]="Zones_30"
q41 = """-- Sont comptabilisés uniquement les zones 30 et pas les voies limitees à 30
-- Seul le sens voiture est pris en compte

"maxspeed" LIKE '30'
AND
(
	"zone:maxspeed" LIKE 'FR:30'
	OR
	"source:maxspeed" LIKE 'FR:zone30'
)
AND
(
	"bicycle" IS NULL
	OR
	"bicycle" NOT IN ('no')
)

 """

# line_gpd_clipped.loc[osmid_bike_type[46],"info"]="Zones_rencontre"
q42 = """

--soit une voie de type living street
(
"highway" LIKE 'living_street'

OR

--soit une voie avec le tag zone:maxspeed ou source:maxspeed
	( 
	"maxspeed"='20'
	AND
		(
		"zone:maxspeed"='FR:20'
		OR
		"source:maxspeed"='FR:zone20'
		)
	)
)
 """


# line_gpd_clipped.loc[osmid_bike_type[48],"info"]="chaucidou" -> Piste cyclable
q43 = """(	-- Soit
	(	-- une route explicitement à double sens
		(
			"oneway" LIKE 'no' OR oneway IS NULL
		)
		AND
		(
			"junction" IS NULL
			OR
			"junction" NOT IN ('roundabout','circular')
		)
	)
	AND --et qui a
	(	-- soit une bande cyclable classique
		"cycleway" = 'lane'
		OR
		(	-- soit une bande cyclable à droite et à gauche quelque soit le sens
			"cycleway:right" = 'lane'
			AND "cycleway:left" = 'lane'
		)
		OR	-- soit une bande cyclable à droite et à gauche quelque soit le sens
		"cycleway:both" = 'lane'
	)
	AND -- et qui ne comporte q'une seule voie
	(
	    "lanes" = '1'
	)
)
 """

# line_gpd_clipped.loc[osmid_bike_type[49],"info"]="escalier"
q44 = """
-- Sont comptabilisés uniquement les escaliers ayant un aménagement pour les vélos

"highway" = 'steps' -- un escalier

AND
--avec une goulotte pour les vélos sur le coté droit
(
	( "ramp:bicycle:right" = 'yes')

	OR 

	( "ramp:bicycle:left" = 'yes' )

    OR 
    
	( "ramp:bicycle" = 'yes' )
	OR
	( "ramp:bicycle:both" = 'yes' )

)

 """

# line_gpd_clipped.loc[osmid_bike_type[52],"info"]="footway_permissive-1x"
q45 = """(
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
q46 = """(
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
# line_gpd_clipped.loc[osmid_bike_type[54],"info"]="velorue"
q47 = """(
    "cyclestreet" = 'yes'
    OR
    "bicycle_road" = 'yes'
)

AND
(
	"bicycle" IS NULL
	OR
	"bicycle" NOT IN ('no')
)
 """


# line_gpd_clipped.loc[osmid_bike_type[58],"info"]="Limite_a_20-1x"
q48 = """ 

"maxspeed" LIKE '20'

"""

# line_gpd_clipped.loc[osmid_bike_type[60],"info"]="Limite_a_50-1x"
q49 = """ 

"maxspeed" LIKE '50'

"""


# all in a array

queries = [
    q0,
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
]
