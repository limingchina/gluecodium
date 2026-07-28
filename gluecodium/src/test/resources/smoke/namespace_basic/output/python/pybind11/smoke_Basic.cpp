

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
#include "root/space/smoke/Basic.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using Basic = ::root::space::smoke::Basic;


void register_smoke_Basic(py::module_& module) {
    py::class_<Basic, std::shared_ptr<Basic>>(module, "smoke_Basic")
        .def("__gluecodium_id__", [](const Basic& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("basic_method", &Basic::basic_method, py::arg("input_string"))
        ;
}

