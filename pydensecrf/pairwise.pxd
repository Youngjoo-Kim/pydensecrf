from eigen cimport *


cdef extern from "densecrf/include/labelcompatibility.h":
    cdef cppclass LabelCompatibility:
        pass

    cdef cppclass PottsCompatibility(LabelCompatibility):
        PottsCompatibility(float) except +
        void apply( c_MatrixXf & out_values, const c_MatrixXf & in_values ) const

    cdef cppclass DiagonalCompatibility(LabelCompatibility):
        DiagonalCompatibility(const c_VectorXf&) except +

    cdef cppclass MatrixCompatibility(LabelCompatibility):
        MatrixCompatibility(const c_MatrixXf&) except +

cdef extern from "densecrf/include/pairwise.h":
    cpdef enum NormalizationType: NO_NORMALIZATION, NORMALIZE_BEFORE, NORMALIZE_AFTER, NORMALIZE_SYMMETRIC
    cpdef enum KernelType: CONST_KERNEL, DIAG_KERNEL, FULL_KERNEL


cdef extern from "densecrf/include/pairwise.h":
    cdef cppclass c_PairwisePotentials "PairwisePotential":
        c_PairwisePotentials(
            const c_MatrixXf & features, LabelCompatibility * compatibility,
            KernelType ktype,
            NormalizationType ntype) except +

        void apply(c_MatrixXf & out, const c_MatrixXf & Q) const


cdef extern from "densecrf/include/pairwise.h":
    cdef cppclass c_DenseKernel "DenseKernel":
        c_DenseKernel(const c_MatrixXf & f, KernelType ktype, NormalizationType ntype);

        void apply( c_MatrixXf & out, const c_MatrixXf & Q ) const;


cdef class PairwisePotentials:
    cdef c_PairwisePotentials *_this


cdef class DenseKernel:
    cdef c_DenseKernel *_this


cdef class PottsComp:
    cdef PottsCompatibility *_this

