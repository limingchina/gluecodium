

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
#include "foo/AlienEnum1.h"
#include "foo/AlienEnum2.h"
#include "foo/AlienEnum3.h"
#include "smoke/EnumDefaultsExternal.h"
#include "smoke/EnumWrapper.h"
#include "optional"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using EnumDefaultsExternal = ::smoke::EnumDefaultsExternal;


void register_smoke_EnumDefaultsExternal(py::module_& module) {
    py::class_<EnumDefaultsExternal, std::shared_ptr<EnumDefaultsExternal>>(module, "smoke_EnumDefaultsExternal")
        .def("__gluecodium_id__", [](const EnumDefaultsExternal& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        ;
}

