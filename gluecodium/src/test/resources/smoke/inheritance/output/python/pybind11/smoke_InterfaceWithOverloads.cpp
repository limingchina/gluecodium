

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InterfaceWithOverloads.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InterfaceWithOverloads = ::smoke::InterfaceWithOverloads;

class InterfaceWithOverloadsTrampoline : public InterfaceWithOverloads {
public:
    using InterfaceWithOverloads::InterfaceWithOverloads;

    void parent_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, InterfaceWithOverloads, parent_method);
    }
    void parent_method(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, InterfaceWithOverloads, parent_method, input);
    }
};

void register_InterfaceWithOverloads(py::module_& module) {
    py::class_<InterfaceWithOverloads, std::shared_ptr<InterfaceWithOverloads>, InterfaceWithOverloadsTrampoline>(module, "InterfaceWithOverloads")
        .def(py::init<>())
        .def("parent_method", [](InterfaceWithOverloads& self) {
            return self.parent_method();
        })
        .def("parent_method", [](InterfaceWithOverloads& self, const ::std::string& input) {
            return self.parent_method(input);
        }, py::arg("input"))
        ;
}

