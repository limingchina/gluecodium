

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/OuterInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using OuterInterface = ::smoke::OuterInterface;

class OuterInterfaceTrampoline : public OuterInterface {
public:
    using OuterInterface::OuterInterface;

    ::std::string foo(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(::std::string, OuterInterface, foo, input);
    }
};

void register_OuterInterface(py::module_& module) {
    py::class_<OuterInterface, std::shared_ptr<OuterInterface>, OuterInterfaceTrampoline>(module, "OuterInterface")
        .def(py::init<>())
        .def("foo", [](OuterInterface& self, const ::std::string& input) {
            return self.foo(input);
        }, py::arg("input"))
        ;
}

