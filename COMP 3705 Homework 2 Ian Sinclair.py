# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 09:13:30 2022

@author: IanSi
"""

class vertex() :
    def __init__( self, x : int, y : int ) :
        self.x = x
        self.y = y
    
    def toString( self ) :
        return str(self.x) + " , " + str(self.y)



def cross( A : vertex, B : vertex, C : vertex ) :
    """
    Parameters
    ----------
    C : vertex
    A : vertex
    B : vertex

    Returns
    -------
    Cross product between 2D vectors (B-A) and (C-B).
    """
    return ( (B.x - A.x) * (C.y - B.y) ) - ( (B.y - A.y) * (C.x - B.x) )

def Reflex( P, i : int ) :
    if len( P ) < 3 :
        return None
    
    if not ( 0 <= i < len( P ) ) :
        raise("Index i out of bounds of polygon.")
    
    A = P[i-1]
    B = P[i]
    if i == len( P ) - 1 :
        C = P[0]
    else : 
        C = P[i+1]
    
    det = cross( A, B, C )
    
    if det < 0 :
        return True
    return False

def Orient(A : vertex, B : vertex, C : vertex ) :
    """
    Parameters
    ----------
    q : vertex
    A : vertex
    B : vertex

    Returns
    0 --> A, B and q are collinear
    1 --> Clockwise
    -1 --> Counterclockwise
    """
    Cross_product = cross( A, B, C ) 
    if Cross_product > 0 :
        return 1 
    elif Cross_product < 0 :
        return -1
    return 0;


def onEdge( q : vertex, v1 : vertex, v2 : vertex ) :
    """
    Parameters
    ----------
    q : vertex
    v1 : vertex
    v2 : vertex
    Assume q, v1, v2 are colinear
    Returns
    -------
    bool
        True --> q is on line segment v1v2
        False --> q is not on line segment v1v2.

    """
    if (v1.y >= q.y >= v2.y) or (v2.y >= q.y >= v1.y) :
        if (v1.x >= q.x >= v2.x) or (v2.x >= q.x >= v1.x) :
            return True
    return False



def intersect( A1 : vertex, A2 : vertex, B1 : vertex, B2: vertex ) :
    """
    Parameters
    ----------
    A1 : vertex
    A2 : vertex
    B1 : vertex
    B2 : vertex
    
    Line segment A1 --> A2 and B1 --> B2

    Returns
    -------
    INT
        0 --> if A1 is on line segment of B1 --> B2
        1 --> if line segment A1 --> A2 intersects B1 --> B2
        -1 --> if no intersection.

    """
    #  Orientation of every combination of connecting vectors between
    #   line segments.
    O1 = Orient(A1, A2, B1)
    O2 = Orient(A1, A2, B2)
    O3 = Orient(B1, B2, A1)
    O4 = Orient(B1, B2, A2)
    
    if (O3 == 0) : #  A1 is colinear with B1,B2
        if onEdge( A1, B1, B2 ) : #  A1 is on line segment B1 --> B2
            return 0
        return -1
    
    if (O4 == 0) : #  A1 is colinear with B1,B2
        if onEdge( A2, B1, B2 ) : #  A2 is on line segment B1 --> B2
            return 0
        return -1  
    
    
    if (O1 == 0) and (O2 == 0) :  #  B1 and B2 are colinear with A1 and A2.
        if onEdge( A1, B1, B2 ) : #  A1 is on boundary of B1 -- B2
            return 0
        return -1
    
    #  General case, if both line segments intersect but none are colinear.
    if ( O1 != 0 and O2 != 0 and O3 != 0 and O4 != 0 ) :
        if (O1 != O2) and (O3 != O4) :
            return 1    
    return -1


def LocallyInterior( P, i : int, j : int ) :
    
    if len( P )  < 3:
        raise("Invalid Polygon, must have more than 3 vertices.")
    
    if i == j :
        raise("Line segment must be non trivial, i != j")
    
        
    if abs( i - j) == 1 :
        return True
    
    #  check if segment ij intersects boundary of P
    if intersect( P[i], P[0], P[j], P[-1] ) == 1 :
        return False
    
    for v in range( 0, len(P)-1 ) :
        if (i is not v) and (i is not v+1) :
            if (j is not v) and (j is not v+1) :
                if intersect(P[i],P[v] , P[j], P[v+1]) == 1 :
                    return False    
    
    # Finds orientation of polygon P, and P'
    P_sub = P[j:] + P[:i] + [P[i]]
    
    P_sub_orient = 0
    P_orient = 0
    
    if len( P_sub ) <= 2 :
        print('Trivial')
        return True
    
    for v in range( 0 , len( P )-2 ) :
        P_orient += Orient( P[v] , P[v+1], P[v+2] )
    
    for v in range( 0 , len( P_sub )-2 ) :
        P_sub_orient += Orient( P_sub[v], P_sub[v+1], P_sub[v+2] )
    
        #  Checks if P and P' are different orientations.
    if P_sub_orient < 0 and P_orient >= 0 :
        return False
    
    if P_sub_orient >= 0 and P_orient < 0 :
        return False
    
    return True


def driver1() :
    P = [ vertex(20,20),
         vertex(15,30),
         vertex(10,20),
         vertex(10,10),
         vertex(13,10), # reflex point
         vertex(15,0),
         vertex(18,20), #  reflex point
         ]
    
    print( Reflex( P, 6 ) )



def driver2() :
    P = [ vertex(40,20), 
         vertex(40,40), 
         vertex(20,40), 
         vertex(20,20),
         vertex(30,30), 
         ]
    
    print(LocallyInterior(P, 0, 3 )) #  Should be False
    print(LocallyInterior(P, 1, 3 )) #  Should be True
if __name__ == "__main__" :
    driver1()
    driver2()
