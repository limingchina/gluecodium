

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Locale.h"
#include "gluecodium/TimePointHash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/OuterStruct.h"
#include "chrono"
#include "cstdint"
#include "functional"
#include "memory"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterStruct = ::smoke::OuterStruct;

void register_OuterStruct(py::module_& module) {
    py::class_<OuterStruct>(module, "OuterStruct")
        .def_readwrite("field", &OuterStruct::field)
        .def(py::init<::std::string>(), py::arg("field"))
        .def("do_nothing", &OuterStruct::do_nothing)
        ;
}

