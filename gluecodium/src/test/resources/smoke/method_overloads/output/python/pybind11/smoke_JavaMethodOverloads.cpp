

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
#include "smoke/JavaMethodOverloads.h"
#include "string"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using JavaMethodOverloads = ::smoke::JavaMethodOverloads;


void register_smoke_JavaMethodOverloads(py::module_& module) {
    py::class_<JavaMethodOverloads, std::shared_ptr<JavaMethodOverloads>>(module, "smoke_JavaMethodOverloads")
        .def("one", &JavaMethodOverloads::one, py::arg("input"))
                .def("two", [](JavaMethodOverloads& self, py::handle input) {
                        self.two(gluecodium::python::from_python_regular<::std::vector< ::std::string >>(input));
                }, py::arg("input"))
        ;
}

