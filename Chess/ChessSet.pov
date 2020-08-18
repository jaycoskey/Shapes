// POV-Ray scene description for a chess board
// Copyright (c) 2008, by Jay M. Coskey
// POV-Ray, v3.6
//
// -w320 -h240
// -w800 -h600 +a0.3

global_settings { assumed_gamma 2.2 max_trace_level 5 }

#include "shapes.inc"
#include "colors.inc"
#include "textures.inc"
#include "skies.inc"
#include "metals.inc"
#include "woods.inc"

#declare TORUS_R1 = 2;
#declare TORUS_R2 = (1/3) * TORUS_R1;
#declare TORUS_R = TORUS_R1 + TORUS_R2;

#declare PIECE_BASE_RADIUS = (2/3) * TORUS_R1;
#declare PIECE_BASE_HEIGHT = 3 * TORUS_R1;
#declare PIECE_FOOT_RADIUS = 1 * TORUS_R2;
#declare PIECE_HEAD_RADIUS = 1 * TORUS_R2;

#declare PAWN_BASE_RADIUS = PIECE_BASE_RADIUS;
#declare PAWN_BASE_HEIGHT = 0.8 * PIECE_BASE_HEIGHT;
#declare PAWN_FOOT_RADIUS = PIECE_FOOT_RADIUS;
#declare PAWN_HEAD_RADIUS = 1.0 * (TORUS_R1);

#declare CROWN_HEIGHT = TORUS_R1 + TORUS_R2;
#declare BISHOP_CAP_HEIGHT = TORUS_R1;
#declare PI = 3.14159265359;

camera {
    location  <40, 30, -70>
    direction <0, 0, 2>
    up        <0, 1, 0>
    right     <4/3, 0, 0>
    look_at   <0, -1, 1>
    aperture 0
}

light_source { <800, 600, -200> colour White }

#declare PawnBase =
union {
    intersection {
        torus { PAWN_BASE_RADIUS, PAWN_FOOT_RADIUS }
        plane { -y, 0 }
    }
    cylinder { 0, y*PAWN_BASE_HEIGHT, PAWN_BASE_RADIUS }
}

#declare PieceBase =
union {
    intersection {  // BOTTOM
        union {
            torus { PIECE_BASE_RADIUS, PIECE_FOOT_RADIUS }
            cylinder { <0, 0, 0>, <0, PIECE_FOOT_RADIUS, 0>, PIECE_BASE_RADIUS }
        }
        plane { -y, 0 }
    }
    intersection { // TOP
        union {
            torus { TORUS_R - PIECE_HEAD_RADIUS, PIECE_HEAD_RADIUS }
            cylinder { <0, -PIECE_HEAD_RADIUS, 0>, <0, 0, 0>, TORUS_R1 }
        }
        plane { y, 0 }
        translate PIECE_BASE_HEIGHT * y
    }
    cylinder { 0, y * PIECE_BASE_HEIGHT, PIECE_BASE_RADIUS }
}

#declare Pawn = union {
    object {
        sphere { <0, 0, 0>, PAWN_HEAD_RADIUS }
        translate PAWN_BASE_HEIGHT * y
    }
    object { PawnBase }
}

#declare Crown = union {
    cylinder { <  TORUS_R1, 0, 0>, <  TORUS_R1, CROWN_HEIGHT, 0>, TORUS_R2 }
    cylinder { < -TORUS_R1, 0, 0>, < -TORUS_R1, CROWN_HEIGHT, 0>, TORUS_R2 }
    cylinder { < 0, 0,  TORUS_R1>, < 0, CROWN_HEIGHT,  TORUS_R1>, TORUS_R2 }
    cylinder { < 0, 0, -TORUS_R1>, < 0, CROWN_HEIGHT, -TORUS_R1>, TORUS_R2 }
    torus { TORUS_R1, TORUS_R2 translate <0, CROWN_HEIGHT, 0> }
}

#declare Rook = union {
    object {
        Crown
        translate PIECE_BASE_HEIGHT * y
    }
    object { PieceBase }
}

#declare VerticalTorus = object {
    torus { TORUS_R1, TORUS_R2 rotate <0, 0, 90> translate <0, PIECE_BASE_HEIGHT + TORUS_R1, 0> }
}

#declare Knight = union {
    object { VerticalTorus }
    object { PieceBase }
}

#declare Bishop = union {
    object {
        torus { TORUS_R1, TORUS_R2 }
        rotate <0, 0, 60>
        translate <-0.5 * TORUS_R1, PIECE_BASE_HEIGHT + BISHOP_CAP_HEIGHT, 0>
    }
    object {
        torus { TORUS_R1, TORUS_R2 }
        rotate <0, 0, -60>
        translate <0.5 * TORUS_R1, PIECE_BASE_HEIGHT + BISHOP_CAP_HEIGHT, 0>
    }
    object { PieceBase }
}

#declare Queen = union {
    object { VerticalTorus }
    object { VerticalTorus rotate <0,  60, 0> }
    object { VerticalTorus rotate <0, 120, 0> }
    object { PieceBase }
}

#declare King = union {
    torus { TORUS_R1, TORUS_R2 rotate <0, 0, 90> translate <0, PIECE_BASE_HEIGHT + CROWN_HEIGHT, 0> }
    torus { TORUS_R1, TORUS_R2 rotate <90, 0, 0> translate <0, PIECE_BASE_HEIGHT + CROWN_HEIGHT, 0> }
    object { Rook }
}

#declare WWood = texture { T_Silver_3B }
#declare BWood = texture { T_Gold_3C }

#declare WPawn = object { Pawn
    texture {
        WWood
        pigment { quick_color red 0.95 green 0.62 }
    }
}

#declare BPawn = object { Pawn
    texture {
        BWood
        pigment { quick_color red 0.4 green 0.2 }
    }
}

#declare WRook = object { Rook
    texture {
        WWood
        pigment { quick_color red 0.95 green 0.62 }
    }
}

#declare BRook = object { Rook
    texture {
        BWood
        pigment { quick_color red 0.4 green 0.2 }
    }
}

#declare WKnight = object { Knight
    texture {
        WWood
        pigment { quick_color red 0.95 green 0.62 }
    }
}

#declare BKnight = object { Knight
    rotate 180*y
    texture {
        BWood
        pigment { quick_color red 0.4 green 0.2 }
    }
}

#declare WBishop = object { Bishop
    texture {
        WWood
        pigment { quick_color red 0.95 green 0.62 }
    }
}

#declare BBishop = object { Bishop
    rotate 180*y
    texture {
        BWood
        pigment { quick_color red 0.4 green 0.2 }
    }
}

#declare WQueen = object { Queen
    texture {
        WWood
        pigment { quick_color red 0.95 green 0.62 }
    }
}

#declare BQueen = object { Queen
    texture {
        BWood
        pigment { quick_color red 0.4 green 0.2 }
    }
}

#declare WKing = object { King
    texture {
        WWood
        pigment { quick_color red 0.95 green 0.62 }
    }
}

#declare BKing = object { King
    texture {
        BWood
        pigment { quick_color red 0.4 green 0.2 }
    }
}

#declare FarPawns = union {
    object { BPawn translate <-28, 0, 20> }
    object { BPawn translate <-20, 0, 20> }
    object { BPawn translate <-12, 0, 20> }
    object { BPawn translate < -4, 0, 20> }
    object { BPawn translate <  4, 0, 20> }
    object { BPawn translate < 12, 0, 20> }
    object { BPawn translate < 20, 0, 20> }
    object { BPawn translate < 28, 0, 20> }
}

#declare FarPieces = union {
    object { FarPawns }
    object { BRook   translate <-28, 0, 28> }
    object { BKnight translate <-20, 0, 28> }
    object { BBishop translate <-12, 0, 28> }
    object { BQueen  translate < -4, 0, 28> }
    object { BKing   translate <  4, 0, 28> }
    object { BBishop translate < 12, 0, 28> }
    object { BKnight translate < 20, 0, 28> }
    object { BRook   translate < 28, 0, 28> }
}

#declare NearPawns =
union {
    object { WPawn translate <-28, 0, -20> }
    object { WPawn translate <-20, 0, -20> }
    object { WPawn translate <-12, 0, -20> }
    object { WPawn translate < -4, 0, -20> }
    object { WPawn translate <  4, 0, -20> }
    object { WPawn translate < 12, 0, -20> }
    object { WPawn translate < 20, 0, -20> }
    object { WPawn translate < 28, 0, -20> }
}

#declare NearPieces = union {
    object { NearPawns }
    object { WRook   translate <-28, 0, -28> }
    object { WKnight translate <-20, 0, -28> }
    object { WBishop translate <-12, 0, -28> }
    object { WQueen  translate < -4, 0, -28> }
    object { WKing   translate <  4, 0, -28> }
    object { WBishop translate < 12, 0, -28> }
    object { WKnight translate < 20, 0, -28> }
    object { WRook   translate < 28, 0, -28> }
}

#declare Pieces =
union {
    object { NearPieces }
    object { FarPieces }
}

#declare FramePiece =
intersection {
    plane { +y, -0.15 }
    plane { -y, 3 }
    plane { -z, 35 }
    plane { <-1, 0, 1>, 0 }
    plane { < 1, 0, 1>, 0 }
}

#declare Frame =
union {
    union {
        object { FramePiece }
        object { FramePiece rotate 180*y }
        texture {
            T_Wood20
            scale 2
            rotate y*87
            translate x*1
            finish {
                specular 1
                roughness 0.02
                ambient 0.35
            }
        }
    }

    union {
        object { FramePiece rotate -90*y }
        object { FramePiece rotate  90*y }
        texture {
            T_Wood20
            scale 2
            rotate y*2
            finish {
                specular 1
                roughness 0.02
                ambient 0.35
            }
        }
    }
}
#declare Board =
    box { <-32, -1, -32> <32, 0, 32>
        texture {
            tiles {
                texture {
                    pigment {
                        // White marble
                        wrinkles
                        turbulence 1.0
                        colour_map {
                            [0.0 0.7 colour White
                                     colour White]
                            [0.7 0.9 colour White
                                     colour red 0.8 green 0.8 blue 0.8]
                            [0.9 1.0 colour red 0.8 green 0.8 blue 0.8
                                     colour red 0.5 green 0.5 blue 0.5]
                        }
                        scale <0.6, 1, 0.6>
                        rotate -30*y
                    }
                    finish {
                        specular 1
                        roughness 0.02
                        reflection 0.25
                    }
                }
                tile2
                texture {
                    pigment {
                        // Dark granite
                        granite
                        scale <0.3, 1, 0.3>
                        colour_map {
                            [0 1 colour Black
                                colour red 0.5 green 0.5 blue 0.5]
                        }
                    }
                    finish {
                        specular 1
                        roughness 0.02
                        reflection 0.25
                    }
                }
            }
            scale <8, 1, 8>
        }
    }


object { NearPieces }
object { FarPieces }
object { Board }
object { Frame }
