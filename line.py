from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30

class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = [Decimal(point)
                   for point in normal_vector]

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0'] * self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c / Decimal(initial_coefficient)
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    def __eq__(self, line2):
        v1 = Vector(self.normal_vector)
        v2 = Vector(line2.normal_vector)

        if v1.iszero():
            if not line2.normal_vector.iszero():
                return False

            diff = self.constant_term - line2.constant_term
            return MyDecimal(diff).is_near_zero()

        elif v2.iszero():
            return False

        if not self.isparallel(line2):
            return False

        basepoint_difference = self.basepoint.substract(line2.basepoint)
        return basepoint_difference.isorthogonal(v1)


    def isparallel(self, other_line):
        v1 = Vector(self.normal_vector)
        v2 = Vector(other_line.normal_vector)
        return v1.isparallel(v2)

    def intersection(self, other_line):
        if self == other_line and self.isparallel(other_line):
            return None
        else:
            a, b = self.normal_vector
            k1 = self.constant_term

            c, d = other_line.normal_vector
            k2 = other_line.constant_term

            denominator = ((a*d) - (b*c))

            x = ((d*k1) - (b*k2)) / denominator
            y = ((-c*k1) + (a*k2)) / denominator

            return Vector([x, y])


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
