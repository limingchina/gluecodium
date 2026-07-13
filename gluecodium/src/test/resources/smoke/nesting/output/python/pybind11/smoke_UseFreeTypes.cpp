

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FreeEnum.h"
#include "smoke/FreePoint.h"
#include "smoke/FreeTypeDef.h"
#include "smoke/UseFreeTypes.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseFreeTypes = ::gluecodium::smoke::UseFreeTypes;

void register_UseFreeTypes(py::module_& module) {
    py::class_<UseFreeTypes, std::shared_ptr<UseFreeTypes>>(module, "UseFreeTypes")
        .def("do_stuff", &UseFreeTypes::do_stuff, py::arg("point"), py::arg("mode"))
        ;
}

