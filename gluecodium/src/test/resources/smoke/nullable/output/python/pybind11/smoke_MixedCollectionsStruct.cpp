

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/TimePointHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/MixedCollectionsStruct.h"
#include "chrono"
#include "optional"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MixedCollectionsStruct = ::gluecodium::smoke::MixedCollectionsStruct;

void register_MixedCollectionsStruct(py::module_& module) {
    py::class_<MixedCollectionsStruct>(module, "MixedCollectionsStruct")
        .def_readwrite("almost_dates", &MixedCollectionsStruct::almost_dates)
        .def_readwrite("dates", &MixedCollectionsStruct::dates)
        ;
}

