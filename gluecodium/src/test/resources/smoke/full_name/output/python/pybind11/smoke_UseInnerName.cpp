

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
#include "smoke/OuterName.h"
#include "smoke/UseInnerName.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseInnerName = ::smoke::UseInnerName;


void register_smoke_UseInnerName(py::module_& module) {
    py::class_<UseInnerName, std::shared_ptr<UseInnerName>>(module, "smoke_UseInnerName")
        .def("__gluecodium_id__", [](const UseInnerName& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("do_foo", &UseInnerName::do_foo)
        ;
}

