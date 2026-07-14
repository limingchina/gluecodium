

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ChildInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ChildInterface = ::smoke::ChildInterface;

class ChildInterfaceTrampoline : public ChildInterface {
public:
    using ChildInterface::ChildInterface;

    void child_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, ChildInterface, child_method);
    }
};

void register_ChildInterface(py::module_& module) {
    py::class_<ChildInterface, std::shared_ptr<ChildInterface>, ChildInterfaceTrampoline>(module, "ChildInterface")
        .def(py::init<>())
        .def("child_method", [](ChildInterface& self) {
            return self.child_method();
        })
        ;
}

