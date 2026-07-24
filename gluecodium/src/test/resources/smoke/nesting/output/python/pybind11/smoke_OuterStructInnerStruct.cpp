

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/TimePointHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/OuterStruct.h"
#include "chrono"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InnerStruct = ::smoke::OuterStruct::InnerStruct;

void register_smoke_OuterStructInnerStruct(py::module_& module) {
    py::class_<InnerStruct>(module, "OuterStructInnerStruct")
        .def_readwrite("other_field", &InnerStruct::other_field)
        .def(py::init<>())
        .def(py::init<::std::vector< ::std::chrono::system_clock::time_point >(), py::arg("other_field"))
        ;
}

