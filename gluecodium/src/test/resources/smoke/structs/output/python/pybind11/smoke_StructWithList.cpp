

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
#include "gluecodium/VectorHash.h"
#include "smoke/StructWithList.h"
#include "vector"

using StructWithList = ::smoke::StructWithList;



void register_smoke_StructWithList(py::module_& module) {
auto cls_StructWithList = py::class_<StructWithList>(module, "smoke_StructWithList")
        .def_readwrite("field", &StructWithList::field)
        .def(py::init<>())
        .def(py::init<::std::vector< ::smoke::StructWithList >>(), py::arg("field"))
        ;


}
