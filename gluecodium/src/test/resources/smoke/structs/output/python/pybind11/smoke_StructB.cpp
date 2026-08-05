

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/VectorHash.h"
#include "smoke/StructA.h"
#include "smoke/StructB.h"
#include "vector"

using StructB = ::smoke::StructB;



void register_smoke_StructB(py::module_& module) {
auto cls_StructB = py::class_<StructB>(module, "smoke_StructB")
        .def_readwrite("field", &StructB::field)
        .def(py::init<>())
        .def(py::init<::std::vector< ::smoke::StructA >>(), py::arg("field"))
        ;


}
