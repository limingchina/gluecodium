

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
#include "smoke/FreeEnum.h"
#include "smoke/FreePoint.h"
#include "smoke/FreeTypeDef.h"
#include "smoke/UseFreeTypes.h"
#include "chrono"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseFreeTypes = ::smoke::UseFreeTypes;


void register_smoke_UseFreeTypes(py::module_& module) {
    py::class_<UseFreeTypes, std::shared_ptr<UseFreeTypes>>(module, "smoke_UseFreeTypes")
        .def("__gluecodium_id__", [](const UseFreeTypes& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def("do_stuff", &UseFreeTypes::do_stuff, py::arg("point"), py::arg("mode"))
        ;
}

