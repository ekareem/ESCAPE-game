from __future__ import annotations
from IO_Object import IO_Entity

IO_MASS = 1
IO_GRAVITY = 2.5

class IO_Coordinate(IO_Entity):
    def __init__(self,x : float = 0,y : float = 0):
        """
        @member x int : x coordinate\n
        @member y int : y coordinate\n
        """
        super().__init__()
        self.x = x
        self.y = y

    def __add__(self,other : IO_Coordinate) -> IO_Coordinate:
        """
        + oparator overload\n
        adds two self and other dimen object\n

        @param other Dimen : \n
        @return Dimen\n
        """
        return self.__class__(self.x + other.x, self.y + other.y)
    
    def __iadd__(self,other):
        """
        += oparator overload\n
        subtracts two self and other dimen object\n
        """
        self.x += other.x
        self.y += other.y
        return self

    def __sub__ (self,other) -> IO_Coordinate:
        """
        - oparator overload\n
        subtract two self and other dimen object\n

        @param other Dimen :\n
        @return Dimen\n
        """
        return self.__class__(self.x - other.x, self.y - other.y)
        
    def __isub__(self,other):
        """
        -= oparator overload\n
        subtracts two self and other dimen object\n
        """
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self,scaler) -> IO_Coordinate:
        """
        * oparator overload\n
        multiply two self and other dimen object\n

        @param other Dimen : \n
        @return Dimen\n
        """
        return self.__class__(self.x * scaler, self.y * scaler)

    def __imul__(self,scaler):
        """
        *= oparator overload\n
        subtracts two self and other dimen object\n
        """
        self.x *= scaler
        self.y *= scaler
        return self

    def __truediv__(self,scaler) -> IO_Coordinate:
        """
        oparator overload\n
        multiply two self and other dimen object\n

        @param other Dimen : \n
        @return Dimen\n
        """
        return self.__class__(self.x / scaler, self.y * scaler)

    def __idiv__(self,scaler):
        """
        /= oparator overload\n
        multiply two self and other dimen object\n

        @param other Dimen : \n
        @return Dimen\n
        """
        self.x /= scaler
        self.y /= scaler

    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'x', self.x
        yield 'y', self.y 

class IO_Point(IO_Coordinate):
    """
    defindes 2d point
    """
    def __init__(self,x=0,y=0):
        super().__init__(x,y)

class IO_Vector(IO_Coordinate):
    """
    defindes 2d point
    """
    def __init__(self,x=0,y=0):
        super().__init__(x,y)

class IO_Transform(IO_Coordinate):
    """
    defindes 2d point
    """
    def __init__(self,x=0,y=0):
        super().__init__(x,y)
        
    def translateX(self,x):
        """
        translate X
        param x float : component x is translated x amount
        """
        self.x += x
    
    def translateY(self,y):
        """
        translate y
        param y float : component y is translated y amount
        """
        self.y += y
        
    def translate(self,vector):
        """
        translate both x and y component
        vector IO_Vector : x and y are translated by the value of the x and y component of vector
        """
        self.x += vector.x
        self.y += vector.y

class IO_RigidBody(IO_Entity):
    """
    defines a rigid body that has physics
    """
    def __init__(self,mass = IO_MASS,gravity = IO_Vector()):
        """
        mass float : objects mass
        gravity float : objects gravity
        friction IO_Vector : objects fricton
        position IO_Vector : objects position
        velocity IO_Vector : objects Velocity
        accelaration IO_Vector : object acceleration
        """
        super().__init__()
        self.mass = mass
        self.gravity : IO_Vector = gravity
        self.force = IO_Vector()
        self.friction = IO_Vector()
        self.position = IO_Vector()
        self.velocity = IO_Vector()
        self.accelaration = IO_Vector()
        
    def applyForce(self,force):
        """
        sets The Force IO_Vector
        param force IO_Vector 
        """
        self.force = force
        
    def applyForceX(self,Fx):
        """
        sets The x component of force vector
        param fx Scaler
        """
        self.force.x = Fx
        
    def applyForceY(self,Fy):
        """
        sets The y component of force vector
        param fy Scaler
        """
        self.force.y = Fy
        
    def unSetForce(self):
        """
        resets the Force vector
        """
        self.force.x = 0
        self.force.y = 0
        
        
    def applyFriction(self,friction):
        """
        sets The friction IO_Vector
        param friction IO_Vector 
        """
        self.friction = friction
        
    def applyFrictionX(self,Fx):
        """
        sets The x component of friction vector
        param fx Scaler
        """
        self.friction.x = Fx
        
    def applyFrictionY(self,Fy):
        """
        sets The y component of friction vector
        param fx Scaler
        """
        self.friction.y = Fy
        
    def unSetFriction(self):
        """
        reset friction vector
        """
        self.friction.x = 0
        self.friction.y = 0


    def update(self,dt):
        """
        updates rigid body components
        """
        self.accelaration.x = (self.force.x + self.friction.y)/self.mass
        self.accelaration.y = (self.force.y + self.gravity.y)/self.mass
        self.velocity = self.accelaration*dt
        self.position = self.velocity*dt

    def __iter__(self):
        yield 'class', self.__class__.__name__
        yield 'mass', self.mass
        yield 'gravity', self.gravity
        yield 'friction', self.friction
        yield 'position', self.position
        yield 'velocity', self.velocity
        yield 'accelaration', self.accelaration
        