

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
using ChildInterfaceOverloads = ::smoke::ChildInterfaceOverloads;

class ChildInterfaceOverloadsTrampoline : public ChildInterfaceOverloads {
public:
    using ChildInterfaceOverloads::ChildInterfaceOverloads;

    void foo(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, ChildInterfaceOverloads, foo, input);
    }
    void bar(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, ChildInterfaceOverloads, bar, input);
    }
};

void register_ChildInterfaceOverloads(py::module_& module) {
    py::class_<ChildInterfaceOverloads, std::shared_ptr<ChildInterfaceOverloads>, ChildInterfaceOverloadsTrampoline>(module, "ChildInterfaceOverloads")
        .def(py::init<>())
        .def("foo", [](ChildInterfaceOverloads& self, const ::std::string& input) {
            return self.foo(input);
        }, py::arg("input"))
        .def("bar", [](ChildInterfaceOverloads& self, const ::std::string& input) {
            return self.bar(input);
        }, py::arg("input"))
        ;
}

