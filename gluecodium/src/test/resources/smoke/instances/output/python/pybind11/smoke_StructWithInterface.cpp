

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
#include "smoke/SimpleInterface.h"
#include "smoke/StructWithInterface.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using StructWithInterface = ::smoke::StructWithInterface;

void register_smoke_StructWithInterface(py::module_& module) {
    py::class_<StructWithInterface>(module, "smoke_StructWithInterface")
        .def_readwrite("interface_instance", &StructWithInterface::interface_instance)
        .def(py::init<>())
        .def(py::init<::std::shared_ptr< ::smoke::SimpleInterface >>(), py::arg("interface_instance"))
        ;
}

