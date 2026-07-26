

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
#include "gluecodium/UnorderedMapHash.h"
#include "smoke/SkipTypes.h"
#include "smoke/SkippedEverywhere.h"
#include "cstdint"
#include "string"
#include "unordered_map"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SkippedEverywhere = ::smoke::SkippedEverywhere;

void register_smoke_SkippedEverywhere(py::module_& module) {
    py::class_<SkippedEverywhere>(module, "smoke_SkippedEverywhere")
        .def_readwrite("nothing_to_see_here", &SkippedEverywhere::nothing_to_see_here)
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("nothing_to_see_here"))
                .def("use_map_in_dart", [](SkippedEverywhere& self, py::handle foo) {
                        self.use_map_in_dart(gluecodium::python::from_python_regular<::std::unordered_map< int32_t, ::smoke::SkipTypes::NotInDart >>(foo));
                }, py::arg("foo"))
        ;
}

