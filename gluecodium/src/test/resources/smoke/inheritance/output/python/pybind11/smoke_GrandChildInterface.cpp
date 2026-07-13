

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/GrandChildInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using GrandChildInterface = ::gluecodium::smoke::GrandChildInterface;

class GrandChildInterfaceTrampoline : public GrandChildInterface {
public:
    using GrandChildInterface::GrandChildInterface;

    void grand_child_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, GrandChildInterface, grand_child_method);
    }
};

void register_GrandChildInterface(py::module_& module) {
    py::class_<GrandChildInterface, std::shared_ptr<GrandChildInterface>, GrandChildInterfaceTrampoline>(module, "GrandChildInterface")
        .def("grand_child_method", &GrandChildInterface::grand_child_method)
        ;
}

