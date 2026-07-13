

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ChildInterfaceOverloads.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ChildInterfaceOverloads = ::gluecodium::smoke::ChildInterfaceOverloads;

class ChildInterfaceOverloadsTrampoline : public ChildInterfaceOverloads {
public:
    using ChildInterfaceOverloads::ChildInterfaceOverloads;

    void foo(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ChildInterfaceOverloads, foo, input);
    }
    void bar(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ChildInterfaceOverloads, bar, input);
    }
};

void register_ChildInterfaceOverloads(py::module_& module) {
    py::class_<ChildInterfaceOverloads, std::shared_ptr<ChildInterfaceOverloads>, ChildInterfaceOverloadsTrampoline>(module, "ChildInterfaceOverloads")
        .def("foo", &ChildInterfaceOverloads::foo, py::arg("input"))
        .def("bar", &ChildInterfaceOverloads::bar, py::arg("input"))
        ;
}

