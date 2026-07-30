

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/TimePointHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/MixedCollectionsStruct.h"
#include "chrono"
#include "optional"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using MixedCollectionsStruct = ::smoke::MixedCollectionsStruct;

void register_smoke_MixedCollectionsStruct(py::module_& module) {
    py::class_<MixedCollectionsStruct>(module, "smoke_MixedCollectionsStruct")
        .def_readwrite("almost_dates", &MixedCollectionsStruct::almost_dates)
        .def_readwrite("dates", &MixedCollectionsStruct::dates)
        .def(py::init<>())
        .def(py::init<::std::vector< std::optional< ::std::chrono::system_clock::time_point > >, ::std::vector< ::std::chrono::system_clock::time_point >>(), py::arg("almost_dates"), py::arg("dates"))
        ;
}

