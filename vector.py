import math
from decimal import Decimal, getcontext

getcontext().prec =  30

class Vector(object):
  TOLERANCE = 1e-10
  """Describes a vector with multiple coordinates"""

  def __init__(self, coordinates):
      try:
          if not coordinates:
              raise ValueError
          self.coordinates = tuple([Decimal(c) for c in coordinates])
          self.dimension = len(coordinates)

      except ValueError:
          raise ValueError('The coordinates must be nonempty')

      except TypeError:
          raise TypeError('The coordinates must be an iterable')

  def __str__(self):
      return 'Vector: {}'.format([round(coord, 3)
                                  for coord in self.coordinates])

  def __eq__(self, v):
      return self.coordinates == v.coordinates

  def add(self, other_vector):
    return Vector(map(sum, zip(self.coordinates, other_vector.coordinates)))

  def substract(self, other_vector):
    return Vector([coords[0] - coords[1]
                   for coords in zip(self.coordinates, other_vector.coordinates)])

  def times_scalar(self, factor):
    return Vector([coord * factor
                   for coord in self.coordinates])

  def magnitude(self):
    return math.sqrt(sum(coord ** 2
      for coord in self.coordinates))

  def normalize(self):
    try:
      normalized_magnitude = Decimal(1 / self.magnitude())
      return self.times_scalar(normalized_magnitude)
    except ZeroDivisionError:
      print("Cannot divide by zero")
      return 0

  def product(self, other_vector):
    return sum([coords[0] * coords[1]
      for coords in zip(self.coordinates, other_vector.coordinates)])

  def angle(self, other_vector, degrees=False):
    try:
      total_magnitude = Decimal(self.magnitude() * other_vector.magnitude())
      division = self.product(other_vector) / total_magnitude
      radians = math.acos(round(division, 2))
      if degrees:
        return math.degrees(radians)
      else:
        return radians
    except ZeroDivisionError:
      print("Cannot divide by zero")
      return 0

  def iszero(self):
    return abs(self.magnitude()) < self.TOLERANCE

  def isparallel(self, other_vector):
    return self.iszero() or other_vector.iszero() or self.angle(other_vector) in [0, math.pi]

  def isorthogonal(self, other_vector):
    return abs(self.product(other_vector)) < self.TOLERANCE

  def projection_vector(self, other_vector):
    other_vector_normalized = other_vector.normalize()
    dot_product = self.product(other_vector_normalized)

    return other_vector_normalized.times_scalar(dot_product)


  def cross_product(self, other_vector):
    """
      The producto of magnitude of vector a times the magnitude of vector b times sin(angle)
      || a x b || = ||a|| * ||b|| * sin(angle)

      |y1*z2   -   y2z1|
      |-(x1*z2 - x2*z1)|
      |x1*y2   -   x2y1|
    """
    [x1, y1, z1] = self.coordinates
    [x2, y2, z2] = other_vector.coordinates
    x = (y1 * z2) - (y2 * z1)
    y = -((x1 * z2) - (x2 * z1))
    z = (x1 * y2) - (x2 * y1)
    return Vector([x, y, z])

  def area_parallelogram(self, other):
      return self.cross_product(other).magnitude()

  def area_triangle(self, other):
      return round(self.cross_product(other).magnitude() / 2, 3)
