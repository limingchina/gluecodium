

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/SimpleClass.h"
#include "smoke/StructWithClass.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithClass = ::gluecodium::smoke::StructWithClass;

void register_StructWithClass(py::module_& module) {
    py::class_<StructWithClass>(module, "StructWithClass")
        .def_readwrite("class_instance", &StructWithClass::class_instance)
        .def(py::init<::std::shared_ptr< ::smoke::SimpleClass >>(), py::arg("class_instance"))
        ;
}

